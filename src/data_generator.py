import json
import re
import logging
import src.configs as configs
import src.data_types as datatypes
import src.random_generator_impl as rgi
import src.types_patterns as tp
from datetime import date
from src.attribute import Attribute
from src.table import Table


all_tables_dict: dict[str,Table] = {}

def _generate_field(attribute: Attribute) -> dict[str]: 
    '''
    This generates random values according to a datatype.
    '''
    global all_tables_dict

    key = attribute.name
    datatype = attribute.datatype
    args = attribute.args
    nullable = attribute.nullable
    autoinc_value = attribute.autoinc
    value = None
    
    for i in range(configs.MAX_TRIES_GEN_RAND):
        match datatype:
            case datatypes.STRING:
                value = rgi.generate_random_string(args[0], args[1])

            case datatypes.INT:
                value = rgi.generate_random_int(args[0], args[1])

            case datatypes.FLOAT:
                value = rgi.generate_random_float(args[0], args[1])
            
            case datatypes.PRECISION:
                value = rgi.generate_random_float_with_decimals(args[1], args[2], args[0])
            
            case datatypes.BOOLEAN:
                value = rgi.generate_random_boolean(args[0])
            
            case datatypes.DATETIME:
                value = rgi.generate_random_datetime(args[0], args[1]).strftime(configs.DATE_FORMAT)
            
            case datatypes.FORMATTED_DATETIME:
                value = rgi.generate_random_datetime(args[1], args[2]).strftime(args[0])
            
            case datatypes.TOKENS:
                value = rgi.generate_random_from_pool(args)
            
            case datatypes.AUTOINC:
                value = autoinc_value
                attribute.autoinc += args[1]
            
            case datatypes.FOREIGN:
                values_pool = all_tables_dict[args[0]].get_attribute(args[1]).values
                value = rgi.generate_random_from_pool(values_pool)
            
            case datatypes.NULL:
                value = None

        # nullable attributes have a random chance of getting the null value
        value = None if rgi.generate_random_float(0,1) < configs.CHANCE_RANDOM_NULL and nullable else value

        # keys can't have repeated values. this checks for repeated value and re-generates it if necessary.
        if attribute.is_key():
            if attribute.add_value(value):
                break
            
            else:
                if (i+1 == configs.MAX_TRIES_GEN_RAND):
                    logging.warning("WARN: Could not generate enough values for attribute {}. ".format(attribute.name) + \
                          "Consider increasing the range (or having better luck with RNGs).")
                    value = None
                else:
                    continue
        
        else:
            break

    return {
        key: value
    }


def _parse_type(typeStr: str) -> tuple[str,list] :
    '''
    This parses a line in the schema file containing attribute, datatype and parameters.
    '''

    match_result = re.match(tp.all_patterns, typeStr, re.IGNORECASE)
    if match_result is not None:
        datatype = next((item for item in match_result.groups() if item is not None), datatypes.NULL)
        
        match datatype.lower():
            case datatypes.VOC_AUTOINC:
                start = configs.AUTOINC_START if match_result.group(20) is None else (int)(match_result.group(20))
                step = configs.AUTOINC_STEP if match_result.group(21) is None else (int)(match_result.group(21))
                
                return datatypes.AUTOINC, [start,step]
            
            case datatypes.VOC_STRING | datatypes.VOC_VARCHAR:
                min = configs.MIN_STRING_LENGTH if match_result.group(2) is None else (int)(match_result.group(2))
                max = configs.MAX_STRING_LENGTH if match_result.group(3) is None else (int)(match_result.group(3))

                min = configs.MIN_STRING_LENGTH if min < 0 else min
                max = configs.MAX_STRING_LENGTH if max < 0 else max
                if (max < min):
                    aux = max
                    max = min
                    min = aux
                return datatypes.STRING, [min, max]

            case datatypes.VOC_INT | datatypes.VOC_NUMBER:
                min = configs.MIN_NUMBER if match_result.group(2) is None else (int)(match_result.group(2))
                max = configs.MAX_NUMBER if match_result.group(3) is None else (int)(match_result.group(3))
                if (max < min):
                    aux = max
                    max = min
                    min = aux
                return datatypes.INT, [min, max]

            case datatypes.VOC_FLOAT:
                min = configs.MIN_NUMBER if match_result.group(2) is None else (int)(match_result.group(2))
                max = configs.MAX_NUMBER if match_result.group(3) is None else (int)(match_result.group(3))
                if (max < min):
                    aux = max
                    max = min
                    min = aux
                return datatypes.FLOAT, [min, max]

            case datatypes.VOC_TOKENS:
                tokens_list = match_result.group(5).split(",")

                return datatypes.TOKENS, tokens_list
            
            case datatypes.VOC_PRECISION:
                precision = (int)(match_result.group(7))
                min = configs.MIN_PRECISION_NUMBER if match_result.group(8) is None else (int)(match_result.group(8))
                max = configs.MAX_PRECISION_NUMBER if match_result.group(9) is None else (int)(match_result.group(9))
                
                if (max < min):
                    aux = max
                    max = min
                    min = aux

                return datatypes.PRECISION, [precision, min, max]
            
            case datatypes.VOC_BOOLEAN:
                chance = 0.5 if match_result.group(11) is None else (float)(match_result.group(11))
                chance = 0.5 if chance > 1 else chance

                return datatypes.BOOLEAN, [chance]
            
            case datatypes.VOC_DATETIME:
                date1 = configs.MIN_RANDOM_DATE if match_result.group(13) is None else date.fromisoformat(match_result.group(13))
                date2 = configs.MAX_RANDOM_DATE if match_result.group(14) is None else date.fromisoformat(match_result.group(14))
                
                if date1 > date2:
                    aux = date1
                    date1 = date2
                    date2 = aux

                return datatypes.DATETIME, [date1, date2]
            
            case datatypes.VOC_FORM_DATETIME:
                format = match_result.group(16)
                date1 = configs.MIN_RANDOM_DATE if match_result.group(17) is None else date.fromisoformat(match_result.group(17))
                date2 = configs.MAX_RANDOM_DATE if match_result.group(18) is None else date.fromisoformat(match_result.group(18))
                
                if date1 > date2:
                    aux = date1
                    date1 = date2
                    date2 = aux

                return datatypes.FORMATTED_DATETIME, [format, date1, date2]
            
            case datatypes.VOC_FOREIGN:
                table = match_result.group(23)
                attribute = match_result.group(24)
                found = False
                
                if table in all_tables_dict:
                    t:Table = all_tables_dict[table]
                    for att in t.attributes:
                        if attribute == att.name and att.is_key():
                            found = True 

                if found:   
                    return datatypes.FOREIGN, [table,attribute]
                else:
                    logging.warning("Did not find {}.{}. Is must be already defined before ".format(table, attribute) \
                                    + "this attribute. It also must be defined as a Key (optional K).")
            
            case _:
                logging.warning("Could not identify datatype when reading [{}].".format(typeStr))
                                
    return datatypes.NULL, []
    

def _generate_schema(schema_description: str) -> list[Table]:
    '''
    This parses schema file containing tables
    '''
    global all_tables_dict
    tables = []
    table:Table = None
    table_re = "^(\w+) (\d+)$"
    attribute_re = "^([\w]+) ([a-zA-Z][^ ]+)( [N|K|F]+)?"
    for line in schema_description.split("\n"):
        line = line.strip()

        if line.startswith("#") or len(line) == 0:
            continue

        match_result = re.match(table_re, line, re.IGNORECASE)
        if match_result is not None:
            table_name = match_result.group(1)
            quantity = (int)(match_result.group(2))
            
            if table is not None:
                all_tables_dict[table.name] = table
                tables.append(table)

            table = Table(table_name, quantity)

        else:
            match_result = re.match(attribute_re, line, re.IGNORECASE)
            if match_result is not None:
                attribute_name = match_result.group(1)
                datatype, args = _parse_type(match_result.group(2))
                if match_result.group(3) is not None:
                    nullable = "N" in match_result.group(3)
                    pk = "K" in match_result.group(3)
                    
                else:
                    nullable = pk = False

                table.with_attribute(Attribute(attribute_name, datatype, args, nullable, pk, False))

    if table is not None:
        all_tables_dict[table.name] = table
        tables.append(table)

    # for t in tables:
    #     t.print()

    return tables
    # tables must be returned in order they are read. investigate if dict.values() messes up the order
    # return all_tables_dict.values()
    # investigate the use of OrderedDict


def _read_input_schema_from_file(filePath) -> list[Table]:
    '''
    This reads and parses the input schema from a file.
    '''
    with open(filePath, "r") as file:
        object = file.read()
        
        return _generate_schema(object)



def _generate_record(schema: Table) -> dict:
    '''
    This generates a record according to a schema
    '''
    record = {}
    for item in schema.attributes:
        record.update(_generate_field(item))
    
    return record

def run(file_str:str, file_out:str):
    tables = _read_input_schema_from_file(file_str)
    
    with open(file_out, "w") as f:

        for table in tables:
            for i in range(table.qt_records):
                record = _generate_record(table)

                f.write(json.dumps(record) + "\n")


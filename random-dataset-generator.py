
import json
import re
import src.configs as configs
import src.data_types as datatypes
import logging
import src.random_generator as random_generator
import src.types_patterns as tp
from datetime import date
from src.attribute import Attribute
from src.table import Table


all_tables_dict: dict[str,Table] = {}

file_str = "input-schema.txt"
file_out = "generated_records.json"


def generate_field(attribute: Attribute) -> dict[str]: 
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
                value = random_generator.generate_random_string(args[0], args[1])

            case datatypes.INT:
                value = random_generator.generate_random_int(args[0], args[1])

            case datatypes.FLOAT:
                value = random_generator.generate_random_float(args[0], args[1])
            
            case datatypes.PRECISION:
                value = random_generator.generate_random_float_with_decimals(args[1], args[2], args[0])
            
            case datatypes.BOOLEAN:
                value = random_generator.generate_random_boolean(args[0])
            
            case datatypes.DATETIME:
                value = random_generator.generate_random_datetime(args[0], args[1]).strftime(configs.DATE_FORMAT)
            
            case datatypes.FORMATTED_DATETIME:
                value = random_generator.generate_random_datetime(args[1], args[2]).strftime(args[0])
            
            case datatypes.TOKENS:
                value = random_generator.generate_random_from_pool(args)
            
            case datatypes.AUTOINC:
                value = autoinc_value
                attribute.autoinc += args[1]
            
            case datatypes.FOREIGN:
                values_pool = all_tables_dict[args[0]].get_attribute(args[1]).values
                value = random_generator.generate_random_from_pool(values_pool)
            
            case datatypes.NULL:
                value = None

        # nullable attributes have a random chance of getting the null value
        value = None if random_generator.generate_random_float(0,1) < configs.CHANCE_RANDOM_NULL and nullable else value

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


def parse_type(typeStr: str) -> tuple[str,list] :
    '''
    This parses a line in the schema file containing attribute, datatype and parameters.
    '''

    # match for STRING | VARCHAR | INT | FLOAT
    match_result = re.match(tp.pattern_str_int, typeStr, re.IGNORECASE)
    
    if match_result is not None:
        datatype = match_result.group(1).lower()

        if datatype == 'string' or datatype == 'varchar':
            min = configs.MIN_STRING_LENGTH if match_result.group(2) is None else (int)(match_result.group(2))
            max = configs.MAX_STRING_LENGTH if match_result.group(3) is None else (int)(match_result.group(3))

            min = 0 if min < 0 else min
            datatype = datatypes.STRING
        else:
            min = configs.MIN_NUMBER if match_result.group(2) is None else (int)(match_result.group(2))
            max = configs.MAX_NUMBER if match_result.group(3) is None else (int)(match_result.group(3))
            datatype = datatypes.FLOAT if datatype == "float" else datatypes.INT

        if (max < min):
            aux = max
            max = min
            min = aux

        return datatype, [min, max]
    
    else:
        # match for TOKENS
        match_result = re.match(tp.pattern_tokens, typeStr, re.IGNORECASE)
        if match_result is not None:
            
            tokens_list = match_result.group(2).split(",")

            return datatypes.TOKENS, tokens_list
    
        else:
            # match for PRECISION
            match_result = re.match(tp.pattern_precision, typeStr, re.IGNORECASE)
            if match_result is not None:
                
                precision = (int)(match_result.group(2))
                min = configs.MIN_PRECISION_NUMBER if match_result.group(3) is None else (int)(match_result.group(3))
                max = configs.MAX_PRECISION_NUMBER if match_result.group(4) is None else (int)(match_result.group(4))
                
                if (max < min):
                    aux = max
                    max = min
                    min = aux

                return datatypes.PRECISION, [precision, min, max]
            
            else:
                # match for BOOLEAN
                match_result = re.match(tp.pattern_bool, typeStr, re.IGNORECASE)
                if match_result is not None:
                    datatype = match_result.group(1).lower()

                    chance = 0.5 if match_result.group(2) is None else (float)(match_result.group(2))
                    chance = 0.5 if chance > 1 else chance

                    return datatypes.BOOLEAN, [chance]
            
                else:
                    # match for DATETIME
                    match_result = re.match(tp.pattern_datetime, typeStr, re.IGNORECASE)
                    if match_result is not None:
                        date1 = configs.MIN_RANDOM_DATE if match_result.group(2) is None else date.fromisoformat(match_result.group(2))
                        date2 = configs.MAX_RANDOM_DATE if match_result.group(3) is None else date.fromisoformat(match_result.group(3))
                        
                        if date1 > date2:
                            aux = date1
                            date1 = date2
                            date2 = aux

                        return datatypes.DATETIME, [date1, date2]
                    
                    else:
                        # match for FORMATTED_DATETIME
                        match_result = re.match(tp.pattern_formatted_datetime, typeStr, re.IGNORECASE)
                        if match_result is not None:
                            format = match_result.group(2)
                            date1 = configs.MIN_RANDOM_DATE if match_result.group(3) is None else date.fromisoformat(match_result.group(3))
                            date2 = configs.MAX_RANDOM_DATE if match_result.group(4) is None else date.fromisoformat(match_result.group(4))
                            
                            if date1 > date2:
                                aux = date1
                                date1 = date2
                                date2 = aux

                            return datatypes.FORMATTED_DATETIME, [format, date1, date2]
                        
                        else:
                            # match for AUTOINC
                            match_result = re.match(tp.pattern_autoinc, typeStr, re.IGNORECASE)
                            if match_result is not None:
                                start = configs.AUTOINC_START if match_result.group(2) is None else (int)(match_result.group(2))
                                step = configs.AUTOINC_STEP if match_result.group(3) is None else (int)(match_result.group(3))
                                
                                return datatypes.AUTOINC, [start,step]
                            
                            else:
                                global all_tables_dict

                                # match for FOREIGN
                                match_result = re.match(tp.pattern_foreign, typeStr, re.IGNORECASE)
                                if match_result is not None:
                                    table = match_result.group(2)
                                    attribute = match_result.group(3)
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

                                        
    logging.warning("WARN: {} din't match with any datatypes".format(typeStr))
    return datatypes.NULL, []
    

def read_input_schema_from_file(filePath) -> list[Table]:
    '''
    This reads and parses the input schema from a file.
    '''
    with open(filePath, "r") as file:
        object = file.read()
        
        return generate_schema(object)


def generate_schema(schema_description: str) -> list[Table]:
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
                datatype, args = parse_type(match_result.group(2))
                if match_result.group(3) is not None:
                    nullable = "N" in match_result.group(3)
                    pk = "K" in match_result.group(3)
                    
                else:
                    nullable = pk = False

                table.with_attribute(Attribute(attribute_name, datatype, args, nullable, pk, False))

    if table is not None:
        all_tables_dict[table.name] = table
        tables.append(table)

    for t in tables:
        t.print()

    return tables
    # tables must be returned in order they are read. investigate if dict.values() messes up the order
    # return all_tables_dict.values()


def generate_record(schema: Table) -> dict:
    '''
    This generates a record according to a schema
    '''
    record = {}
    for item in schema.attributes:
        record.update(generate_field(item))
    
    return record


def run(file_str:str, file_out:str):
    tables = read_input_schema_from_file(file_str)
    
    with open(file_out, "w") as f:

        for table in tables:
            for i in range(table.qt_records):
                record = generate_record(table)

                f.write(json.dumps(record) + "\n")




# parse_type("string(10)")                        # not-accepted: it will take default min, max values
# parse_type("string(10,20)")                     # it takes min as 10 and max as 20
# parse_type("int")                               # it takes default min as 0 and max as 100
# parse_type("int(33,5)")                         # it will revert min as 5 and max as 33
# parse_type("int(3,5)")                          # it takes min as 3 and max as 5
# parse_type("tokens(a,b,c,12)")                  # it uses randomly one of the 4 tokens provided
# parse_type("precision(10)")                     # it uses 10 decimal points, min as 0 and max as 10
# parse_type("precision(10,20,30)")               # it uses 10 decimal points, min as 20 and max as 30
# parse_type("precision(10,5,3)")                 # it uses 10 decimal points, min as 3 and max as 5
# parse_type("boolean")                           # it uses .5 chance of true
# parse_type("boolean(0.23)")                     # it uses .23 chance of true
# parse_type("boolean(1.23)")                     # it uses .5 chance of true
# parse_type("date(2020-02-20,2021-11-21)")       # it generates dates between the specified dates
# parse_type("date(2022-02-20,2021-11-21)")       # it generates dates between the specified dates
# parse_type("date")                              # it generates dates between 1970 and today
# parse_type("formatted_date(%m/%d/%Y,2020-02-20,2021-11-21)")
# parse_type("formatted_date(%m/%d/%Y,2022-02-20,2021-11-21)")
# parse_type("formatted_date(%m/%d/%Y)")          # it generates dates between 1970 and today
# parse_type("autoinc(1,10)")                     # it generates an incremental value starting at 1 and adding 10 each time
# parse_type("autoinc(-1,10)")                    # it generates an incremental value starting at -1 and adding 10 each time
# parse_type("autoinc(1,-10)")                    # it generates an incremental value starting at 1 and adding -10 each time
# parse_type("autoinc(10)")                       # not accepted: it generates an incremental value starting at 1 and adding 1 each time
# parse_type("autoinc")                           # it generates an incremental value starting at 1 and adding 1 each time
# parse_type("foreign(table.attribute)")          # it generates values from the pool of values from table.attribute
# allow null values with option N at the end of the line
# allow distinct values with option K at the end of the line

# date formats: https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes


run(file_str, file_out)

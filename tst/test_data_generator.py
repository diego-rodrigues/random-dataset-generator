import unittest
import src.data_generator as dg
import src.data_types as datatypes
import src.configs as configs
from datetime import datetime
from src.table import Table
from src.attribute import Attribute


class TestAttribute(unittest.TestCase):

    def test_generate_schema_one_table(self):
        schemaStr = "Table 10\nid INT"
        table = Table("Table", 10)
        table.with_attribute(Attribute("id",datatypes.INT,[0,100]))
        
        actual = dg._generate_schema(schemaStr)
        expected = [table]
        self.assertListEqual(actual, expected)

    def test_generate_schema_multi_table(self):
        schemaStr = "TableA 10\nid INT(-1,20)\n\nTableB 5\nid AUTOINC"
        tableA = Table("TableA", 10)
        tableA.with_attribute(Attribute("id",datatypes.INT,[-1,20]))
        tableB = Table("TableB", 5)
        tableB.with_attribute(Attribute("id",datatypes.AUTOINC,[1,1]))
        
        actual = dg._generate_schema(schemaStr)
        expected = [tableA, tableB]
        self.assertListEqual(actual, expected)

    def test_parse_type_str_default(self):
        inputStr = "string"
        
        expected = (datatypes.STRING, [configs.MIN_STRING_LENGTH, configs.MAX_STRING_LENGTH])
        actual = dg._parse_type(inputStr)
        self.assertEqual(actual, expected)

    def test_parse_type_str_args(self):
        inputStr = "string(5,10)"
        
        expected = (datatypes.STRING, [5,10])
        actual = dg._parse_type(inputStr)
        self.assertEqual(actual, expected)

    def test_parse_type_str_neg_reverse(self):
        inputStr = "string(5,-5)"
        
        expected = (datatypes.STRING, [5,10])
        actual = dg._parse_type(inputStr)
        self.assertEqual(actual, expected)

    
    def test_parse_type_varchar_default(self):
        inputStr = "varchar"
        
        expected = (datatypes.STRING, [configs.MIN_STRING_LENGTH, configs.MAX_STRING_LENGTH])
        actual = dg._parse_type(inputStr)
        self.assertEqual(actual, expected)

    def test_parse_type_autoinc_default(self):
        inputStr = "autoinc"
        
        expected = (datatypes.AUTOINC, [configs.AUTOINC_START, configs.AUTOINC_STEP])
        actual = dg._parse_type(inputStr)
        self.assertEqual(actual, expected)

    def test_parse_type_autoinc_args(self):
        inputStr = "autoinc(3,4)"
        
        expected = (datatypes.AUTOINC, [3,4])
        actual = dg._parse_type(inputStr)
        self.assertEqual(actual, expected)

    def test_parse_type_autoinc_args_neg(self):
        inputStr = "autoinc(-3,-4)"
        
        expected = (datatypes.AUTOINC, [-3,-4])
        actual = dg._parse_type(inputStr)
        self.assertEqual(actual, expected)

    def test_parse_type_int_default(self):
        inputStr = "int"
        
        expected = (datatypes.INT, [configs.MIN_NUMBER, configs.MAX_NUMBER])
        actual = dg._parse_type(inputStr)
        self.assertEqual(actual, expected)

    def test_parse_type_int_args(self):
        inputStr = "int(3,4)"
        
        expected = (datatypes.INT, [3,4])
        actual = dg._parse_type(inputStr)
        self.assertEqual(actual, expected)

    def test_parse_type_int_args_neg_rev(self):
        inputStr = "int(-3,-4)"
        
        expected = (datatypes.INT, [-4,-3])
        actual = dg._parse_type(inputStr)
        self.assertEqual(actual, expected)

    def test_parse_type_number_default(self):
        inputStr = "number"
        
        expected = (datatypes.INT, [configs.MIN_NUMBER, configs.MAX_NUMBER])
        actual = dg._parse_type(inputStr)
        self.assertEqual(actual, expected)

    def test_parse_type_float_default(self):
        inputStr = "float"
        
        expected = (datatypes.FLOAT, [configs.MIN_NUMBER, configs.MAX_NUMBER])
        actual = dg._parse_type(inputStr)
        self.assertEqual(actual, expected)

    def test_parse_type_float_args(self):
        inputStr = "float(3,4)"
        
        expected = (datatypes.FLOAT, [3,4])
        actual = dg._parse_type(inputStr)
        self.assertEqual(actual, expected)

    def test_parse_type_float_args_neg_rev(self):
        inputStr = "float(-3,-4)"
        
        expected = (datatypes.FLOAT, [-4,-3])
        actual = dg._parse_type(inputStr)
        self.assertEqual(actual, expected)

    def test_parse_type_precision_args(self):
        inputStr = "precision(1,3,4)"
        
        expected = (datatypes.PRECISION, [1,3,4])
        actual = dg._parse_type(inputStr)
        self.assertEqual(actual, expected)

    def test_parse_type_precision_args_neg_rev(self):
        inputStr = "precision(2,-3,-4)"
        
        expected = (datatypes.PRECISION , [2,-4,-3])
        actual = dg._parse_type(inputStr)
        self.assertEqual(actual, expected)

    def test_parse_type_datetime_default(self):
        inputStr = "datetime"
        
        expected = (datatypes.DATETIME, [configs.MIN_RANDOM_DATE, configs.MAX_RANDOM_DATE])
        actual = dg._parse_type(inputStr)
        self.assertEqual(actual, expected)

    def test_parse_type_datetime_args(self):
        inputStr = "datetime(1920-11-01,2024-12-02)"
        
        expected = (datatypes.DATETIME, [datetime(1920,11,1,0,0).date(),datetime(2024,12,2,0,0).date()])
        actual = dg._parse_type(inputStr)
        self.assertEqual(actual, expected)

    def test_parse_type_datetime_args_rev(self):
        inputStr = "datetime(2024-12-02,1920-11-01)"
        
        expected = (datatypes.DATETIME, [datetime(1920,11,1,0,0).date(),datetime(2024,12,2,0,0).date()])
        actual = dg._parse_type(inputStr)
        self.assertEqual(actual, expected)
    
    def test_parse_type_formatted_datetime_default(self):
        inputStr = "formatted_datetime(%d%m%Y)"
        
        expected = (datatypes.FORMATTED_DATETIME, ["%d%m%Y",configs.MIN_RANDOM_DATE, configs.MAX_RANDOM_DATE])
        actual = dg._parse_type(inputStr)
        self.assertEqual(actual, expected)

    def test_parse_type_formatted_datetime_args(self):
        inputStr = "formatted_datetime(%d%m%Y,1920-11-01,2024-12-02)"
        
        expected = (datatypes.FORMATTED_DATETIME, ["%d%m%Y",datetime(1920,11,1,0,0).date(),datetime(2024,12,2,0,0).date()])
        actual = dg._parse_type(inputStr)
        self.assertEqual(actual, expected)

    def test_parse_type_formatted_datetime_args_rev(self):
        inputStr = "formatted_datetime(%d%m%Y,2024-12-02,1920-11-01)"
        
        expected = (datatypes.FORMATTED_DATETIME, ["%d%m%Y",datetime(1920,11,1,0,0).date(),datetime(2024,12,2,0,0).date()])
        actual = dg._parse_type(inputStr)
        self.assertEqual(actual, expected)

    def test_parse_type_boolean_default(self):
        inputStr = "boolean"
        
        expected = (datatypes.BOOLEAN, [0.50])
        actual = dg._parse_type(inputStr)
        self.assertEqual(actual, expected)

    def test_parse_type_boolean_arg(self):
        inputStr = "boolean(0.35)"
        
        expected = (datatypes.BOOLEAN, [0.35])
        actual = dg._parse_type(inputStr)
        self.assertEqual(actual, expected)

    def test_parse_type_boolean_arg_zero(self):
        inputStr = "boolean(0.0)"
        
        expected = (datatypes.BOOLEAN, [0.0])
        actual = dg._parse_type(inputStr)
        self.assertEqual(actual, expected)

    def test_parse_type_boolean_arg_one(self):
        inputStr = "boolean(1.0)"
        
        expected = (datatypes.BOOLEAN, [1.0])
        actual = dg._parse_type(inputStr)
        self.assertEqual(actual, expected)

    def test_parse_type_tokens(self):
        inputStr = "tokens(a)"
        
        expected = (datatypes.TOKENS, ["a"])
        actual = dg._parse_type(inputStr)
        self.assertEqual(actual, expected)

    def test_parse_type_tokens_mult(self):
        inputStr = "tokens(a,b,c,d)"
        
        expected = (datatypes.TOKENS, ["a","b","c","d"])
        actual = dg._parse_type(inputStr)
        self.assertEqual(actual, expected)

    def test_parse_type_foreign(self):
        dg.all_tables_dict = dict()
        tableA = Table("tableA",10)
        tableA.with_attribute(Attribute("attB", datatypes.AUTOINC, [1,1], False, True))
        dg.all_tables_dict["tableA"] = tableA

        inputStr = "foreign(tableA.attB)"
        
        expected = (datatypes.FOREIGN, ["tableA", "attB"])
        actual = dg._parse_type(inputStr)
        self.assertEqual(actual, expected)

    def test_parse_type_error(self):
        inputStr = "unknown"
        
        expected = (datatypes.NULL, [])
        actual = dg._parse_type(inputStr)
        self.assertEqual(actual, expected)


    
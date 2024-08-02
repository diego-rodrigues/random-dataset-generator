import unittest
from src.table import Table
from src.attribute import Attribute

class TestTable(unittest.TestCase):

    def test_create_table(self):
        t = Table("test", 10)
        self.assertEqual(t.name, "test")
        self.assertEqual(t.attributes, list())
        self.assertEqual(t.qt_records, 10)

    def test_add_attribute(self):
        t = Table("test", 10)
        att = Attribute("att", "str", [])
        t.with_attribute(att)

        self.assertTrue(att in t.attributes)
        self.assertTrue(t.has_attribute("att"))
    
    def test_get_attribute(self):
        t = Table("test", 10)
        att = Attribute("att", "str", [])
        t.with_attribute(att)

        att_get = t.get_attribute("att")
        self.assertEqual(att_get.name, "att")

    def test_print(self):
        t = Table("test", 10)
        self.assertIsNotNone(t.__str__)

if __name__ == '__main__':
    unittest.main() 

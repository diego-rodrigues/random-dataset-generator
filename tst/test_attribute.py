import unittest
from src.attribute import Attribute

class TestAttribute(unittest.TestCase):

    def test_create_attribute(self):
        att = Attribute("test", "str", [])
        self.assertEqual(att.name, "test")
        self.assertEqual(att.datatype, "str")
        self.assertEqual(att.args, [])
        self.assertFalse(att.nullable)
        self.assertFalse(att.pk)
        self.assertFalse(att.fk)
        self.assertEqual(att.values, list())
        self.assertEqual(att.autoinc, 0)

    def test_modifiers_true(self):
        att = Attribute("test", "str", [], False, True, True)
        self.assertFalse(att.nullable)
        self.assertTrue(att.pk)
        self.assertTrue(att.fk)
        self.assertEqual(att.modifiers_str(),' PKFK')

        att = Attribute("test", "str", [], False, False, True)
        self.assertEqual(att.modifiers_str(),'   FK')

        att = Attribute("test", "str", [], True, False, True)
        self.assertEqual(att.modifiers_str(),'N  FK')
        
        att = Attribute("test", "str", [], False, False, False)
        self.assertEqual(att.modifiers_str(),'     ')

    def test_is_key(self):
        att = Attribute("test", "str", [], False, True, True)
        self.assertTrue(att.is_key())

        att = Attribute("test", "str", [])
        self.assertFalse(att.is_key())

    def test_add_values(self):
        att = Attribute("test", "str", [])
        self.assertFalse(att.has_value("str"))

        att.add_value("str")
        self.assertTrue(att.has_value("str"))

    def test_print(self):
        att = Attribute("test", "str", [], False, True, True)
        self.assertIsNotNone(att.__str__)

if __name__ == '__main__':
    unittest.main() 

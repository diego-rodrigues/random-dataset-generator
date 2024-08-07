
from src.attribute import Attribute
from src.configs import PRINT_LINE_SIZE

class Table:
    def __init__(self, name: str, qt_records: int):
        self.name = name
        self.attributes:list[Attribute] = []
        self.qt_records = qt_records


    def with_attribute(self, attribute: Attribute):
        self.attributes.append(attribute)

    def has_attribute(self, attribute_name: str):
        for a in self.attributes:
            if a.name == attribute_name:
                return True
        return False
    
    def get_attribute(self, attribute_name: str):
        for a in self.attributes:
            if a.name == attribute_name:
                return a
        return None

    def __str__(self):
        line_text_size = PRINT_LINE_SIZE
        str = "|{:{fill}<{len}}|\n".format("",fill="-",len=line_text_size+7) + \
        "| {:{len}} {:>4} |\n".format(self.name, self.qt_records,len=line_text_size) + \
        "|{:{fill}<{len}}|\n".format("",fill="=",len=line_text_size+7);
    
        for a in self.attributes:
            att = (a.name[:(line_text_size-14)] + '..') if len(a.name) > (line_text_size-14) else a.name
            datatype = (a.datatype[:8]) if len(a.datatype) > 8 else a.datatype
            str += "| > {:{len}} {:8} {:5} |\n".format(att, datatype, a.modifiers_str(),len=line_text_size-12)
            
        str += "|{:{fill}<{len}}|\n".format("",fill="-",len=line_text_size+7)
        return str

    def print(self):
        print(self)

    def __eq__(self, other):
        if isinstance(other, Table):
            return self.name == other.name \
                and self.qt_records == other.qt_records \
                and self.attributes == other.attributes
        return False

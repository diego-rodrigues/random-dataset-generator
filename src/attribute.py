import logging
from src.data_types import AUTOINC

class Attribute:
    def __init__(self, name: str, datatype: str, args: list, nullable: bool = False, pk: bool = False, fk: bool = False):
        self.name = name
        self.datatype = datatype
        self.args = args
        self.nullable = nullable
        self.pk = pk
        self.fk = fk
        self.values = []
        self.autoinc = 0 if datatype != AUTOINC else args[0]
        if (pk and nullable):
            logging.warning("WARN: Attribute [{}] can't be a Key and Nullable. Ignoring nullable option.".format(self.name))
            self.nullable = False

    def modifiers_str(self) -> str:
        ret = "N" if self.nullable else " "
        ret += "PK" if self.pk else "  "
        ret += "FK" if self.fk else "  "
        return ret
        
    def has_value(self, obj) -> bool:
        return obj in self.values
    
    def add_value(self, obj) -> bool:
        if self.has_value(obj):
            return False

        else:
            self.values.append(obj)
            return True

    def is_key(self) -> bool:
        return self.pk
    
    def __str__(self):
        return "{} :{}({}) | {}".format(self.name, self.datatype, self.args, self.modifiers_str())
    
    def __eq__(self, other):
        if isinstance(other, Attribute):
            return self.name == other.name \
                and self.datatype == other.datatype \
                and self.args == other.args \
                and self.nullable == other.nullable \
                and self.pk == other.pk \
                and self.fk == other.fk \
                and self.values == other.values \
                and self.autoinc == other.autoinc
        return False

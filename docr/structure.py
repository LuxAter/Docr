from enum import Enum


class Type(Enum):
    NONE = 0
    TU = 1
    TEXT = 2
    BOLD = 3
    ITALIC = 4
    INLINE_CODE = 5
    INLINE_MATH = 6
    ITEM = 7
    ENUM = 8
    CODE = 9
    MATH = 10
    DEFINITION = 11
    ADMONITON = 12


class Element():
    def __init__(self, string=str(), type=Type.NONE, meta=None):
        self.data = string
        if meta:
            if isinstance(meta, list) is False:
                self.meta_data = [meta]
            else:
                self.meta_data = meta
        else:
            self.meta_data = list()
        self.type = type

    def __nonzero__(self):
        if self.data is False:
            return False
        for elem in self.data:
            if elem is True:
                return True
        return False

    def __repr__(self):
        return '(' + repr(self.type) + ', ' + repr(
            self.meta_data) + ', ' + repr(self.data) + ')'

    def print(self, indent=0):
        ret = (' ' * indent) + '(' + repr(self.type) + ', '
        length = len(ret)
        new = False
        ret += repr(self.meta_data)
        length = len(ret)
        ret += ', '
        if self.data:
            if isinstance(self.data, list):
                ret += '[\n'
                for item in self.data:
                    if isinstance(item, Element):
                        ret += item.print(indent + length + 2) + '\n'
                    else:
                        ret += (' ' * indent) + repr(item) + '\n'
                ret += (' '* indent) + ']'
                new = True
            else:
                ret += repr(self.data)
        else:
            ret += repr(self.data)
        if new:
            ret += (' ' * indent) + ')'
        else:
            ret += ')'
        return ret

    def append(self, value, cond=True):
        if cond is False:
            self.data.append(value)
        else:
            if self.data and self.data[-1]:
                self.data.append(value)

"""
Docr markup Abstract Syntax Tree.
"""

from enum import Enum


class SyntaxTree(object):

    class Tokens(Enum):
        NONE = 0
        TEXT = 1
        COMMAND = 2
        PARAGRAPH = 3

    class Attrs(Enum):
        NONE = 0
        CODE = 1
        BOLD = 2
        ITALIC = 3


    def __init__(self, token=Tokens.NONE):
        self.token = token
        self.text = str()
        self.lexmes = list()

    def __repr__(self):
        return "<" + str(self.token) + ">"


    def string(self, indent=0):
        rep = (' ' * indent) + self.__repr__() + ": \'" + self.text + "\'"
        for lex in self.lexmes:
            rep += "\n" + lex.string(indent + 1)
        return rep

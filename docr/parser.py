from enum import Enum
from lexer import Lexer
Tokens = Lexer.Tokens


class Parser(object):
    class Object(object):
        class Type(Enum):
            NULL = -1
            TEXT = 0
            CODE = 1
            EMPH = 2
            STRONG = 3
            MATH = 4
            INLINE_MATH = 5
            UNICODE = 6
            PARAGRAPH = 7
            FUNCTION = 8
            TITLE = 9
            ITEMIZE = 10
            ENUMERATION = 11

        def __init__(self):
            self.token = Parser.Object.Type.NULL
            self.title_level = 1
            self.data = list()

        def __repr__(self):
            if self.token != self.Type.TITLE:
                return "<Parser.Object {}> : {}".format(self.token.__repr__(), self.data)
            else:
                return "<Parser.Object {}> : {} : {}".format(self.token.__repr__(), self.title_level, self.data)

        def set_type(self, token):
            if token == Lexer.Tokens.OPEN_PARAGRAPH:
                self.token = Parser.Object.Type.PARAGRAPH
            elif token == Lexer.Tokens.CODE_OPEN_DELIM:
                self.token = Parser.Object.Type.CODE
            elif token == Lexer.Tokens.EMPH_OPEN_DELIM:
                self.token = Parser.Object.Type.EMPH
            elif token == Lexer.Tokens.STRONG_OPEN_DELIM:
                self.token = Parser.Object.Type.STRONG
            elif token == Lexer.Tokens.MATH_OPEN_DELIM:
                self.token = Parser.Object.Type.MATH
            elif token == Lexer.Tokens.MATH_INLINE_OPEN_DELIM:
                self.token = Parser.Object.Type.INLINE_MATH
            elif token == Lexer.Tokens.FUNCTION_OPEN_DELIM:
                self.token = Parser.Object.Type.FUNCTION
            elif token == Lexer.Tokens.OPEN_TITLE:
                self.token = Parser.Object.Type.TITLE
            elif token == Lexer.Tokens.ENUMERATION_DELIM:
                self.token = Parser.Object.Type.ENUMERATION
            elif token == Lexer.Tokens.ITEMIZE_DELIM:
                self.token = Parser.Object.Type.ITEMIZE

    def __init__(self):
        self.lexmes = list()

    @staticmethod
    def is_open(token):
        if token in (Lexer.Tokens.OPEN_PARAGRAPH, Lexer.Tokens.CODE_OPEN_DELIM, Lexer.Tokens.EMPH_OPEN_DELIM, Lexer.Tokens.STRONG_OPEN_DELIM, Lexer.Tokens.MATH_OPEN_DELIM, Lexer.Tokens.MATH_INLINE_OPEN_DELIM, Lexer.Tokens.FUNCTION_OPEN_DELIM, Lexer.Tokens.OPEN_TITLE):
            return True

    @staticmethod
    def is_unended(token):
        if token in (Lexer.Tokens.UNICODE, Lexer.Tokens.ENUMERATION_DELIM, Lexer.Tokens.ITEMIZE_DELIM):
            return True

    def is_closing(self, obj, token):
        if obj == self.Object.Type.PARAGRAPH and token == Lexer.Tokens.CLOSE_PARAGRAPH:
            return True
        elif obj == self.Object.Type.CODE and token == Lexer.Tokens.CODE_CLOSE_DELIM:
            return True
        elif obj == self.Object.Type.EMPH and token == Lexer.Tokens.EMPH_CLOSE_DELIM:
            return True
        elif obj == self.Object.Type.STRONG and token == Lexer.Tokens.STRONG_CLOSE_DELIM:
            return True
        elif obj == self.Object.Type.MATH and token == Lexer.Tokens.MATH_CLOSE_DELIM:
            return True
        elif obj == self.Object.Type.INLINE_MATH and token == Lexer.Tokens.MATH_INLINE_CLOSE_DELIM:
            return True
        elif obj == self.Object.Type.FUNCTION and token == Lexer.Tokens.FUNCTION_CLOSE_DELIM:
            return True
        elif obj == self.Object.Type.TITLE and token == Lexer.Tokens.CLOSE_TITLE:
            return True
        return False

    def create_unended_object(self, lex):
        obj = self.Object()
        obj.set_type(lex[0])
        while len(self.lexmes) > 1:
            lexme = self.lexmes[0]
            self.lexmes = self.lexmes[1:]
            if lexme[0] == Lexer.Tokens.WORD:
                if len(obj.data) == 0 or isinstance(obj.data[-1], Parser.Object) is True:
                    obj.data.append(lexme[1])
                else:
                    obj.data[-1] += ' ' + lexme[1]
            elif self.is_open(lexme[0]) is True or self.is_unended(lexme[0]) is True:
                self.lexmes = [lexme] + self.lexmes
                break
            elif lexme[0] == Lexer.Tokens.CLOSE_PARAGRAPH:
                self.lexmes = [lexme] + self.lexmes
                break
        return obj


    def create_ended_object(self, lex):
        obj = self.Object()
        obj.set_type(lex[0])
        if obj.token == Parser.Object.Type.TITLE:
            obj.title_level = lex[2]
        while len(self.lexmes) > 1:
            lexme = self.lexmes[0]
            self.lexmes = self.lexmes[1:]
            if lexme[0] == Lexer.Tokens.WORD:
                if len(obj.data) == 0 or isinstance(obj.data[-1], Parser.Object) is True:
                    obj.data.append(lexme[1])
                else:
                    obj.data[-1] += ' ' + lexme[1]
            elif self.is_open(lexme[0]) is True:
                obj.data.append(self.create_ended_object(lexme))
            elif self.is_unended(lexme[0]) is True:
                obj.data.append(self.create_unended_object(lexme))
            elif self.is_closing(obj.token, lexme[0]) is True:
                break
        return obj

    def parse(self, lexical):
        self.lexmes = lexical
        objects = list()
        while len(self.lexmes) > 0:
            lexme = self.lexmes[0]
            self.lexmes = self.lexmes[1:]
            objects.append(self.create_ended_object(lexme))
        return objects[:-1]

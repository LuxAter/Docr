"""
Docr markup lexical analyser
"""

from enum import Enum


class Lexer(object):
    class Tokens(Enum):
        WORD = 0
        OPEN_PARAGRAPH = 1
        CLOSE_PARAGRAPH = 2
        CODE_OPEN_DELIM = 3
        CODE_CLOSE_DELIM = 4
        EMPH_OPEN_DELIM = 5
        EMPH_CLOSE_DELIM = 6
        ITAL_OPEN_DELIM = 7
        ITAL_CLOSE_DELIM = 8
        MATH_OPEN_DELIM = 9
        MATH_CLOSE_DELIM = 10
        MATH_INLINE_OPEN_DELIM = 11
        MATH_INLINE_CLOSE_DELIM = 12
        UNICODE = 13
        FUNCTION_OPEN_DELIM = 14
        FUNCTION_CLOSE_DELIM = 15

    @staticmethod
    def is_special(char, delims):
        if len(delims) > 0 and (delims[-1] == Lexer.Tokens.MATH_OPEN_DELIM or delims[-1] == Lexer.Tokens.MATH_INLINE_OPEN_DELIM) and char != '$' and char != ' ':
            return False
        if char in (' ', '`', '*', '$', '_', '\'', '\"', '\n', '\\', '<', '>'):
            return True
        return False

    @staticmethod
    def analyze(filepath):
        tokens = [[Lexer.Tokens.OPEN_PARAGRAPH, str()], [Lexer.Tokens.WORD, str()]]
        escaped = False
        delims = list()
        prev_char = 0
        with open(filepath, 'r') as fi:
            while True:
                char = fi.read(1)
                if not char:
                    break
                elif escaped is True and char == 'u':
                    tokens.append([Lexer.Tokens.UNICODE, str()])
                    escaped = False
                elif escaped is True or Lexer.is_special(char, delims) is False:
                    tokens[-1][1] += char
                elif escaped is False and Lexer.is_special(char, delims) is True:
                    if tokens[-1][1] == str():
                            tokens.pop()
                    if char == '\\':
                        escaped = True
                    elif char == '`':
                        if len(delims) > 0 and delims[-1] == Lexer.Tokens.CODE_OPEN_DELIM:
                            delims.pop()
                            tokens.append([Lexer.Tokens.CODE_CLOSE_DELIM, char])
                        else:
                            delims.append(Lexer.Tokens.CODE_OPEN_DELIM)
                            tokens.append([Lexer.Tokens.CODE_OPEN_DELIM, char])
                        tokens.append([Lexer.Tokens.WORD, str()])
                    elif char == '*':
                        if len(delims) > 0 and delims[-1] == Lexer.Tokens.EMPH_OPEN_DELIM:
                            delims.pop()
                            tokens.append([Lexer.Tokens.EMPH_CLOSE_DELIM, char])
                        else:
                            delims.append(Lexer.Tokens.EMPH_OPEN_DELIM)
                            tokens.append([Lexer.Tokens.EMPH_OPEN_DELIM, char])
                        tokens.append([Lexer.Tokens.WORD, str()])
                    elif char == '_':
                        if len(delims) > 0 and delims[-1] == Lexer.Tokens.ITAL_OPEN_DELIM:
                            delims.pop()
                            tokens.append([Lexer.Tokens.ITAL_CLOSE_DELIM, char])
                        else:
                            delims.append(Lexer.Tokens.ITAL_OPEN_DELIM)
                            tokens.append([Lexer.Tokens.ITAL_OPEN_DELIM, char])
                        tokens.append([Lexer.Tokens.WORD, str()])
                    elif char == '<':
                        delims.append(Lexer.Tokens.FUNCTION_OPEN_DELIM)
                        tokens.append([Lexer.Tokens.FUNCTION_OPEN_DELIM, char])
                        tokens.append([Lexer.Tokens.WORD, str()])
                    elif char == '>' and len(delims) > 0 and delims[-1] == Lexer.Tokens.FUNCTION_OPEN_DELIM:
                        delims.pop()
                        tokens.append([Lexer.Tokens.FUNCTION_CLOSE_DELIM, char])
                        tokens.append([Lexer.Tokens.WORD, str()])
                    elif char == '$' and prev_char != '$':
                        if len(delims) > 0 and (delims[-1] == Lexer.Tokens.MATH_INLINE_OPEN_DELIM or delims[-1] == Lexer.Tokens.MATH_OPEN_DELIM):
                            delims.pop()
                            tokens.append([Lexer.Tokens.MATH_INLINE_CLOSE_DELIM, char])
                        else:
                            delims.append(Lexer.Tokens.MATH_INLINE_OPEN_DELIM)
                            tokens.append([Lexer.Tokens.MATH_INLINE_OPEN_DELIM, char])
                        tokens.append([Lexer.Tokens.WORD, str()])
                    elif char == '$' and prev_char == '$':
                        if len(delims) > 0 and delims[-1] == Lexer.Tokens.MATH_INLINE_OPEN_DELIM:
                            delims[-1] = Lexer.Tokens.MATH_OPEN_DELIM
                            tokens[-1] = [Lexer.Tokens.MATH_OPEN_DELIM, '$$']
                        else:
                            tokens[-1] = [Lexer.Tokens.MATH_CLOSE_DELIM, '$$']
                    elif prev_char == '\n' and char =='\n':
                        tokens.append([Lexer.Tokens.CLOSE_PARAGRAPH, str()])
                        tokens.append([Lexer.Tokens.OPEN_PARAGRAPH, str()])
                        tokens.append([Lexer.Tokens.WORD, str()])
                    else:
                        tokens.append([Lexer.Tokens.WORD, str()])
                elif escaped is True:
                    escaped = False
                prev_char = char
        if tokens[-1][1] == str():
            tokens.pop()
        tokens.append([Lexer.Tokens.CLOSE_PARAGRAPH, str()])
        return tokens

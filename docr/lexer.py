"""
Docr markup lexical analyser
"""

from enum import Enum


class Lexer(object):
    class Tokens(Enum):
        NULL = -1
        WORD = 0
        OPEN_PARAGRAPH = 1
        CLOSE_PARAGRAPH = 2
        CODE_OPEN_DELIM = 3
        CODE_CLOSE_DELIM = 4
        EMPH_OPEN_DELIM = 5
        EMPH_CLOSE_DELIM = 6
        STRONG_OPEN_DELIM = 7
        STRONG_CLOSE_DELIM = 8
        MATH_OPEN_DELIM = 9
        MATH_CLOSE_DELIM = 10
        MATH_INLINE_OPEN_DELIM = 11
        MATH_INLINE_CLOSE_DELIM = 12
        UNICODE = 13
        FUNCTION_OPEN_DELIM = 14
        FUNCTION_CLOSE_DELIM = 15
        ENUMERATION_DELIM = 16
        ITEMIZE_DELIM = 17
        OPEN_TITLE = 18
        CLOSE_TITLE = 19

    def __init__(self):
        self.lex = list()
        self.raw = list()
        self.delims = list()

    def get_token(self, char):
        if char == '`':
            if len(self.delims) > 0 and self.delims[-1] == Lexer.Tokens.CODE_OPEN_DELIM:
                return Lexer.Tokens.CODE_CLOSE_DELIM, True
            return Lexer.Tokens.CODE_OPEN_DELIM, False
        elif char == '*':
            if len(self.delims) > 0 and self.delims[-1] == Lexer.Tokens.STRONG_OPEN_DELIM:
                return Lexer.Tokens.STRONG_CLOSE_DELIM, True
            return Lexer.Tokens.STRONG_OPEN_DELIM, False
        elif char == '_':
            if len(self.delims) > 0 and self.delims[-1] == Lexer.Tokens.EMPH_OPEN_DELIM:
                return Lexer.Tokens.EMPH_CLOSE_DELIM, True
            return Lexer.Tokens.EMPH_OPEN_DELIM, False
        elif char == '$':
            if len(self.delims) > 0 and self.delims[-1] == Lexer.Tokens.MATH_INLINE_OPEN_DELIM:
                return Lexer.Tokens.MATH_INLINE_CLOSE_DELIM, True
            return Lexer.Tokens.MATH_INLINE_OPEN_DELIM, False
        if len(self.delims) > 0 and self.delims[-1] == Lexer.Tokens.NULL:
            return Lexer.Tokens.NULL, True
        return Lexer.Tokens.NULL, False

    def special_char(self, char, prev_char):
        delim, close = self.get_token(char)
        if close is True:
            self.delims.pop()
            if char == '$' and prev_char == '$':
                self.lex.pop()
                if len(self.delims) > 0 and self.delims[-1] == Lexer.Tokens.MATH_OPEN_DELIM:
                    self.delims.pop()
                    delim = Lexer.Tokens.MATH_CLOSE_DELIM
                else:
                    self.delims.append(Lexer.Tokens.MATH_OPEN_DELIM)
                    delim = Lexer.Tokens.MATH_OPEN_DELIM
        else:
            self.delims.append(delim)
        self.lex.append([delim, char])


    def analyze_paragraph(self, par_id):
        par = self.raw[par_id]
        first_in_line = True
        self.lex.append([Lexer.Tokens.OPEN_PARAGRAPH, str()])
        prev_char = 0
        paragraph_iter = iter(par)
        i = 0
        for ch in paragraph_iter:
            if ch != ' ' and first_in_line is True and ch in ('-', '+', '*'):
                first_in_line = False
                self.lex.append([Lexer.Tokens.ITEMIZE_DELIM, ch])
                i += 1
                continue
            if ch == '#' and first_in_line is True:
                first_in_line = False
                st = ch
                for next_char in par[i+1:]:
                    if next_char == '#':
                        st += next_char
                    else:
                        break
                for x in range(1, len(st)):
                    i += 1
                    next(paragraph_iter)
                self.lex.append([Lexer.Tokens.OPEN_TITLE, st, len(st)])
                self.delims.append([Lexer.Tokens.OPEN_TITLE, len(st)])
                i += 1
                continue
            elif ch != ' ' and first_in_line is True and ch in ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9'):
                st = ch
                for next_char in par[i+1:]:
                    if next_char in ('0', '1' ,'2', '3', '4', '5', '6', '7', '8', '9'):
                        st += next_char
                    if next_char in ('.', ')'):
                        st += next_char
                        break
                first_in_line = False
                if st[-1] in ('.', ')'):
                    self.lex.append([Lexer.Tokens.ENUMERATION_DELIM, st])
                    for x in range(1, len(st)):
                        i += 1
                        next(paragraph_iter)
                    i += 1
                    continue
            if ch == '\n':
                first_in_line = True
                if len(self.lex) > 0 and len(self.delims) > 0 and self.lex[-1][1] == '#' * self.delims[-1][1] and self.delims[-1][0] == Lexer.Tokens.OPEN_TITLE:
                    st = self.lex[-1][1]
                    self.lex.pop()
                    self.delims.pop()
                    self.lex.append([Lexer.Tokens.CLOSE_TITLE, st, len(st)])
                self.lex.append([Lexer.Tokens.WORD, str()])
            elif ch in ('`', '*', '$', '_', '\'', '\"', '<', '>'):
                self.special_char(ch, prev_char)
            elif ch == ' ':
                self.lex.append([Lexer.Tokens.WORD, str()])
            else:
                first_in_line = False
                if self.lex[-1][0] == Lexer.Tokens.WORD:
                    self.lex[-1][1] += ch
                else:
                    self.lex.append([Lexer.Tokens.WORD, ch])
            i += 1
            prev_char = ch
        self.lex.append([Lexer.Tokens.CLOSE_PARAGRAPH, str()])

    def analyze(self, filepath):
        self.raw.append(list())
        with open(filepath, 'r') as fi:
            prev_ch = 0
            for line in fi:
                for ch in line:
                    if ch == '\n' and prev_ch == '\n':
                        self.raw.append(list())
                    else:
                        self.raw[-1].append(ch)
                    prev_ch = ch
        for i, par in enumerate(self.raw):
            self.analyze_paragraph(i)
        #  from pprint import pprint
        #  pprint(self.lex)
        return self.lex

    #  def analyze(self, filepath):
        #  tokens = [[Lexer.Tokens.OPEN_PARAGRAPH, str()], [Lexer.Tokens.WORD, str()]]
        #  escaped = False
        #  delims = list()
        #  prev_char = 0
        #  with open(filepath, 'r') as fi:
        #  while True:
        #  char = fi.read(1)
        #  if not char:
        #  break
        #  elif escaped is True and char == 'u':
        #  tokens.append([Lexer.Tokens.UNICODE, str()])
        #  escaped = False
        #  elif escaped is True or Lexer.is_special(char, delims) is False:
        #  tokens[-1][1] += char
        #  elif escaped is False and Lexer.is_special(char, delims) is True:
        #  if tokens[-1][1] == str():
        #  tokens.pop()
        #  if char == '\\':
        #  escaped = True
        #  elif char == '`':
        #  if len(delims) > 0 and delims[-1] == Lexer.Tokens.CODE_OPEN_DELIM:
        #  delims.pop()
        #  tokens.append([Lexer.Tokens.CODE_CLOSE_DELIM, char])
        #  else:
        #  delims.append(Lexer.Tokens.CODE_OPEN_DELIM)
        #  tokens.append([Lexer.Tokens.CODE_OPEN_DELIM, char])
        #  tokens.append([Lexer.Tokens.WORD, str()])
        #  elif char == '*':
        #  if len(delims) > 0 and delims[-1] == Lexer.Tokens.EMPH_OPEN_DELIM:
        #  delims.pop()
        #  tokens.append([Lexer.Tokens.EMPH_CLOSE_DELIM, char])
        #  else:
        #  delims.append(Lexer.Tokens.EMPH_OPEN_DELIM)
        #  tokens.append([Lexer.Tokens.EMPH_OPEN_DELIM, char])
        #  tokens.append([Lexer.Tokens.WORD, str()])
        #  elif char == '_':
        #  if len(delims) > 0 and delims[-1] == Lexer.Tokens.ITAL_OPEN_DELIM:
        #  delims.pop()
        #  tokens.append([Lexer.Tokens.ITAL_CLOSE_DELIM, char])
        #  else:
        #  delims.append(Lexer.Tokens.ITAL_OPEN_DELIM)
        #  tokens.append([Lexer.Tokens.ITAL_OPEN_DELIM, char])
        #  tokens.append([Lexer.Tokens.WORD, str()])
        #  elif char == '<':
        #  delims.append(Lexer.Tokens.FUNCTION_OPEN_DELIM)
        #  tokens.append([Lexer.Tokens.FUNCTION_OPEN_DELIM, char])
        #  tokens.append([Lexer.Tokens.WORD, str()])
        #  elif char == '>' and len(delims) > 0 and delims[-1] == Lexer.Tokens.FUNCTION_OPEN_DELIM:
        #  delims.pop()
        #  tokens.append([Lexer.Tokens.FUNCTION_CLOSE_DELIM, char])
        #  tokens.append([Lexer.Tokens.WORD, str()])
        #  elif char == '$' and prev_char != '$':
        #  if len(delims) > 0 and (delims[-1] == Lexer.Tokens.MATH_INLINE_OPEN_DELIM or delims[-1] == Lexer.Tokens.MATH_OPEN_DELIM):
        #  delims.pop()
        #  tokens.append([Lexer.Tokens.MATH_INLINE_CLOSE_DELIM, char])
        #  else:
        #  delims.append(Lexer.Tokens.MATH_INLINE_OPEN_DELIM)
        #  tokens.append([Lexer.Tokens.MATH_INLINE_OPEN_DELIM, char])
        #  tokens.append([Lexer.Tokens.WORD, str()])
        #  elif char == '$' and prev_char == '$':
        #  if len(delims) > 0 and delims[-1] == Lexer.Tokens.MATH_INLINE_OPEN_DELIM:
        #  delims[-1] = Lexer.Tokens.MATH_OPEN_DELIM
        #  tokens[-1] = [Lexer.Tokens.MATH_OPEN_DELIM, '$$']
        #  else:
        #  tokens[-1] = [Lexer.Tokens.MATH_CLOSE_DELIM, '$$']
        #  tokens.append([Lexer.Tokens.WORD, str()])
        #  elif prev_char == '\n' and char =='\n':
        #  tokens.append([Lexer.Tokens.CLOSE_PARAGRAPH, str()])
        #  tokens.append([Lexer.Tokens.OPEN_PARAGRAPH, str()])
        #  tokens.append([Lexer.Tokens.WORD, str()])
        #  else:
        #  tokens.append([Lexer.Tokens.WORD, str()])
        #  elif escaped is True:
        #  escaped = False
        #  prev_char = char
        #  if tokens[-1][1] == str():
        #  tokens.pop()
        #  tokens.append([Lexer.Tokens.CLOSE_PARAGRAPH, str()])
        #  return tokens

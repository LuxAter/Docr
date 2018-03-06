from pprint import pprint
from enum import Enum
from structure import *


class Parser():
    def __init__(self):
        self.tu = None

    def parse_block(self, i, lines, delim, type, flags, meta_data=False):
        if lines[i].strip().startswith(delim) and not any(flags):
            elem = Element('', type)
            if meta_data is True or meta_data == 'str':
                elem.meta_data = [lines[i].strip()[len(delim):].strip()]
            elif meta_data == 'list':
                elem.meta_data = lines[i].strip()[len(delim):].strip().split()
            i+= 1
            while i < len(lines) and lines[i].strip().endswith(delim) is False:
                elem.data += lines[i]
                i += 1
            i += 1
            return i, [elem]
        return i, []

    def parse_element(self, element):
        if isinstance(element.data, list):
            print(element)
            for elem in element.data:
                self.parse_element(elem)
            return False
        in_element = Element(element.data, element.type, element.meta_data)
        string = element.data
        lines = string.splitlines()
        element.data = [Element('', Type.TEXT)]
        sub_elements = False
        special_par = False
        special_open = False
        indent_clear = 0
        for i, line in enumerate(lines):
            if special_par is False and line.strip() == str():
                if special_open is True and len(lines) > i + 1 and len(
                        lines[i + 1]) - len(
                            lines[i + 1].lstrip()) != indent_clear:
                    element.append(Element('', Type.TEXT))
                    indent_clear = 0
                    special_open = False
                    sub_elements = True
                elif special_open is False:
                    element.append(Element('', Type.TEXT))
                    indent_clear = 0
                    special_open = False
                    sub_elements = True
                else:
                    element.data[-1].data += "\n"

            else:
                print(self.parse_block(i, lines, '$$$', Type.MATH, [False], 'list'))
                print(self.parse_block(i, lines, '```', Type.CODE, [False], 'str'))
                if line.strip().startswith('$$$') and special_par is False:
                    special_par = True
                    element.data[-1].type = Type.MATH
                    element.data[-1].meta_data = line.strip()[3:].split()
                elif line.strip().endswith('$$$') and special_par is True:
                    special_par = False
                    element.append(Element('', Type.TEXT))
                elif line.strip().startswith('```') and special_par is False:
                    special_par = True
                    element.data[-1].type = Type.CODE
                    element.data[-1].meta_data = line.strip()[3:].split()
                elif line.strip().endswith('```') and special_par is True:
                    special_par = False
                elif line.strip().endswith(':') and special_par is False and special_open is False:
                    special_open = True
                    element.data[-1].type = Type.DEFINITION
                    element.data[-1].meta_data = [line.strip()[:-1]]
                elif line.strip().startswith('!!!') and special_par is False and special_open is False:
                    special_open = True
                    element.data[-1].type = Type.ADMONITON
                    element.data[-1].meta_data = [line.strip()[3:].strip()]
                else:
                    if (special_par is True or special_open is True) and bool(
                            element.data[-1].data) is False:
                        indent_clear = len(line) - len(line.lstrip())
                    element.data[-1].data += line[indent_clear:] + '\n'

        if len(element.data) == 1 and element.data[0] == in_element:
            element.data = in_element.data
            return False

        for elem in element.data:
            if elem.type not in (Type.MATH, Type.CODE):
                while self.parse_element(elem):
                    pass
        # print(element.print())
        return sub_elements

    # def parse_paragraph(self, string, indent=0):
    #     def check_par(par, type=None):
    #         par[0] = par[0].rstrip()
    #         if par[0] == str():
    #             return par
    #         if type is not None:
    #             par[1] = type
    #         elif par[0].lstrip().startswith('!!!'):
    #             par[1] = self.ParType.ADMONITON
    #         elif par[0].splitlines()[0].endswith(':'):
    #             par[1] = self.ParType.DEFINITION
    #         return par
    #     paragraphs = [self.Element()]
    #     special_par = None
    #     for line in string.splitlines():
    #         if indent == 0 and line.strip() == str() and special_par is None:
    #             paragraphs[-1] = check_par(paragraphs[-1])
    #             paragraphs.append(['', self.ParType.TEXT])
    #         elif len(line) - len(line.strip()) < indent and special_par is None:
    #             paragraphs[-1] = check_par(paragraphs[-1])
    #             paragraphs.append(['', self.ParType.TEXT])
    #         else:
    #             if special_par is not None:
    #                 if special_par[0] is self.ParType.CODE and line.rstrip().endswith('```'):
    #                     paragraphs[-1] = check_par(paragraphs[-1], special_par)
    #                     paragraphs.append(['', self.ParType.TEXT])
    #                     special_par = None
    #                 elif special_par[0] is self.ParType.MATH and line.rstrip().endswith('$$$'):
    #                     paragraphs[-1] = check_par(paragraphs[-1], special_par)
    #                     paragraphs.append(['', self.ParType.TEXT])
    #                     special_par = None
    #                 else:
    #                     paragraphs[-1][0] += line + '\n'
    #             else:
    #                 if line.lstrip().startswith('```') and special_par is None:
    #                     special_par = (self.ParType.CODE,line.strip().lstrip('```'))
    #                 elif line.lstrip().startswith('$$$') and special_par is None:
    #                     special_par = (self.ParType.MATH, None)
    #                 else:
    #                     paragraphs[-1][0] += line + '\n'
    #
    #     paragraphs = filter(lambda x: x[0] != str(), paragraphs)
    #     for par in paragraphs:
    #         print(par)
    #     return paragraphs
    #

    def parse(self, string):
        self.tu = Element(string, Type.TU)
        self.parse_element(self.tu)

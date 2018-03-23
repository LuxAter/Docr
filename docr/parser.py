from pprint import pprint
from enum import Enum
from structure import *


class Parser():
    def __init__(self):
        self.tu = None

    def parse_inline_block(self, delim, type, data):
        data_in = data[:]
        data_string = data[:]
        data = []
        counts = [data_string.count(x) for x in delim]
        while max(counts) >= 2:
            first = [
                data_string.find(x)
                if data_string.find(x) != -1 else len(data_string) + 1
                for x in delim
            ]
            first = min(first)
            c_delim = data_string[first]
            if len(data_string) > first + 1 and data_string[first
                                                            + 1] == c_delim:
                c_delim += c_delim
            pre = data_string[:first]
            con = data_string[first + len(c_delim):]
            data_string = con[con.find(c_delim) + len(c_delim):]
            con = con[:con.find(c_delim)]
            data.append(Element(pre, Type.TEXT))
            data.append(Element(con, type[delim.index(c_delim)]))
            counts = [data_string.count(x) for x in delim]
        data.append(Element(data_string, Type.TEXT))
        if data[0].data == data_in:
            return data_in
        return data

    def parse_block(self,
                    i,
                    lines,
                    delim,
                    type,
                    meta_data=False,
                    success=False):
        if lines[i].strip().startswith(delim):
            elem = Element('', type)
            if meta_data is True or meta_data == 'str':
                elem.meta_data = [lines[i].strip()[len(delim):].strip()]
            elif meta_data == 'list':
                elem.meta_data = lines[i].strip()[len(delim):].strip().split()
            i += 1
            while i < len(lines) and lines[i].strip().endswith(delim) is False:
                elem.data += lines[i] + '\n'
                i += 1
            i += 1
            return i, [elem], True
        return i, [], success

    def parse_front_block(self,
                          i,
                          lines,
                          delim,
                          type,
                          meta_data=False,
                          success=False):
        if lines[i].strip().startswith(delim):
            elem = Element('', type)
            if meta_data is True or meta_data == 'str':
                elem.meta_data = [lines[i].strip()[len(delim):].strip()]
            elif meta_data == 'list':
                elem.meta_data = lines[i].strip()[len(delim):].strip().split()
            i += 1
            indent_width = 0
            if i < len(lines):
                indent_width = len(lines[i]) - len(lines[i].lstrip())
            while i < len(lines) and (
                    len(lines[i]) - len(lines[i].lstrip()) >= indent_width
                    or lines[i].strip() == str()):
                elem.data += lines[i][indent_width:] + '\n'
                i += 1
            return i, [elem], True
        return i, [], success

    def parse_end_block(self,
                        i,
                        lines,
                        delim,
                        type,
                        meta_data=False,
                        success=False):
        if i >= len(lines):
            return i, [], success
        if lines[i].strip().endswith(delim):
            elem = Element('', type)
            if meta_data is True or meta_data == 'str':
                elem.meta_data = [lines[i].strip()[:-len(delim)].strip()]
            elif meta_data == 'list':
                elem.meta_data = lines[i].strip()[:-len(delim)].strip().split()
            i += 1
            indent_width = 0
            if i < len(lines):
                indent_width = len(lines[i]) - len(lines[i].lstrip())
            while i < len(lines) and (
                    len(lines[i]) - len(lines[i].lstrip()) >= indent_width
                    or lines[i].strip() == str()):
                elem.data += lines[i][indent_width:] + '\n'
                i += 1
            return i, [elem], True
        return i, [], success

    def parse_list_block(self, i, lines, success=False):
        if i >= len(lines):
            return i, [], success
        if lines[i].strip() == str():
            return i, [], success
        if lines[i].strip()[0] in ('-', '+',
                                   '*') and lines[i].strip()[1] == ' ':
            elem = Element('', Type.ITEM)
            elem.data = []
            depth = 0
            while i < len(lines) and (
                    lines[i].strip() == str() or lines[i][0] == ' ' or
                (lines[i][0] in ('-', '+', '*') and lines[i][1] == ' ')):
                if lines[i].strip() == str():
                    elem.data[-1].data += '\n'
                    i += 1
                    continue
                if lines[i][0] == ' ':
                    elem.data[-1].data += lines[i][depth:] + '\n'
                else:
                    if elem.data and elem.data[-1].data.endswith('\n\n'):
                        elem.data[-1].data = elem.data[-1].data[:-1]
                    depth = lines[i].find(' ') + 1
                    elem.append(
                        Element(lines[i][lines[i].find(' ') + 1:] + '\n',
                                Type.TEXT))
                i += 1
            if elem.data and elem.data[-1].data.endswith('\n\n'):
                elem.data[-1].data = elem.data[-1].data[:-1]
            return i, [elem], True
        elif 48 <= ord(lines[i][0]) <= 57 or 65 <= ord(
                lines[i][0]) <= 90 or 97 <= ord(lines[i][0]) <= 122:
            elem = Element(list(), Type.ENUM)
            if 48 <= ord(lines[i].strip()[0]) <= 57:
                elem.meta_data = ['arabic']
            elif lines[i].strip()[0] == 'i':
                elem.meta_data = ['roman']
            elif lines[i].strip()[0] == 'I':
                elem.meta_data = ['Roman']
            elif lines[i].strip()[0] == 'a':
                elem.meta_data = ['alpha']
            elif lines[i].strip()[0] == 'A':
                elem.meta_data = ['Alpha']
            else:
                return i, [], success
            if lines[i].strip()[1] in ('.', ')', ']'):
                elem.meta_data.append(lines[i].strip()[1])
            else:
                return i, [], success
            if lines[i].strip()[2] != ' ':
                return i, [], success
            while i < len(lines) and (lines[i].strip() == str()
                                      or lines[i][0] == ' ' or
                                      elem.meta_data[1] in lines[i].strip()):
                if lines[i].strip() == str():
                    elem.data[-1].data += '\n'
                    i += 1
                    continue
                if lines[i][0] == ' ':
                    elem.data[-1].data += lines[i].strip() + '\n'
                else:
                    if elem.data and elem.data[-1].data.endswith('\n\n'):
                        elem.data[-1].data = elem.data[-1].data[:-1]
                    elem.append(
                        Element(lines[i][lines[i].strip().find(
                            elem.meta_data[1]) + 2:] + '\n', Type.TEXT))
                i += 1
            if elem.data and elem.data[-1].data.endswith('\n\n'):
                elem.data[-1].data = elem.data[-1].data[:-1]
            return i, [elem], True
        return i, [], success

    def parse_element(self, element):
        if isinstance(element.data, list):
            # print(element)
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
        i = 0
        while i < len(lines):
            if lines[i].strip() == str():
                element.append(Element('', Type.TEXT))
                indent_clear = 0
                sub_elements = True

            else:
                i, res, suc = self.parse_block(i, lines, '$$$', Type.MATH,
                                               'list')
                element.cat(res)
                i, res, suc = self.parse_block(i, lines, '```', Type.CODE,
                                               'str', suc)
                element.cat(res)
                i, res, suc = self.parse_front_block(
                    i, lines, '!!!', Type.ADMONITON, 'str', suc)
                element.cat(res)
                i, res, suc = self.parse_end_block(i, lines, ':',
                                                   Type.DEFINITION, 'str', suc)
                element.cat(res)
                i, res, suc = self.parse_list_block(i, lines, suc)
                element.cat(res)
                if suc:
                    element.append(Element('', Type.TEXT))
                    i -= 1
                else:
                    element.data[-1].data += lines[i] + '\n'
            i += 1

        if len(element.data) == 1 and element.data[0] == in_element:
            element.data = in_element.data
            element.data = self.parse_inline_block(
                ['`', '$$', '$', '**', '__', '*', '_'], [
                    Type.INLINE_CODE, Type.MATH, Type.INLINE_MATH, Type.BOLD,
                    Type.BOLD, Type.ITALIC, Type.ITALIC
                ], element.data)
            return False

        for elem in element.data:
            if elem.type not in (Type.MATH, Type.CODE):
                while self.parse_element(elem):
                    pass
        return sub_elements

    def trim_element(self, elem, elem_up):
        if isinstance(elem.data, list):
            type = elem.type
            if elem_up:
                prev_type = elem_up.type
            else:
                prev_type = None
            for sub in elem.data:
                self.trim_element(sub, elem)
            if type == Type.TEXT and prev_type not in (Type.ITEM, Type.ENUM):
                index = elem_up.data.index(elem)
                elem_up.data = elem_up.data[:
                                            index] + elem.data + elem_up.data[index
                                                                              +
                                                                              1:]
        elif isinstance(elem.data, str) and elem.data == str():
            elem_up.data.remove(elem)


    def parse(self, string):
        self.tu = Element(string, Type.TU)
        self.parse_element(self.tu)
        self.trim_element(self.tu, None)

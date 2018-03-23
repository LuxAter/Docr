import os
import re
from structure import *

class Generator():
    def __init__(self):
        self.tu = None
        self.sections = dict()

    def parse_template_file(self, file):
        template_name = str()
        template = str()
        pat = re.compile('\[([a-z]|[A-Z]|[_ ])+\]')
        with open(file, 'r') as f:
            for line in f:
                if pat.match(line):
                    if template_name != str():
                        self.sections[template_name] = template[:-1]
                    template_name = line[1:-2]
                    template = str()
                else:
                    template += line
        self.sections[template_name] = template[:-1]
        print(self.sections)


    def parse_template_dir(self, dir):
        pass

    def load_templates(self, dir):
        if os.path.isfile(dir):
            self.parse_template_file(dir)
        elif os.path.isdir(dir):
            self.parse_template_dir(dir)
        else:
            print("INVALID TEMPLATE DIR {}".format(dir))

    def replace_template(self, template, element):
        data = {"%text%": element.data}
        if isinstance(element.meta_data, list):
            for i, entry in enumerate(element.meta_data):
                data["%" + str(i) + "%"] = entry
        else:
            data['%0%'] = element.meta_data
        pattern = re.compile('(' + '|'.join(data.keys()) + ')')
        # print(pattern)
        result = pattern.sub(lambda x: data[x.group()], template)
        # print(result)
        return result

    def generate_element(self, element):
        result = str()
        if isinstance(element.data, list):
            if element.type != Type.TU:
                data = str()
                for sub in element.data:
                    data += self.generate_element(sub)
                element.data = data
                result = self.replace_template(self.sections[str(element.type)[5:]], element)
            else:
                for sub in element.data:
                    result += self.generate_element(sub)
        elif isinstance(element.data, str):
            if str(element.type)[5:] in self.sections:
                result = self.replace_template(self.sections[str(element.type)[5:]], element)
            else:
                print("UNKNOWN TYPE {}".format(str(element.type)))
        return result


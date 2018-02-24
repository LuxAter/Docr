#  from parser.Parser import Object

class Generator(object):

    def __init__(self):
        self.output_format = "NULL"
        self.data = dict()

    def __repr__(self):
        return "<" + self.output_format + " Generator>"

    def get_delim(self, delim):
        if delim in self.data:
            return self.data[delim]
        else:
            return "{" + delim + "}"

    def gen_object_entry(self, obj):
        print(self.get_delim(str(obj.token) + " Open"), end='')
        for sub in obj.data:
            if isinstance(sub, str):
                print("[" + sub + "]", end='')
            else:
                self.gen_object_entry(sub)
        print(self.get_delim(str(obj.token) + " Close"))


    def gen_file(self, obj_list):
        for obj in obj_list:
            self.gen_object_entry(obj)

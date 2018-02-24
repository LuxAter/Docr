import generators.base

class Generator(generators.base.Generator):

    def __init__(self):
        self.output_format = "HTML"
        self.data = dict()

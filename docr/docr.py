from parser import Parser
from generator import Generator

def main():
    parser = Parser()
    gen = Generator()
    # with open("test.emd") as file:
    #     txt = file.read()
    # parser.parse(txt)
    with open("small.emd") as file:
        txt = file.read()
    parser.parse(txt)
    print(parser.tu.print())
    gen.load_templates("templates/markdown.md")
    res = gen.generate_element(parser.tu)
    print(res)


if __name__ == "__main__":
    main()

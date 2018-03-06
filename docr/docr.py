from parser import Parser

def main():
    parser = Parser()
    with open("test.emd") as file:
        txt = file.read()
    parser.parse(txt)
    # with open("small.emd") as file:
    #     txt = file.read()
    # parser.parse(txt)
    print(parser.tu.print())

if __name__ == "__main__":
    main()

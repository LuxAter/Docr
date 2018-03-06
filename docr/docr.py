from parser import Parser

def main():
    parser = Parser()
    with open("test.emd") as file:
        txt = file.read()
    parser.parse(txt)

if __name__ == "__main__":
    main()

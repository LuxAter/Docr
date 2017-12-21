"""
Docr markup parsing module.
"""

from syntaxtree import SyntaxTree

class Parser(object):
    """Parses Docr markup formatted files, and generates the AST representing the data in the file(s) provided by the user."""

    def __init__(self):
        pass

    def parse_attributes(self, word):
        attrs = list()
        if word.startswith('`'):
            word = word[1:]
            attrs.append(SyntaxTree.Attrs.CODE)
        return attrs


    def parse_paragraph(self, paragraph):
        tree = SyntaxTree(SyntaxTree.Tokens.PARAGRAPH)
        tree.lexmes.append(SyntaxTree(SyntaxTree.Tokens.TEXT))
        for word in paragraph.split(' '):
            attrs = self.parse_attributes(word)
            if attrs != tree.lexmes[-1].attributes:
                tree.lexmes.append(SyntaxTree(SyntaxTree.Tokens.TEXT))
                tree.lexmes[-1].attributes = attrs
            tree.lexmes[-1].text += word + ' '
        tree.lexmes[-1].text = tree.lexmes[-1].text.rstrip()
        return tree


    def read_file(self, filepath):
        paragraphs = [str()]
        with open(filepath, 'r') as file:
            for line in file:
                if line == '\n':
                    paragraphs[-1] = paragraphs[-1].rstrip()
                    paragraphs.append(str())
                else:
                    paragraphs[-1] += line.rstrip() + ' '
        paragraphs[-1] = paragraphs[-1].rstrip()
        return self.parse_paragraph(paragraphs[0])



import syntaxtree as st
from parser import Parser
from lexer import Lexer


def pfile(mytree):
    print("""

<head>
<script type="text/javascript" async
  src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.2/MathJax.js?config=TeX-MML-AM_CHTML">
</script>
<script type="text/x-mathjax-config">
  MathJax.Hub.Config({
    tex2jax: {inlineMath: [["$","$"],["\(","\)"]]}
  });
</script>
</head>""")
    for lexme in mytree:
        if lexme[0] == Lexer.Tokens.OPEN_PARAGRAPH:
            print("<p>", end='')
        elif lexme[0] == Lexer.Tokens.CLOSE_PARAGRAPH:
            print("</p>")
        elif lexme[0] == Lexer.Tokens.WORD:
            print(lexme[1], end=' ')
        elif lexme[0] == Lexer.Tokens.CODE_OPEN_DELIM:
            print("<code>", end='')
        elif lexme[0] == Lexer.Tokens.CODE_CLOSE_DELIM:
            print("</code>", end='')
        elif lexme[0] == Lexer.Tokens.EMPH_OPEN_DELIM:
            print("<strong>", end='')
        elif lexme[0] == Lexer.Tokens.EMPH_CLOSE_DELIM:
            print("</strong>", end='')
        elif lexme[0] == Lexer.Tokens.ITAL_OPEN_DELIM:
            print("<em>", end='')
        elif lexme[0] == Lexer.Tokens.ITAL_CLOSE_DELIM:
            print("</em>", end='')
        elif lexme[0] == Lexer.Tokens.MATH_INLINE_OPEN_DELIM:
            print("$", end='')
        elif lexme[0] == Lexer.Tokens.MATH_INLINE_CLOSE_DELIM:
            print("$", end='')
        elif lexme[0] == Lexer.Tokens.MATH_OPEN_DELIM:
            print("\[", end='')
        elif lexme[0] == Lexer.Tokens.MATH_CLOSE_DELIM:
            print("\]", end='')
        elif lexme[0] == Lexer.Tokens.UNICODE:
            print("&#{};".format(int(lexme[1], 16)), end=' ')


def main():
    mytree = Lexer.analyze("test.doc")
    from pprint import pprint
    pprint(mytree)
    #  pfile(mytree)



if __name__ == "__main__":
    main()

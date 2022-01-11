"""
Module that lists out all lex tokens.
Modify this file if you want to add more tokens, which can be accomplished by:

If the token you're going to add is a syntactically valid identifier:
    add it into the `reserved` dictionary, where key is the token itself and value is token name.
Else:
    makes it into a global variable or function that starts with "t_" and the following the name of your token.

Refer to https://www.dabeaz.com/ply/ply.html for more details.
"""

# Reserved keywords
reserved = {
    "return": "Return",
    "int": "Int",
    "if": "If",
    "else": "Else",
    "while": "While",
    "break": "Break",
    # step-8
    "for": "For",
    "do": "Do",
    "continue": "Continue",
}

t_Semi = ";"
# step-9
t_Comma = ","

t_LParen = "("
t_RParen = ")"
t_LBracket = "["
t_RBracket = "]"
t_LBrace = "{"
t_RBrace = "}"

t_Colon = ":"
t_Question = "?"

t_Plus = "+"
t_Minus = "-"
t_Mul = "*"
t_Div = "/"
t_Mod = "%"
t_Not = "!"
t_BitNot = "~"
t_And = "&&"
t_BitAnd = "&"
t_Or = "||"
t_BitOr = "|"
t_Xor = "^"
t_Equal = "=="
t_NotEqual = "!="
t_Less = "<"
t_LessEqual = "<="
t_Greater = ">"
t_GreaterEqual = ">="
t_Assign = "="


def t_Integer(t):
    r"[0-9]+"  # can be accessed from `t_Interger.__doc__`
    t.value = int(t.value)
    return t


def t_Identifier(t):
    r"[a-zA-Z_][0-9a-zA-Z_]*"
    t.type = reserved.get(t.value, "Identifier")
    return t


# String patterns that should be ignored by the lexer.
t_ignore_Newline = r"(?:\r\n?|\n)"

t_ignore_Whitespace = r"[ \t]+"
t_ignore_LineComment = rf"//.*?(?={t_ignore_Newline})"

# Collection of all tokens.
tokens = tuple(
    name.removeprefix("t_")
    for name in globals()
    if name.startswith("t_") and not name.startswith("t_ignore_")
) + tuple(reserved.values())


def _escape():
    "Don't care about this"

    import re

    token_dict = globals()
    for name in tokens:
        name = f"t_{name}"
        original = token_dict.get(name, name)
        if isinstance(original, str):
            token_dict[name] = re.escape(original)


_escape()

"""
Module that defines a parser using `ply.yacc`.
Add your own parser rules on demand, which can be accomplished by:

1. Define a global function whose name starts with "p_".
2. Write the corresponding grammar rule(s) in its docstring.
3. Complete the function body, which is actually a syntax base translation process.
    We're using this technique to build up the AST.

Refer to https://www.dabeaz.com/ply/ply.html for more details.
"""

import ply.yacc as yacc

from frontend.ast.tree import *
from frontend.lexer import lex
from utils.error import DecafSyntaxError

tokens = lex.tokens
error_stack = list[DecafSyntaxError]()


def p_program_component(p):
    """
    program_component : function
    program_component : declaration Semi
    """
    p[0] = [p[1]]


def p_program_component_many(p):
    """
    program_component : program_component program_component
    """
    if p[2] is not NULL:
        p[1] += p[2]
    p[0] = p[1]


def unary(p):
    p[0] = Unary(UnaryOp.backward_search(p[1]), p[2])


def binary(p):
    p[0] = Binary(BinaryOp.backward_search(p[2]), p[1], p[3])


def p_empty(p: yacc.YaccProduction):
    """
    empty :
    """
    pass


def p_program(p):
    """
    program : program_component
    """
    p[0] = Program(p[1])


def p_type(p):
    """
    type : Int
    """
    p[0] = TInt()


# step-9
def p_function_def(p):
    """
    function : type Identifier LParen Parameter RParen LBrace block RBrace
    """
    p[0] = Function(p[1], p[2], p[7], p[4])


def p_block(p):
    """
    block : block block_item
    """
    if p[2] is not NULL:
        p[1].children.append(p[2])
    p[0] = p[1]


def p_block_empty(p):
    """
    block : empty
    """
    p[0] = Block()


def p_block_item(p):
    """
    block_item : statement
        | declaration Semi
    """
    p[0] = p[1]


def p_statement(p):
    """
    statement : statement_matched
        | statement_unmatched
    """
    p[0] = p[1]


def p_if_else(p):
    """
    statement_matched : If LParen expression RParen statement_matched Else statement_matched
    statement_unmatched : If LParen expression RParen statement_matched Else statement_unmatched
    """
    p[0] = If(p[3], p[5], p[7])


def p_if(p):
    """
    statement_unmatched : If LParen expression RParen statement
    """
    p[0] = If(p[3], p[5])


def p_while(p):
    """
    statement_matched : While LParen expression RParen statement_matched
    statement_unmatched : While LParen expression RParen statement_unmatched
    """
    p[0] = While(p[3], p[5])


# step-8 add p_for, p_dowhile

def p_for(p):
    """
    statement_matched : For LParen opt_expression Semi opt_expression Semi opt_expression RParen statement_matched
    statement_matched : For LParen declaration Semi opt_expression Semi opt_expression RParen statement_matched
    statement_unmatched : For LParen opt_expression Semi opt_expression Semi opt_expression RParen statement_unmatched
    statement_unmatched : For LParen declaration Semi opt_expression Semi opt_expression RParen statement_unmatched
    """
    p[0] = For(p[3], p[5], p[7], p[9])


def p_dowhile(p):
    """
    statement_matched : Do statement_matched While LParen expression RParen Semi
    statement_unmatched : Do statement_unmatched While LParen expression RParen Semi
    """
    p[0] = DoWhile(p[2], p[5])


def p_return(p):
    """
    statement_matched : Return expression Semi
    """
    p[0] = Return(p[2])


def p_expression_statement(p):
    """
    statement_matched : opt_expression Semi
    """
    p[0] = p[1]


def p_block_statement(p):
    """
    statement_matched : LBrace block RBrace
    """
    p[0] = p[2]


def p_break(p):
    """
    statement_matched : Break Semi
    """
    p[0] = Break()


def p_continue(p):
    """
    statement_matched : Continue Semi
    """
    p[0] = Continue()


def p_opt_expression(p):
    """
    opt_expression : expression
    """
    p[0] = p[1]


def p_opt_expression_empty(p):
    """
    opt_expression : empty
    """
    p[0] = NULL


def p_declaration(p):
    """
    declaration : type Identifier
    """
    p[0] = Declaration(p[1], p[2])


def p_declaration_init(p):
    """
    declaration : type Identifier Assign expression
    """
    p[0] = Declaration(p[1], p[2], p[4])


def p_array_dim_list(p):
    """
    arr_dim_list : LBracket Integer RBracket arr_dim_list
    """
    p[0] = [p[2].value] + p[4]


def p_array_dim_list_one(p):
    """
    arr_dim_list : LBracket Integer RBracket
    """
    p[0] = [p[2].value]


def p_array_declaration(p):
    """
    declaration : type Identifier arr_dim_list
    """
    p[0] = Declaration(TArray(p[1].type, p[3]), p[2], None)


def p_call(p):
    """
    postfix : Identifier LParen call_para RParen
    """
    p[0] = FuncCall(p[1], p[3])


def p_call_para(p):
    """
    call_para : expression
    """
    p[0] = [p[1]]


def p_call_para_is_empty(p):
    """
    call_para : empty
    """
    p[0] = []


def p_call_para_many(p):
    """
    call_para : call_para Comma call_para
    """
    if p[3] is not NULL:
        p[1] += p[3]
    p[0] = p[1]


def p_parameter(p):
    """
    Parameter : type Identifier
    """
    p[0] = [Parameter(p[1], p[2])]


def p_parameter_many(p):
    """
    Parameter : Parameter Comma Parameter
    """
    if p[3] is not NULL:
        p[1] += p[3]
    p[0] = p[1]


def p_parameter_is_empty(p):
    """
    Parameter : empty
    """
    p[0] = []


def p_expression_precedence(p):
    """
    expression : assignment
    assignment : conditional
    conditional : logical_or
    logical_or : logical_and
    logical_and : bit_or
    bit_or : xor
    xor : bit_and
    bit_and : equality
    equality : relational
    relational : additive
    additive : multiplicative
    multiplicative : unary
    unary : postfix
    postfix : primary
    """
    p[0] = p[1]


def p_unary_expression(p):
    """
    unary : Minus unary
        | BitNot unary
        | Not unary
    """
    unary(p)


def p_array_idx_list(p):
    """
    arr_idx_list : LBracket expression RBracket arr_idx_list
    """
    p[0] = [p[2]] + p[4]


def p_array_idx_list_one(p):
    """
    arr_idx_list : LBracket expression RBracket
    """
    p[0] = [p[2]]


def p_array_ref(p):
    """
    arr_ref : Identifier arr_idx_list
    """
    p[0] = ArrayRef(p[1].value, p[2])


def p_assignment(p):
    """
    assignment : Identifier Assign expression
    assignment : arr_ref Assign expression
    """
    p[0] = Assignment(p[1], p[3])


def p_binary_expression(p):
    """
    logical_or : logical_or Or logical_and
    logical_and : logical_and And bit_or
    bit_or : bit_or BitOr xor
    xor : xor Xor bit_and
    bit_and : bit_and BitAnd equality
    equality : equality NotEqual relational
        | equality Equal relational
    relational : relational Less additive
        | relational Greater additive
        | relational LessEqual additive
        | relational GreaterEqual additive
    additive : additive Plus multiplicative
        | additive Minus multiplicative
    multiplicative : multiplicative Mul unary
        | multiplicative Div unary
        | multiplicative Mod unary
    """
    binary(p)


def p_conditional_expression(p):
    """
    conditional : logical_or Question expression Colon conditional
    """
    p[0] = ConditionExpression(p[1], p[3], p[5])


def p_int_literal_expression(p):
    """
    primary : Integer
    """
    p[0] = p[1]


def p_identifier_expression(p):
    """
    primary : Identifier
    """
    p[0] = p[1]


def p_brace_expression(p):
    """
    primary : LParen expression RParen
    """
    p[0] = p[2]


def p_array_expression(p):
    """
    primary : arr_ref
    """
    p[0] = ArrayExpr(p[1])


def p_error(t):
    """
    A naive (and possibly erroneous) implementation of error recovering.
    """
    if not t:
        error_stack.append(DecafSyntaxError(t, "EOF"))
        return

    inp = t.lexer.lexdata
    error_stack.append(DecafSyntaxError(t, f"\n{inp.splitlines()[t.lineno - 1]}"))

    parser.errok()
    return parser.token()


parser = yacc.yacc(start="program")
parser.error_stack = error_stack  # type: ignore

# eval_arith.py
#
# Copyright 2009, 2011 Paul McGuire
#
# Expansion on the pyparsing example simpleArith.py, to include evaluation
# of the parsed tokens.
#
# Added support for exponentiation, using right-to-left evaluation of
# operands
#
from pyparsing import Word, nums, alphas, Combine, oneOf, \
    opAssoc, infixNotation, Literal, Group, \
    ZeroOrMore, Forward, alphas, alphanums, Regex, ParseException, \
    CaselessKeyword, Suppress, printables
import math
import operator

exprStack = []
def pushFirst(strg, loc, toks):
    exprStack.append(toks[0])


def pushUMinus(strg, loc, toks):
    for t in toks:
        if t == '-':
            exprStack.append('unary -')
            # ~ exprStack.append( '-1' )
            # ~ exprStack.append( '*' )
        else:
            break


bnf = None


def BNF():
    """
    * means repeat 0-n times
    + means repeat 1-n times


    logicalExpression        :: booleanAndExpression ( OR booleanAndExpression )*
    booleanAndExpression     :: equalityExpression ( AND equalityExpression )*
    equalityExpression       :: relationalExpression ( (EQ|NEQ) relationalExpression )*
    relationalExpression     :: functionalExpression ( (LT|LE|GT|GE) functionalExpression )*
    functionalExpression     :: additiveExpression( function '(' additiveExpression ')' )*
    additiveExpression       :: multiplicativeExpression ( (PLUS|MINUS) multiplicativeExpression )*
    multiplicativeExpression :: unaryExpression ((MULT|DIV|MOD) unaryExpression )*
    unaryExpression          :: NOT primaryExpression
    primaryExpression        :: '(' logicalExpression ')' | value

    function :: abs | trunc | round | sgn
    OR    :: '||' | 'or';
    AND   :: '&&' | 'and';
    EQ    :: '=' | '==';
    NEQ   :: '!=' | '<>';
    LT    :: '<' | 'lt';
    LE    :: '<=' | 'le';
    GT    :: '>' | 'gt';
    GE    :: '>=' | 'ge';
    PLUS  :: '+';
    MINUS :: '-';
    MULT  :: '*';
    DIV   :: '/';
    MOD   :: '%';
    NOT   :: '!' | 'not';

    value   :: number | STRING | DATETIME | BOOLEAN
    number   :: '-'? ('0'..'9')* ('.' ('0'..'9')*)+
    STRING  :: '\'' (~ '\'' )* '\''
    BOOLEAN :: 'true' | 'false'

    """

    global bnf
    if not bnf:
        # ~ Optional( point + Optional( Word( nums ) ) ) +
        # ~ Optional( e + Word( "+-"+nums, nums ) ) )
        # fnumber = Regex(r"[+-]?\d+(?:\.\d*)?")
        fnumber = Regex(r"[+-]?\d+(?:\.\d*)?")
        ident = Word(alphas, alphanums + "_$")

        plus, minus, mult, div = map(Literal, "+-*/")
        _and, _or = map(Literal, ("AND", "OR"))
        _text = Word('"' + alphanums + '"')
        logic_op = _and | _or
        lt, gt, ne, ge, le, eq = map(Literal, ("<", ">", "!=", "GE", "LE", "="))
        comp_op = lt | gt | ne | ge | le | eq
        lpar, rpar = map(Suppress, "()")
        addop = plus | minus
        multop = mult | div
        expop = Literal("^")

        expr = Forward()
        primaryExpression = ((0, None) * minus + (fnumber | ident + lpar + expr + rpar | _text).setParseAction(pushFirst) |
                             Group(lpar + expr + rpar)).setParseAction(pushUMinus)

        # by defining exponentiation as "atom [ ^ factor ]..." instead of "atom [ ^ atom ]...", we get right-to-left
        # exponents, instead of left-to-right that is, 2^3^2 = 2^(3^2), not (2^3)^2
        factor = Forward()
        factor << primaryExpression + ZeroOrMore((expop + factor).setParseAction(pushFirst))
        term = factor + ZeroOrMore((multop + factor).setParseAction(pushFirst))
        addexpr = term + ZeroOrMore((addop + term).setParseAction(pushFirst))
        logicexpr = addexpr + ZeroOrMore((comp_op + addexpr).setParseAction(pushFirst))
        expr << logicexpr + ZeroOrMore((logic_op + logicexpr).setParseAction(pushFirst))
        bnf = expr

    return bnf


# map operator symbols to corresponding arithmetic operations
opn = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": operator.truediv,
    "^": operator.pow}

epsilon = 1e-12
fn = {
    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,
    "exp": math.exp,
    "abs": abs,
    "trunc": lambda a: int(a),
    "round": round,
    "sgn": lambda a: (a > epsilon) - (a < -epsilon)}

compop = {
    "<": lambda a, b: a < b,
    ">": lambda a, b: a > b,
    "=": lambda a, b: a == b,
    "LE": lambda a, b: a <= b,
    "GE": lambda a, b: a >= b,
    "!=": lambda a, b: a != b}

logop = {
    "AND": lambda a, b: a and b,
    "OR": lambda a, b: a or b}

def evaluateStack(s):
    op = s.pop()
    # print(op)
    if op == 'unary -':
        return -evaluateStack(s)
    if op in opn:
        op2 = evaluateStack(s)
        op1 = evaluateStack(s)
        # print(op1, op2)
        return opn[op](op1, op2)
    elif op in fn:
        return fn[op](evaluateStack(s))
    elif op in compop:
        op2 = evaluateStack(s)
        op1 = evaluateStack(s)
        # print(op1, op2)
        return compop[op](op1, op2)
    elif op in logop:
        op2 = evaluateStack(s)
        op1 = evaluateStack(s)
        # print(op1, op2)
        return logop[op](op1, op2)
    elif op[0].isalpha():
        raise Exception("invalid identifier '%s'" % op)
        #return str(op)
    elif not op.isnumeric():
        return op
    else:
        return float(op)


def main():
    print("Start")


def test(s, expVal):
    s = s.replace("<=", "LE")
    s = s.replace(">=", "GE")

    global exprStack
    exprStack[:] = []
    try:
        results = BNF().parseString(s, parseAll=True)
        val = evaluateStack(exprStack[:])
    except ParseException as pe:
        print(s, "failed parse:", str(pe))
    except Exception as e:
        print(s, "failed eval:", str(e))
    else:
        if val == expVal:
            print("PASS:", s, " =>", val, "     Parsed results =>", results, " Expression stack =>", exprStack)
        else:
            print("FAIL:", s +
                  " =>", val, " Expected =>", expVal,
                  "     Parsed results => ", results, "=>", " Expression stack =>", exprStack)
            print(results)
            print(val)

# TEXT responses HAVE to be surrounded with double quotes. i.e. " "
# EACH parameter in a validation rule has to specify a default value if a blank is found
# EACH primary question needs to specify what to default the question value to
#   e.g. Value present will default
if __name__ == '__main__':
    main()
    test("1", 1)
    test("2*3*4", 24)
    test("4+5", 9)
    test("2^2+2", 6)
    test("2+2^2", 6)
    test("2 >= 2", True)
    test("1 < 2", True)
    test("3.01 <= 3.02", True)
    test("3.01 != 3.02", True)
    test("1 < 2 AND 4 > 3", True)
    test("2 < 2 AND 4 > 3", False)
    test("2 < 2 OR 4 > 3", True)
    test("(2 < 2) OR (4 > 3) OR (1=1)", True)
    test("abs(-10+5)", 5)
    test("(abs(25)>0 AND 0=0) OR (abs(0)>0 AND 25=0) AND abs(0-25)>15", True)
    test("(abs(25)>0 AND 0=0) OR (abs(0)>0 AND 25=0) AND abs(0-25)>25", False)
    test("\"test\"=\"test\"", True)
    test("\"toast\"=\"\"", False)
    test("\"\"=\"\"", True)
    test("432=\"\"", False)
    test("\"1234\"!=\"\" AND 1234!=0", True)
    test("\"\"!=\"\" OR 0=0", True)
    test("1234!=\"1234\" AND 1234!=0", True)
    test("1234!=\"1234\"", True)
    # test("47>4", True)
    # test("2>4", False)
    # test("-5 > -5.01", True)
    # test("-6 > -5", False)
    # test("0 = 0", True)
    # test("5>=5", True)
    # test("5<=5", True)
    # test("1!=2", True)
    # test("abs(-10)", 10)
    # test("abs(-10+5)", 5)
    # test("(9+1+5)=10", True)
    # test("(9+1+5)", True)
    # test("0!=\"\"", True)
    # test("(1!=2)", True)
    # test("(1!=2) AND (3=4)", True)


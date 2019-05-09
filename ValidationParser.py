from pyparsing import Word, Literal, Group, ZeroOrMore, Forward, alphas, alphanums, Regex, ParseException, \
    CaselessKeyword, Suppress, delimitedList
from ValidationParserStack import ValidationParserStack


class ValidationParser(object):

    def push_first(self, strg, loc, toks):
        self.exprStack.append(toks[0])

    def push_unary_minus(self, strg, loc, toks):
        for t in toks:
            if t == '-':
                self.exprStack.append('unary -')
            else:
                break

    def __init__(self):
        self.exprStack = []
        self.bnf = self.define_syntax()

    def define_syntax(self):
        fnumber = Regex(r'[+-]?\d+\.\d*([eE][+-]?\d+)?').setParseAction(lambda t: float(t[0]))
        ident = Word(alphas, alphanums + "_$")

        expop, plus, minus, mult, div = map(Literal, "^+-*/")
        lt, gt, ne, ge, le, eq, _in, _nin = map(Literal, ("<", ">", "!=", "GE", "LE", "=", "IN", "NOTIN"))

        custom_alphanums = alphanums + "." + "_"
        _text = Word('"' + custom_alphanums + '"')
        logic_op = CaselessKeyword("AND") | CaselessKeyword("OR")

        comp_op = lt | gt | ne | ge | le | eq | _in | _nin
        lpar, rpar = map(Suppress, "()")
        addop = plus | minus
        multop = mult | div

        _list = Suppress('[') + delimitedList(_text, combine=True) + Suppress(']')
        # searchList = Combine(_text + "IN [" + _list + "]")
        expr = Forward()
        primary_expression = (
                (0, None) * minus + (_list | fnumber | ident + lpar + expr + rpar | _text).setParseAction(self.push_first) |
                Group(lpar + expr + rpar)).setParseAction(self.push_unary_minus)

        # by defining exponentiation as "atom [ ^ factor ]..." instead of "atom [ ^ atom ]...", we get right-to-left
        # exponents, instead of left-to-right that is, 2^3^2 = 2^(3^2), not (2^3)^2
        factor = Forward()
        factor << primary_expression + ZeroOrMore((expop + factor).setParseAction(self.push_first))
        term = factor + ZeroOrMore((multop + factor).setParseAction(self.push_first))
        addexpr = term + ZeroOrMore((addop + term).setParseAction(self.push_first))
        logicexpr = addexpr + ZeroOrMore((comp_op + addexpr).setParseAction(self.push_first))
        expr << logicexpr + ZeroOrMore((logic_op + logicexpr).setParseAction(self.push_first))
        return expr

    def evaluate(self, formula):
        formula = formula.replace("<=", "LE")
        formula = formula.replace(">=", "GE")
        self.exprStack = []
        self.results = self.bnf.parseString(formula, True)
        stack = ValidationParserStack()
        return stack.evaluate(self.exprStack[:])

    def safe_evaluate(self, formula):
        try:
            output = self.evaluate(formula)
        except ParseException as pe:
            return None
        except Exception as e:
            return None
        return output

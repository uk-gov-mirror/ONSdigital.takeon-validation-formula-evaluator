import time
from ValidationParser import ValidationParser


def test(formula, expected):
    p = ValidationParser()
    output = p.safe_evaluate(formula)
    if output == expected:
        print("PASS:", formula, "=>", output)
    else:
        print("FAIL:", formula +
              "=>", output, " Expected =>", expected,
              "     Parsed results => ", p.results, "=>", " Expression stack =>", p.exprStack)


# TEXT responses HAVE to be surrounded with double quotes. i.e. " "
# EACH parameter in a validation rule has to specify a default value if a blank is found
# EACH primary question needs to specify what to default the question value to
#   e.g. Value present will default formula to ""
if __name__ == '__main__':
    start = time.time()
    print("Value Present: ")
    test("\"3.14\"!=\"\"", True)
    test("\"test\"=\"test\"", True)
    test("\"toast\"=\"\"", False)
    test("\"\"=\"\"", True)
    test("432=\"\"", False)
    print()

    print("Zero Continuity: ")
    test("(abs(25)>0 AND 0=0) OR (abs(0)>0 AND 25=0) AND abs(0-25)>15", True)
    test("(abs(25)>0 AND 0=0) OR (abs(0)>0 AND 25=0) AND abs(0-25)>25", False)
    test("(abs(0)>0 AND 0=0) OR (abs(0)>0 AND 0=0) AND abs(0-0)>0", False)
    test("(abs(100)>0 AND 50=0) OR (abs(50)>0 AND 100=0) AND abs(100-50)>0", False)
    print()

    print("Large Value: ")
    test("2 >= 2", True)
    test("100 >= 5", True)
    test("\"zorro\" >= \"alpha\"", True)
    print()

    print("Question v Derived Question:   i.e. <value> <operator> <value>")
    test("\"banana\" <= \"yoghurt\"", True)
    test("1234!=\"1234\"", True)
    test("1 < 2", True)
    test("1.01 < 1", False)
    test("3.01 <= 3.02", True)
    test("3.01 != 3.02", True)
    print()

    print("Value Present with SIC:")
    test("\"1.2\" != \"\" AND \"90101\" IN [\"12345\",\"90101\",\"34545\"]", True)
    test("\"\" != \"\" AND \"90101\" IN [\"12345\",\"90101\",\"34545\"]", False)
    test("245 != \"\" AND \"90105\" IN [\"12345\",\"90101\",\"34545\"]", False)
    print()

    print("Value Present excluding SIC:")
    test("\"1.2\" != \"\" AND \"90101\" NOTIN [\"12345\",\"90101\",\"34545\"]", False)
    test("\"\" != \"\" AND \"90101\" NOTIN [\"12345\",\"90101\",\"34545\"]", False)
    test("245 != \"\" AND \"90105\" NOTIN [\"12345\",\"90101\",\"34545\"]", True)
    print()

    print("Compulsory Value:")  # Note, the wrangler will have to dummy a sentinel value for text fields
    test("abs(0.00) < 0.001 OR \"0.00\"=\"\"", True)
    test("abs(0) < 0.001 OR \"0\"=\"\"", True)
    test("abs(999) < 0.001 OR \"toast\"=\"\"", False)
    test("abs(760.23) < 0.001 OR \"760.23\"=\"\"", False)
    print()

    print('Period on period movement:')
    print()

    print('NonResponder in Previous Period - DQ v Threshold (POPDT):')
    test("(\"responded\" != \"non_responder\") AND ((45/123)>2) AND (123>100)", False)
    test("(\"non_responder\" != \"non_responder\") AND ((45/123)<2) AND (123>100)", False)
    test("(\"responded\" != \"non_responder\") AND ((45/123)<2) AND (123>100)", True)
    print()

    print('NonResponder in Previous Period - Now Zero (POPNZ):')
    test("(\"responded\" = \"non_responder\") AND (0=0)", False)
    test("(\"non_responder\" = \"non_responder\") AND (0=0)", True)
    print()

    print("General: ")
    test("1", 1)
    test("\"test\"", "\"test\"")
    test("2*3*4", 24)
    test("4+5", 9)
    test("2^2+2", 6)
    test("2+2^2", 6)
    test("2+2*2+2", 8)
    test("exp(sin(0))", 1)
    test("1 < 2 AND 4 > 3", True)
    test("2 < 2 AND 4 > 3", False)
    test("2 < 2 OR 4 > 3", True)
    test("(2 < 2) OR (4 > 3) OR (1=1)", True)
    test("abs(-10+5)", 5)
    test("\"1234\"!=\"\" AND 1234!=0", True)
    test("\"\"!=\"\" OR 0=0", True)
    test("1234!=\"1234\" AND 1234!=0", True)
    test("1 IN [1]", True)
    test("\"a\" IN [\"a\"]", True)
    test("1 IN [3,1,2,4,7]", True)
    test("1 IN [2,3,4]", False)
    test("\"house\" IN [\"bucket\",\"cheese\",\"house\",\"moose\"]", True)
    test("\"parsley\" IN [1,2,3,4]", False)

    finish = time.time()
    print(finish-start)








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



#p.evaluate()
#p.evaluate("1 = 1")
#p.evaluate("1 + 2 = 6")
#p.evaluate("exp(2) < 10")
#p.evaluate("exp(sin(0))")
#p.evaluate("1 IN 1")
# p.eval("sin(0)=0")
# p.eval("34 > 19 AND 21134 IN ('12321'....'')")

from ValidationParser import ValidationParser
import pytest

def validationparsing(formula):
    p = ValidationParser()
    output = p.safe_evaluate(formula)
    return output

testData = [
    # value present
    ('"3.14"!=""', True),
    ('"test"="test"', True),
    ('"toast"=""', False),
    ('""=""', True),
    ('432=""', False),
    # zero continuity
    ("(abs(25)>0 AND 0=0) OR (abs(0)>0 AND 25=0) AND abs(0-25)>15", True),
    ("(abs(25)>0 AND 0=0) OR (abs(0)>0 AND 25=0) AND abs(0-25)>25", False),
    ("(abs(0)>0 AND 0=0) OR (abs(0)>0 AND 0=0) AND abs(0-0)>0", False),
    ("(abs(100)>0 AND 50=0) OR (abs(50)>0 AND 100=0) AND abs(100-50)>0", False),
    # large values
    ("2 >= 2", True),
    ("100 >= 5", True),
    ('"zorro" >= "alpha"',True),
    # question vs derived question
    ('"banana" <= "yoghurt"', True),
    ('1234!="1234"', True),
    ("1 < 2", True),
    ("1.01 < 1", False),
    ("3.01 <= 3.02", True),
    ("3.01 != 3.02", True),
    # value present with SIC
    ('"1.2" != "" AND "90101" IN ["12345","90101","34545"]', True),
    ('"" != "" AND "90101" IN ["12345","90101","34545"]', False),
    ('245 != "" AND "90105" IN ["12345","90101","34545"]', False),
    # value present without SIC
    ('"1.2" != "" AND "90101" NOTIN ["12345","90101","34545"]', False),
    ('"" != "" AND "90101" NOTIN ["12345","90101","34545"]', False),
    ('245 != "" AND "90105" NOTIN ["12345","90101","34545"]', True),
    # compulsory value
    ('abs(0.00) < 0.001 OR "0.00"=""', True),
    ('abs(0) < 0.001 OR "0"=""', True),
    ('abs(999) < 0.001 OR "toast"=""', False),
    ('abs(760.23) < 0.001 OR "760.23"=""', False),
    # non responder in previous period POPDT
    ('("responded" != "non_responder") AND ((45/123)>2) AND (123>100)', False),
    ('("non_responder" != "non_responder") AND ((45/123)<2) AND (123>100)', False),
    ('("responded" != "non_responder") AND ((45/123)<2) AND (123>100)', True),
    # POPNZ
    ('("responded" = "non_responder") AND (0=0)', False),
    ('("non_responder" = "non_responder") AND (0=0)', True),
    # general
    ("1", 1),
    ('"test"','"test"'),
    ("2*3*4", 24),
    ("4+5", 9),
    ("2^2+2", 6),
    ("2+2^2", 6),
    ("2+2*2+2", 8),
    ("exp(sin(0))", 1),
    ("1 < 2 AND 4 > 3", True),
    ("2 < 2 AND 4 > 3", False),
    ("2 < 2 OR 4 > 3", True),
    ("(2 < 2) OR (4 > 3) OR (1=1)", True),
    ("abs(-10+5)", 5),
    ('"1234"!="" AND 1234!=0', True),
    ('""!="" OR 0=0', True),
    ('1234!="1234" AND 1234!=0', True),
    ("1 IN [1]", True),
    ('"a" IN ["a"]', True),
    ("1 IN [3,1,2,4,7]", True),
    ("1 IN [2,3,4]", False),
    ('"house" IN ["bucket","cheese","house","moose"]', True),
    ('"parsley" IN [1,2,3,4]', False),
    ]

@pytest.mark.parametrize("formula, expected", testData)
def test_ValidationParser(formula, expected):
    assert validationparsing(formula) == expected


# def test_value_present():
#     print("Testing Value Present: ")
#     assert validationparsing('"3.14"!=""') == True
#     assert validationparsing('"test"="test"') == True
#     assert validationparsing('"toast"=""') == False
#     assert validationparsing('""=""') == True
#     assert validationparsing('432=""') == False


# def test_zero_continuity():
#     print("Testing Zero Continuity: ")
#     assert (
#         validationparsing("(abs(25)>0 AND 0=0) OR (abs(0)>0 AND 25=0) AND abs(0-25)>15")
#         == True
#     )
#     assert (
#         validationparsing("(abs(25)>0 AND 0=0) OR (abs(0)>0 AND 25=0) AND abs(0-25)>25")
#         == False
#     )
#     assert (
#         validationparsing("(abs(0)>0 AND 0=0) OR (abs(0)>0 AND 0=0) AND abs(0-0)>0")
#         == False
#     )
#     assert (
#         validationparsing(
#             "(abs(100)>0 AND 50=0) OR (abs(50)>0 AND 100=0) AND abs(100-50)>0"
#         )
#         == False
#     )


# def test_large_value():
#     print("Testing Large Value: ")
#     assert validationparsing("2 >= 2") == True
#     assert validationparsing("100 >= 5") == True
#     assert validationparsing('"zorro" >= "alpha"') == True


# def test_question_vs_derived_question():
#     print("Question v Derived Question:   i.e. <value> <operator> <value>")
#     assert validationparsing('"banana" <= "yoghurt"') == True
#     assert validationparsing('1234!="1234"') == True
#     assert validationparsing("1 < 2") == True
#     assert validationparsing("1.01 < 1") == False
#     assert validationparsing("3.01 <= 3.02") == True
#     assert validationparsing("3.01 != 3.02") == True


# def test_valuepresent_with_sic():
#     print("Value Present with SIC:")
#     assert (
#         validationparsing('"1.2" != "" AND "90101" IN ["12345","90101","34545"]')
#         == True
#     )
#     assert (
#         validationparsing('"" != "" AND "90101" IN ["12345","90101","34545"]') == False
#     )
#     assert (
#         validationparsing('245 != "" AND "90105" IN ["12345","90101","34545"]') == False
#     )


# def test_valuepresent_excluding_sic():
#     print("Value Present excluding SIC:")
#     assert (
#         validationparsing('"1.2" != "" AND "90101" NOTIN ["12345","90101","34545"]')
#         == False
#     )
#     assert (
#         validationparsing('"" != "" AND "90101" NOTIN ["12345","90101","34545"]')
#         == False
#     )
#     assert (
#         validationparsing('245 != "" AND "90105" NOTIN ["12345","90101","34545"]')
#         == True
#     )


# def test_compulsory_value():
#     print("Compulsory Value:")
#     assert validationparsing('abs(0.00) < 0.001 OR "0.00"=""') == True
#     assert validationparsing('abs(0) < 0.001 OR "0"=""') == True
#     assert validationparsing('abs(999) < 0.001 OR "toast"=""') == False
#     assert validationparsing('abs(760.23) < 0.001 OR "760.23"=""') == False


# def test_nonresponder_in_previous_period_dq_vs_threshhold():
#     print("NonResponder in Previous Period - DQ v Threshold (POPDT):")
#     assert (
#         validationparsing(
#             '("responded" != "non_responder") AND ((45/123)>2) AND (123>100)'
#         )
#         == False
#     )
#     assert (
#         validationparsing(
#             '("non_responder" != "non_responder") AND ((45/123)<2) AND (123>100)'
#         )
#         == False
#     )
#     assert (
#         validationparsing(
#             '("responded" != "non_responder") AND ((45/123)<2) AND (123>100)'
#         )
#         == True
#     )


# def test_nonresponder_in_previous_period_now_zero():
#     print("NonResponder in Previous Period - Now Zero (POPNZ):")
#     assert validationparsing('("responded" = "non_responder") AND (0=0)') == False
#     assert validationparsing('("non_responder" = "non_responder") AND (0=0)') == True


# def test_general():
#     print("General:")
#     assert validationparsing("1") == 1
#     assert validationparsing('"test"') == '"test"'
#     assert validationparsing("2*3*4") == 24
#     assert validationparsing("4+5") == 9
#     assert validationparsing("2^2+2") == 6
#     assert validationparsing("2+2^2") == 6
#     assert validationparsing("2+2*2+2") == 8
#     assert validationparsing("exp(sin(0))") == 1
#     assert validationparsing("1 < 2 AND 4 > 3") == True
#     assert validationparsing("2 < 2 AND 4 > 3") == False
#     assert validationparsing("2 < 2 OR 4 > 3") == True
#     assert validationparsing("(2 < 2) OR (4 > 3) OR (1=1)") == True
#     assert validationparsing("abs(-10+5)") == 5
#     assert validationparsing('"1234"!="" AND 1234!=0') == True
#     assert validationparsing('""!="" OR 0=0') == True
#     assert validationparsing('1234!="1234" AND 1234!=0') == True
#     assert validationparsing("1 IN [1]") == True
#     assert validationparsing('"a" IN ["a"]') == True
#     assert validationparsing("1 IN [3,1,2,4,7]") == True
#     assert validationparsing("1 IN [2,3,4]") == False
#     assert validationparsing('"house" IN ["bucket","cheese","house","moose"]') == True
#     assert validationparsing('"parsley" IN [1,2,3,4]') == False

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
    ('"zorro" >= "alpha"', True),
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
    ('"test"', '"test"'),
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

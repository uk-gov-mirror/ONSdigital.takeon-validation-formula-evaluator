# takeon-validation-formula-evaluator
Core engine of the validation process. Evaluates each formula and returns the response.


**Not production code**
No logging behaviour
No CI/CD integration
Not using Serverless
No formal unit test suite
Limited error handling

**pyparsing.py**
Library file which provides the formula parsing. 
Primary source: https://github.com/pyparsing/pyparsing

**ValidationParser.py**
Class to provide the definition of a valid formula.

**ValidationParserStack.py**
Class to provide the behaviour of each operation within a formula.

**ValidationRunner.py**
Single function which accepts a list containing 'fomrula' and 'metadata'.
Instantiates the parser and iterates over the list to produce an output list

**lambda_function.py**	First commit	8 minutes ago
Lambda entry point.
Unpacks the given json depending on whether it has been called via API gateway or directly.
If it has been given a valid JSON payload evaluate it.
Returns the given output list from the evaluator

**test_harness.py**
Wrapper class for grouping some behaviour tests


**Input JSON**
{
  "validation_input": 
    [
      { "formula": "abs(12) < 3000", "metadata": {} },
      ...
      { "formula": "(abs(25)>0 AND 0=0), "metadata": {"reference": "49900001", "survey": "099", "period": "201409" } 
    ]
}

**Output JSON**
{
      { "formula": "abs(12) > 3000", "triggered":False, "metadata": {} },
      ...
      { "formula": "(abs(25)>0 AND 0=0), "triggered":True, "metadata": {"reference": "49900001", "survey": "099", "period": "201409" } 
}

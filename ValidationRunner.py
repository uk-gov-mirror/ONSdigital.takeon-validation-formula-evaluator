from ValidationParser import ValidationParser


def run(validation_input):
    all_output = []
    p = ValidationParser()
    for item in validation_input["validation_input"]:
        formula = item["formula"]
        row_output = {'formula': formula, 'metadata': item["metadata"], 'triggered': p.safe_evaluate(formula)}
        all_output.append(row_output)
    return all_output

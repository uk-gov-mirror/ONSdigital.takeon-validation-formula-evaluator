import json
from ValidationRunner import run

def lambda_handler(event, context):
    output = run(extract_json_input(event))
    return dict(statusCode=200, body=json.dumps(output))


def extract_json_input(input_data):
    if 'body' in input_data:
        return json.loads(input_data.get('body'))
    else:
        return input_data

# Assumed input format:
# { "validation_input": [
#   {"formula": "1 < 3", "metadata": {} },
#   {"formula": "(abs(25)>0 AND 0=0), "metadata": {"reference": "49900001", "survey": "099", "period": "201409"} ] }
#
# However, when called through the API Gateway this is embedded within a 'body' of a more complicated JSON structure
#
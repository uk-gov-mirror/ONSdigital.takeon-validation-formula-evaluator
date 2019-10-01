import json
from ValidationRunner import run
import os
import boto3


def lambda_handler(event, context):
    try:
        output = run(extract_json_input(event))
        output_to_queue(output)
        return dict(statusCode=200, body=json.dumps(output))
    except KeyError:
        return "Wrong or missing key in JSON"
    except ValueError:
        return "Incorrect value"
    except ZeroDivisionError:
        return "Cannot divide by zero"
    except NameError:
        return "Missing variable"
    except SyntaxError:
        return "Incorrect syntax"
    except Exception:
        return "Something went wrong"
    


def extract_json_input(input_data):
    if "Records" in input_data:
        return json.loads(input_data["Records"][0]["body"])
    else:
        return input_data


def output_to_queue(output):
    queue_url = os.getenv("OUTPUT_QUEUE_URL")
    sqs = boto3.client("sqs")
    sqs.send_message(QueueUrl=queue_url, MessageBody=json.dumps(output))


# Assumed input format:
# { "validation_input": [
#   {"formula": "1 < 3", "metadata": {} },
#   {"formula": "(abs(25)>0 AND 0=0), "metadata": {"reference": "49900001"
# , "survey": "099", "period": "201409"} ] }
#
# However, when called through the API Gateway this is embedded within a
# 'body' of a more complicated JSON structure
#

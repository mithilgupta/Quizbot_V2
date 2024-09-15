# GitHub Actions taken from : https://www.youtube.com/watch?v=xs9oJaaU8I8&t=265s

import json

def lambda_handler(event, context):
    # TODO implement

	input_prompt=event['prompt']
    print(input_prompt)
	print(type(input_prompt))

    return {
        'statusCode': 200,
        'body': json.dumps("hello from lambda")
    }

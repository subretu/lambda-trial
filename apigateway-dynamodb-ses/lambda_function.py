import json


def lambda_handler(event, context):
    print(json.dumps(event, indent=4))

    return{
        'statusCode': 200,
        'headers': {
            'content-type': 'text/html'
        },
        'body': '<html><body>OK</body></html>'
    }

import json, boto3


def handler(event, context):
    # Log the event argument for debugging and for use in local development.
    print(json.dumps(event))

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('challenge_DB')
    response = {
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        }
    }

    if str(event['routeKey']) == "GET /items/{id}":
        item_id = event['pathParameters']['id']
        result = table.get_item(
            Key = {
                'id':item_id
            },
        )
        visitors = result['Item']['visitors']
        response['body'] = json.dumps(int(visitors))
        response['statusCode'] = 200

    elif  event['routeKey'] == 'PUT /items':
        request_body = json.loads(event['body'])
        #Put item in DynamoDB
        result = table.put_item(
            Item={
                'id' : request_body['id'],
                'visitors' : request_body['visitors']
            })
        response['statusCode'] = 200
        response['body'] = " update successfully "

    else:
        response['statusCode'] = 400
        response['body'] = "error"

    return response

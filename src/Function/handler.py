import json, boto3


headers = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*'
    }
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('challenge_DB')

def handler(event, table):
    # Log the event argument for debugging and for use in local development.
    # print(json.dumps(event))



    if str(event['routeKey']) == "GET /items/{id}":
        item_id = event['pathParameters']['id']
        return getitem(table, item_id)
        # visitors = result['Item']['visitors']
        # response['body'] = json.dumps(int(visitors))
        # response['statusCode'] = 200

    elif event['routeKey'] == 'PUT /items':
        request_body = json.loads(event['body'])
        #Put item in DynamoDB
        return putitem(table, request_body)
        # result = table.put_item(
        #     Item={
        #         'id' : request_body['id'],
        #         'visitors' : request_body['visitors']
        #     })
        # response['statusCode'] = 200
        # response['body'] = " update successfully "

    else:
         return   {
            'headers': headers,
            'statusCode' : 400,
            'body':  'error bad request'
        }


def getitem(table,item_id):
    result = table.get_item(
        Key = {
            'id': item_id
        },
    )
    response= {
        'headers': headers
    }

    visitors = result['Item']['visitors']
    response['body'] = json.dumps(int(visitors))
    response['statusCode'] = 200
    return response


def putitem(table,item):
    response = {
        'headers': headers
    }
    result = table.put_item(
        Item = item
    )
    response['statusCode'] = 200
    response['body'] = " update successfully "

    return response
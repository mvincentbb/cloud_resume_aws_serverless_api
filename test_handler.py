import json

import boto3
from moto import mock_dynamodb

from src.Function.handler import handler, getitem


@mock_dynamodb
def test_getitem():

    # Initiate a mock dynamodb
    table_name = "mock_db"
    boto3.setup_default_session()
    table = boto3.client("dynamodb", region_name='us-east-1')
    table.create_table(
        KeySchema=[
            {'AttributeName': 'id', 'KeyType': 'HASH'}
            # {'AttributeName': 'visitors', 'KeyType': 'RANGE'}
        ],
        AttributeDefinitions=[
            {'AttributeName': 'id', 'AttributeType': 'S'},
            # {'AttributeName': 'visitors', 'AttributeType': 'N'},
        ],
        TableName=table_name,
        BillingMode="PAY_PER_REQUEST"
    )

    # Put some mock data in the database
    mock_data = {'id':'1', 'visitors': 2}
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table(table_name)
    table.put_item(
    Item = mock_data
    )


    # Test get event
    #mock event
    mock_get_event = {'routeKey': "GET /items/{id}", 'pathParameters': {'id': '1'}}
    #call handler
    result = handler(mock_get_event, table)
    # result = getitem(table, '1')
    # print(result)
    response = {
        'headers':
            {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
        'body': '2', 'statusCode': 200}

    assert response == result

    #Test put event
    # mock_put_event = {'routeKey': "PUT /items", 'body':{'id':'1', 'visiors': 4}}
    mock_put_event = {'routeKey': 'PUT /items', 'body': json.dumps({'id': '1', 'visitors': 10})}

    result = handler(mock_put_event, table)
    print(result)
    data = table.get_item(
        Key = {
            'id': '1'
        },
    )
    print(data)

    assert data['Item'] == {'id': '1', 'visitors': 10}








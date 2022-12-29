import boto3
from moto import mock_dynamodb

from src.Function.handler import handler, getitem


@mock_dynamodb
def test_handler3():
    # dynamodb = boto3.resource('dynamodb', region_mame='us-east-1'')
    # table = dynamodb.Table('challenge_DB')
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
    # yield table_name
    mock_data = {'id':'1', 'visitors': 2}
    # mock_data = {"id": "1", "visitors":  2}



    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

    table = dynamodb.Table(table_name)

    table.put_item(
    Item = mock_data
    )

    event = {'routeKey': "GET /items/{id}", 'pathParameters': {'id': '1'}}

    result = handler(event, table)

    # result = getitem(table, '1')
    print(result)
    response = {'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'}, 'body': '2', 'statusCode': 200}
    # assert {'body': '{"N": "2"}', 'statusCode': 200} == result
    assert response == result








# test_dynamo_repository.py
import pytest
from moto import mock_aws
import boto3
from src.repository.dynamo_db import DynamoRepository

@pytest.fixture
def dynamo_table():
    with mock_aws():
        client = boto3.client('dynamodb', region_name='us-east-1')
        client.create_table(
            TableName='test_table',
            KeySchema=[
                {'AttributeName': 'user', 'KeyType': 'HASH'},
                {'AttributeName': 'datetime', 'KeyType': 'RANGE'}
            ],
            AttributeDefinitions=[
                {'AttributeName': 'user', 'AttributeType': 'S'},
                {'AttributeName': 'datetime', 'AttributeType': 'S'}
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )
        yield
        client.delete_table(TableName='test_table')

@pytest.fixture
def dynamo_repository(dynamo_table):
    return DynamoRepository(region_name='us-east-1', table_name='test_table')

def test_create_item(dynamo_repository):
    result = dynamo_repository.create_item(
        identification='123',
        datetime='2023-01-01T00:00:00Z',
        date='2023-01-01',
        user='user1',
        status='PROCESSING',
        payload_inbound='{}',
        video_name='video.mp4'
    )
    assert result is True

def test_update_item(dynamo_repository):
    dynamo_repository.create_item(
        identification='123',
        datetime='2023-01-01T00:00:00Z',
        date='2023-01-01',
        user='user1',
        status='PROCESSING',
        payload_inbound='{}',
        video_name='video.mp4'
    )
    result = dynamo_repository.update_item(
        user='user1',
        datetime='2023-01-01T00:00:00Z',
        status='COMPLETED'
    )
    assert result is not None
    assert result['Attributes']['status'] == 'COMPLETED'

import boto3
from botocore.exceptions import ClientError


class DynamoRepository:
    def __init__(self, region_name=None, table_name=None):
        self.region_name = region_name
        self.table_name = table_name
        self.dynamodb = boto3.resource('dynamodb',
                                       region_name=self.region_name
                                       )
        self.table = self.dynamodb.Table(self.table_name)

    def create_item(self, identification, datetime,date, user, status, payload_inbound, video_name):
        item = {
            'user': user,
            'datetime': datetime,
            'date':date,
            'status': status,
            'payload_inbound': payload_inbound,
            'video_name': video_name,
            's3_file_name': f'{identification}.zip'
        }
        try:
            self.table.put_item(Item=item)
            print(f'[DYNAMO] - Item created: {item}')
            return True
        except ClientError as e:
            print(f'Error creating item: {e.response['Error']['Message']}')
            return False

    def update_item(self, user, datetime, status):
        update_expression = []
        expression_attribute_values = {}
        expression_attribute_names = {}

        if status:
            update_expression.append('#status = :status')
            expression_attribute_values[':status'] = status
            expression_attribute_names['#status'] = 'status'

        if not update_expression:
            print('No attributes to update')
            return None

        update_expression = 'SET ' + ', '.join(update_expression)

        try:
            response = self.table.update_item(
                Key={'user': user, 'datetime': datetime},
                UpdateExpression=update_expression,
                ExpressionAttributeValues=expression_attribute_values,
                ExpressionAttributeNames=expression_attribute_names,
                ReturnValues='UPDATED_NEW'
            )

            print(f'[DYNAMO] Item updated: {response.get('Attributes', None)}')
            return response
        except ClientError as e:
            print(f'Error updating item: {e.response['Error']['Message']}')
            return None
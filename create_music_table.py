"""
Here I make this script to create music table. I wanted to try make this one programmatically. It seems worked well in my attempt. Took some time though.
"""
import boto3

# initialize DynamoDB
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

def create_music_table():
    table = dynamodb.create_table(
        TableName='music',
        KeySchema=[
            {
                'AttributeName': 'title',
                # partition key
                'KeyType': 'HASH'
            },
            {
                'AttributeName': 'artist',
                # sort Key
                'KeyType': 'RANGE'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'title',
                # string
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'artist',
                # string
                'AttributeType': 'S'  
            },
            {
                'AttributeName': 'year',
                # string for secondary index
                'AttributeType': 'S'  
            }
        ],
        GlobalSecondaryIndexes=[
            {
                'IndexName': 'year-index',
                'KeySchema': [
                    {
                        'AttributeName': 'year',
                        # partition key for the index
                        'KeyType': 'HASH'  
                    }
                ],
                'Projection': {
                # retrieve all attributes
                    'ProjectionType': 'ALL'  
                },
                'ProvisionedThroughput': {
                    'ReadCapacityUnits': 5,
                    'WriteCapacityUnits': 5
                }
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )
    table.meta.client.get_waiter('table_exists').wait(TableName='music')
    print("Music table created with title, artist, and year-index. for querying later")

# call function here
create_music_table()

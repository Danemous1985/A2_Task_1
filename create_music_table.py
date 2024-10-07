import boto3

# Initialize DynamoDB
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

def create_music_table():
    table = dynamodb.create_table(
        TableName='music',
        KeySchema=[
            {
                'AttributeName': 'title',
                # Partition key
                'KeyType': 'HASH'
            },
            {
                'AttributeName': 'artist',
                # Sort Key
                'KeyType': 'RANGE'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'title',
                # String
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'artist',
                # String
                'AttributeType': 'S'  
            },
            {
                'AttributeName': 'year',
                # String for secondary index
                'AttributeType': 'S'  
            }
        ],
        GlobalSecondaryIndexes=[
            {
                'IndexName': 'year-index',
                'KeySchema': [
                    {
                        'AttributeName': 'year',
                        # Partition key for the index
                        'KeyType': 'HASH'  
                    }
                ],
                'Projection': {
                # Retrieve all attributes
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

# Run the function
create_music_table()

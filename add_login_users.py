import boto3

# Initialize DynamoDB resource
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

"""
Function to add users to the login table
"""
def add_users():
    table = dynamodb.Table('login')

    users = [
        {'email': 's35788544@student.rmit.edu.au', 'user_name': 'Dane Goulter', 'password': '012345'},
        {'email': 's34654341@student.rmit.edu.au', 'user_name': 'Jill Johnson', 'password': '123456'},
        {'email': 's33067112@student.rmit.edu.au', 'user_name': 'Bob Smith', 'password': '234567'},
        {'email': 's31003973@student.rmit.edu.au', 'user_name': 'Tamara Green', 'password': '345678'},
        {'email': 's30095434@student.rmit.edu.au', 'user_name': 'Amy Lee', 'password': '456789'},
        {'email': 's32233445@student.rmit.edu.au', 'user_name': 'Kurt Cobain', 'password': '567890'},
        {'email': 's35657586@student.rmit.edu.au', 'user_name': 'April Goulter', 'password': '678901'},
        {'email': 's33456547@student.rmit.edu.au', 'user_name': 'Steve Beninati', 'password': '789012'},
        {'email': 's36968758@student.rmit.edu.au', 'user_name': 'Samuel Beninati', 'password': '890123'},
        {'email': 's31029389@student.rmit.edu.au', 'user_name': 'Chris Cross', 'password': '901234'}
    ]

    for user in users:
        table.put_item(Item=user)
        print(f"Added {user['user_name']}")

# Run the function
add_users()

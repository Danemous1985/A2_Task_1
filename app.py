from flask import Flask, render_template, request, redirect, url_for, session
import boto3

app = Flask(__name__)
app.secret_key = 'my_key'

"""
NOTE FOR TUTOR:
The credentials below are temporary. I'm having some issue with credentials. Have read alot and seems for some reason, Flask is not detecting the aws credentials file in my EC2 instance. Not sure why. Some reading suggest it may be some problem relating with Flask and using AWS Learner lab permissions limitations. I'm going to try different method soon to try fix this. For right now though, I need to insert the AWS session credentials programatically, not too different from usual anyway. It's just needed for dynamoDB and S3 right now.
"""
dynamodb = boto3.resource(
    'dynamodb',
    region_name='us-east-1',
    aws_access_key_id='ASIASSPVW4E4E3ZL4QE7',
    aws_secret_access_key='BiltZLny2hFvvg41n3xL6LcgcMpaAexhT6SUWMe0',
    aws_session_token='IQoJb3JpZ2luX2VjEE4aCXVzLXdlc3QtMiJHMEUCIQCrpDGC85OVIubbM8wsXsNm6gYw7Hvosm53QA/KjYDXqAIgQ9wO3hWLRT8GaIY66E6Ep5FsILu5XokYZXk0VETD5cIqrwIIp///////////ARAAGgwxNzcxNDU4MzE3MzYiDFRLe+JJzJshC9CZLCqDAusl5l2mfxqyrdjhuRrD1G7B1hdBYXLOmW3HiNp7BvuKkwPXcfWWKcSYy9wu97rVM3LntMudSSsidQman2a3yh3qecLsWsEeC8j7OZdw6u2LqTldrTtNq8O55ifuYAagYJtq5/s/sw97gr8MgALNVS8SDce9WR9eMqorf/qf+O0oR/qH3TJ5OTqLzjzeEgD+8GyggYIZmLCSkvDKb8lmP0Bu0KMjy+r8D9aYY4Vc+VTDgIgp499tF4RXVxVYZOZu6F0ezSXuQ3G3nPL57x7LpVOypiKLdIal3gWf3Jcmw+aJGTWieT9WC6LJqpIFMXUhJFHf1asqCfYa7IMhXQ8MO4vHS78w7IOquAY6nQH/oDS4y9GpLwb4glUQCxCoP5uZuwyG7Zrt7yyRMgCq/5ahuFA0wZhdhVnHcr0fl9RdOWpiRidFFrN2pkIyHBxS9SFEhg95QJ5UpVSSaIXj3ukULN3tMAtuXgUp/jy/p7k4O+shdl9THMJOS6q+5pJrrTV/h3wOFeY3nDwadmYjf7Y4W7RZ+ByXehELsD9p6CJs0x3J3kSvaAfbwzw8'
)

s3 = boto3.client(
    's3',
    region_name='us-east-1',
    aws_access_key_id='ASIASSPVW4E4E3ZL4QE7',
    aws_secret_access_key='BiltZLny2hFvvg41n3xL6LcgcMpaAexhT6SUWMe0',
    aws_session_token='IQoJb3JpZ2luX2VjEE4aCXVzLXdlc3QtMiJHMEUCIQCrpDGC85OVIubbM8wsXsNm6gYw7Hvosm53QA/KjYDXqAIgQ9wO3hWLRT8GaIY66E6Ep5FsILu5XokYZXk0VETD5cIqrwIIp///////////ARAAGgwxNzcxNDU4MzE3MzYiDFRLe+JJzJshC9CZLCqDAusl5l2mfxqyrdjhuRrD1G7B1hdBYXLOmW3HiNp7BvuKkwPXcfWWKcSYy9wu97rVM3LntMudSSsidQman2a3yh3qecLsWsEeC8j7OZdw6u2LqTldrTtNq8O55ifuYAagYJtq5/s/sw97gr8MgALNVS8SDce9WR9eMqorf/qf+O0oR/qH3TJ5OTqLzjzeEgD+8GyggYIZmLCSkvDKb8lmP0Bu0KMjy+r8D9aYY4Vc+VTDgIgp499tF4RXVxVYZOZu6F0ezSXuQ3G3nPL57x7LpVOypiKLdIal3gWf3Jcmw+aJGTWieT9WC6LJqpIFMXUhJFHf1asqCfYa7IMhXQ8MO4vHS78w7IOquAY6nQH/oDS4y9GpLwb4glUQCxCoP5uZuwyG7Zrt7yyRMgCq/5ahuFA0wZhdhVnHcr0fl9RdOWpiRidFFrN2pkIyHBxS9SFEhg95QJ5UpVSSaIXj3ukULN3tMAtuXgUp/jy/p7k4O+shdl9THMJOS6q+5pJrrTV/h3wOFeY3nDwadmYjf7Y4W7RZ+ByXehELsD9p6CJs0x3J3kSvaAfbwzw8'
)

# s3 = boto3.client('s3', region_name='us-east-1')

# dynamoDB tables
login_table = dynamodb.Table('login')
music_table = dynamodb.Table('music')
subscriptions_table = dynamodb.Table('subscription')

"""
route returns index page (functions as login page)
"""
@app.route('/')
def index():
    return render_template('index.html')

"""
route for going regitration page. As of now, registering new user is fully functional.
"""
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        user_name = request.form['user_name']
        password = request.form['password']

        # check if email already exists in the table
        response = login_table.get_item(Key={'email': email})
        
        if 'Item' in response:
            error = "The email is already registered."
            return render_template('register.html', error=error)

        # store new user in the DynamoDB table
        login_table.put_item(
            Item={
                'email': email,
                'user_name': user_name,
                'password': password
            }
        )
        return redirect(url_for('index'))
    
    return render_template('register.html')


"""
route for login. It is working correctly and dynamoDB database with users is fully setup and functioning with correct partition key.
"""
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # retrieve the user from DynamoDB based on email
        response = login_table.get_item(Key={'email': email})

        if 'Item' in response:
            user = response['Item']
            if user['password'] == password:
                session['email'] = user['email']
                session['user_name'] = user['user_name']  # Store user name in session
                return redirect(url_for('main_page'))
            else:
                error = "Invalid credentials"
                return render_template('index.html', error=error)
        else:
            error = "User not found"
            return render_template('index.html', error=error)

    return render_template('index.html')

"""
simply logout route for logging out user.
"""
@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('email', None)
    return redirect(url_for('index'))

"""
main page route. It's working so far, but not all functions in yet. Have done test with artist image, logging in and pulling the right subscription and is going ok so far. Alot more for different functions for main page I'll create soon.
"""
@app.route('/main_page')
def main_page():
    if 'email' in session:
        user_email = session['email']
        
        # get user's name
        response = login_table.get_item(Key={'email': user_email})
        user_name = response['Item']['user_name']
        
        # retrieve subscribed music data for the user from subscriptions table
        subscription_response = subscriptions_table.query(
            KeyConditionExpression=boto3.dynamodb.conditions.Key('email').eq(user_email)
        )
        subscriptions = subscription_response.get('Items', [])
        
        # collect the music based on subscription
        subscribed_music = []
        for subscription in subscriptions:
            music_id = subscription.get('music_id')
            artist = subscription.get('artist')
            
            # query music table using both title (music_id) and artist
            music_response = music_table.get_item(Key={'title': music_id, 'artist': artist})
            if 'Item' in music_response:
                music_data = music_response['Item']
                
                # Get the artist image from S3 bucket
                artist_image_key = music_data.get('img_url')
                artist_image_url = s3.generate_presigned_url(
                    'get_object',
                    Params={'Bucket': 'task1musicimages', 'Key': artist_image_key},
                    ExpiresIn=3600
                )
                
                music_data['artist_image_url'] = artist_image_url
                subscribed_music.append(music_data)

        return render_template('main.html', user_name=user_name, subscribed_music=subscribed_music)
    
    return redirect(url_for('index'))



# remove subscription for the user
@app.route('/remove_music/<music_id>', methods=['POST'])
def remove_music(music_id):
    user_email = session['email']
    subscriptions_table.delete_item(
        Key={
            'email': user_email,
            'music_id': music_id
        }
    )
    return redirect(url_for('main_page'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)

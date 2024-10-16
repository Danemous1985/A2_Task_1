from flask import Flask, render_template, request, redirect, url_for, session
import boto3
from boto3.dynamodb.conditions import Attr

app = Flask(__name__)
app.secret_key = 'my_key'

"""
NOTE FOR TUTOR:
The credentials below are temporary. I'm having some issue with credentials. Have read alot and seems for some reason, Flask is not detecting the aws credentials file in my EC2 instance. Not sure why. Some reading suggest it may be some problem relating with Flask and using AWS Learner lab permissions limitations. I'm going to try different method soon to try fix this. For right now though, I need to insert the AWS session credentials programatically, not too different from usual anyway. It's just needed for dynamoDB and S3 right now.
"""
dynamodb = boto3.resource(
    'dynamodb',
    region_name='us-east-1',
    aws_access_key_id='ASIASSPVW4E4PBJYURYQ',
    aws_secret_access_key='CnueBha8Vc2n946wymnn6Xt2r1GuO8a/QWLjvXTO',
    aws_session_token='IQoJb3JpZ2luX2VjEK///////////wEaCXVzLXdlc3QtMiJGMEQCIHZfTVDSVK8Q8XjIDnid+NgKIlRUPr6viyvK2zsY3rmHAiBC6mjJ2kToLZK3u/fxXf7S1A/IftCgJgxxOCj7JMStgCqmAggXEAAaDDE3NzE0NTgzMTczNiIMVQT/Vx4JEB4Yb9C+KoMC1mUJt/ciOgvAAdD9F9TMKLx1/j/YDl7L/b0WMjo5q6DntP9vm4BKRYF34I3eoI652xNpC4EsUhQRD4ec/BGpHd6cd1n+JTm6IcS5iOO5xvmxNFmhsPRHg4FuMnj9tIcIHdTY2ZmgxpnE4MWCjtCw1nb7oqzBiReFFxiPs0+MmNmxsYKL0l42IhVEmCFCEePOLvosRL7hgjMRVt+ZQuO1zSdCrix0Vw7Y9ULIX8faYzEOZKupTXWjJH4SfwdiZ66lD4F3zQtTR0/DUis5PS0JoeGTZOEC6eGYyeiwq4lODYxmNGGhsP+KxHqIuWsuMxeMkPxDhmcWH3FNt4ksqxpSLR68FzDBlr+4BjqeATNzCD5pq8yqJ36lbmEnIalNuQFI1JGfgd+bd0uNG82StbAOuokI/M6eNkSG54+e+sON/QB/xiFLP3AQ6fib0dBOexBICVfXX4EoVIjeHiNIdQ2L5OlJWCVIy8eDKi/8AhM2XHBGAGFTEeoCP/Yicxf4XDKtHvvMvFJSOgaG3Bijn2Licxwv5dVMR/cQCSwOmSyPa3ATlnWtQ+C/LyTu'
)

s3 = boto3.client(
    's3',
    region_name='us-east-1',
    aws_access_key_id='ASIASSPVW4E4PBJYURYQ',
    aws_secret_access_key='CnueBha8Vc2n946wymnn6Xt2r1GuO8a/QWLjvXTO',
    aws_session_token='IQoJb3JpZ2luX2VjEK///////////wEaCXVzLXdlc3QtMiJGMEQCIHZfTVDSVK8Q8XjIDnid+NgKIlRUPr6viyvK2zsY3rmHAiBC6mjJ2kToLZK3u/fxXf7S1A/IftCgJgxxOCj7JMStgCqmAggXEAAaDDE3NzE0NTgzMTczNiIMVQT/Vx4JEB4Yb9C+KoMC1mUJt/ciOgvAAdD9F9TMKLx1/j/YDl7L/b0WMjo5q6DntP9vm4BKRYF34I3eoI652xNpC4EsUhQRD4ec/BGpHd6cd1n+JTm6IcS5iOO5xvmxNFmhsPRHg4FuMnj9tIcIHdTY2ZmgxpnE4MWCjtCw1nb7oqzBiReFFxiPs0+MmNmxsYKL0l42IhVEmCFCEePOLvosRL7hgjMRVt+ZQuO1zSdCrix0Vw7Y9ULIX8faYzEOZKupTXWjJH4SfwdiZ66lD4F3zQtTR0/DUis5PS0JoeGTZOEC6eGYyeiwq4lODYxmNGGhsP+KxHqIuWsuMxeMkPxDhmcWH3FNt4ksqxpSLR68FzDBlr+4BjqeATNzCD5pq8yqJ36lbmEnIalNuQFI1JGfgd+bd0uNG82StbAOuokI/M6eNkSG54+e+sON/QB/xiFLP3AQ6fib0dBOexBICVfXX4EoVIjeHiNIdQ2L5OlJWCVIy8eDKi/8AhM2XHBGAGFTEeoCP/Yicxf4XDKtHvvMvFJSOgaG3Bijn2Licxwv5dVMR/cQCSwOmSyPa3ATlnWtQ+C/LyTu'
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
            error = "The email already exists"
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

        # retrieve the user from dynamoDB based on email
        response = login_table.get_item(Key={'email': email})

        if 'Item' in response:
            user = response['Item']
            if user['password'] == password:
                session['email'] = user['email']
                  # store user name in session
                session['user_name'] = user['user_name']
                return redirect(url_for('main_page'))
            else:
                error = "email or password invalid"
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
                
                # get artist image from S3 bucket
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
    if 'email' in session:
        user_email = session['email']
        try:
            subscriptions_table.delete_item(
                Key={
                    'email': user_email,
                    'music_id': music_id
                }
            )
        except Exception as e:
            print(f"Error while removing: {e}")

        return redirect(url_for('main_page'))
    
    return redirect(url_for('index'))




@app.route('/query_music', methods=['POST'])
def query_music():
    # get username from the session
    user_name = session.get('user_name', 'User')

    title = request.form.get('title')
    artist = request.form.get('artist')
    year = request.form.get('year')

    filter_expression = None

    # construct the filter expression for query. This worked better
    if title:
        filter_expression = Attr('title').contains(title)
    
    if artist:
        if filter_expression:
            filter_expression = filter_expression & Attr('artist').contains(artist)
        else:
            filter_expression = Attr('artist').contains(artist)

    if year:
        if filter_expression:
            filter_expression = filter_expression & Attr('year').contains(year)
        else:
            filter_expression = Attr('year').contains(year)

    # return an empty result set if nothing provided
    if not filter_expression:
        return render_template('main.html', query_results=[], user_name=user_name)

    # now query music table using filter expression
    query_response = music_table.scan(FilterExpression=filter_expression)
    query_results = query_response.get('Items', [])

    # for every result generate the URL for the artist image from S3 bucket
    for result in query_results:
        artist_image_key = result.get('img_url')
        artist_image_url = s3.generate_presigned_url(
            'get_object',
            Params={'Bucket': 'task1musicimages', 'Key': artist_image_key},
            ExpiresIn=3600
        )
        result['artist_image_url'] = artist_image_url

    # render main page with query results and user name
    return render_template('main.html', query_results=query_results, user_name=user_name)



@app.route('/subscribe_music/<music_id>/<artist>', methods=['POST'])
def subscribe_music(music_id, artist):
    user_email = session['email']

    # add subscription to dynamoDB table
    try:
        subscriptions_table.put_item(
            Item={
                'email': user_email,
                'music_id': music_id,
                'artist': artist
            }
        )
    except Exception as e:
        print(f"Error while subscribing: {e}")

    return redirect(url_for('main_page'))



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)

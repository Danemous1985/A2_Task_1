import boto3
import json
import requests
import os

# Initialize DynamoDB and S3
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
s3 = boto3.client('s3')

# bucket name
BUCKET_NAME = 'task1musicimages'

# reference music table
table = dynamodb.Table('music')

"""
function downloads images to ec2 instance
"""
def download_image(image_url, file_name):
    response = requests.get(image_url)
    if response.status_code == 200:
        with open(file_name, 'wb') as img_file:
            img_file.write(response.content)
        print(f"Image downloaded: {file_name}")
        return file_name
    else:
        print(f"Failed to download image from {image_url}")
        return None

"""
function then uploads images to S3 storage
"""
def upload_to_s3(file_name, bucket, object_name=None):
    if object_name is None:
        object_name = file_name
    try:
        s3.upload_file(file_name, bucket, object_name)
        print(f"Image uploaded to S3: {object_name}")
    except Exception as e:
        print(f"Failed to upload {file_name} to S3: {e}")

# open and read the JSON file
with open('a2.json', 'r') as json_file:
    music_data = json.load(json_file)
    
    # iterate through each item in the JSON file and load it into dynamo
    for music_item in music_data['songs']:
        table.put_item(
            Item={
                'title': music_item['title'],
                'artist': music_item['artist'],
                'year': music_item['year'],
                'web_url': music_item['web_url'],
                'img_url': music_item['img_url']
            }
        )
        print(f"Added {music_item['title']} by {music_item['artist']}")

        # download artist image
        image_file_name = f"{music_item['artist']}.jpg"
        downloaded_image = download_image(music_item['img_url'], image_file_name)

        # if image was downloaded, upload it to S3 bucket
        if downloaded_image:
            upload_to_s3(downloaded_image, BUCKET_NAME, f"artist_images/{image_file_name}")

        # remove local image after upload to S3 bucket
        if os.path.exists(image_file_name):
            os.remove(image_file_name)
            print(f"Local image file deleted: {image_file_name}")

print("Data and images have been successfully processed!")

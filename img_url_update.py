"""
I made this script a bit later on. The image URL's in dynamoDB were set wrong. This updated them.
"""
import boto3

# initialize dynamoDB resource
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

# reference the music table
music_table = dynamodb.Table('music')

# scan the table to get all items
response = music_table.scan()
items = response['Items']

# update each item in the table to correct the img_url field
for item in items:
    artist = item['artist']
    new_img_url = f"artist_images/{artist}.jpg"
    
    music_table.update_item(
        Key={
            'title': item['title'],
            'artist': item['artist']
        },
        UpdateExpression="set img_url = :i",
        ExpressionAttributeValues={
            ':i': new_img_url
        }
    )
    print(f"Updated {item['title']} by {item['artist']} with new img_url: {new_img_url}")

print("img_url fields updated")

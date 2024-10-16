# Music Subscription Service

This project is a cloud-based music subscription service built using **AWS DynamoDB**, **Flask**, and **boto3**.

## Setup Instructions  
NOTE: I've had trouble with credentials. Some reason, the program won't run correctly without my credentials  
inside the app.py. I know this isn't good security practice, but it seems boto3 has some issue clashing with  
the AWS Learner Lab version of things and I don't have access to change it. In normal circumstance, it should  
be easy fix, but I do not have the privileges. 

1. Clone the repository using Git.
2. Install the required dependencies.
3. Configure AWS credentials. Need to do this as had some trouble with running scripts.  
In the AWS CLI:  
   a. nano ~/.aws/credentials  
   b. Paste credentials  
   [default]  
   aws_access_key_id=  
   aws_secret_access_key=  
   aws_session_token=  
   Also need to add it in app.py
     
   dynamodb = boto3.resource(  
    'dynamodb',  
    region_name='us-east-1',  
    aws_access_key_id='',  
    aws_secret_access_key='',  
    aws_session_token=''    
   )  

   s3 = boto3.client(  
   's3',  
   region_name='us-east-1',  
   aws_access_key_id='',  
   aws_secret_access_key='',  
   aws_session_token=''  
     
5. Transfer app.py through FileZilla for new credentials then run the application through EC2 DNS address.

## File Structure
NOTE: login.html is no longer used. index.html is now the login page. I will remove unneeded files later.

```bash
.
├── app.py                  # Main Flask application
├── create_music_table.py    # Script to create the music table in DynamoDB
├── img_url_update.py        # Script to see the image URL to S3 correctly
├── load_music_data.py       # Script to load data into the music table
├── templates/               # HTML templates for the app
│   ├── index.html           # Home page
│   └── register.html        # Page for registering a new user
│   └── login.html           # Page for a user to login (this is redundant, index.html is now the login page)
│   └── main.html            # Main page after logging in
├── static/                  # Static files (CSS, JS, images)
│   └── main.css             # Styling for the main page
│   └── login.css            # Styling for login page
│   └── register.css         # Styling for registration page
├── requirements.txt         # Python dependencies
└── a2.json                  # JSON file containing music data

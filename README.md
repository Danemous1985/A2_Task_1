# Music Subscription Service

This project is a cloud-based music subscription service built using **AWS DynamoDB**, **Flask**, and **boto3**.

## Setup Instructions

1. Clone the repository using Git.
2. Install the required dependencies.
3. Configure AWS credentials. Need to do this as had some trouble with running scripts.
   In the AWS CLI:
   aws configure
   Example:
   AWS Access Key ID [None]: ASIASSPVW4E4NRSCHGDX
   AWS Secret Access Key [None]: eW1v9iFIfcrE83gR1aFhzBTcCN639xYcS/4Z9TMt
   Default region name [None]: us-east-1
   Default output format [None]: json
   
   export AWS_SESSION_TOKEN="SESSION_TOKEN"

5. Run the application.

## File Structure
(some are not implemented yet)

```bash
.
├── app.py                  # Main Flask application
├── create_music_table.py    # Script to create the music table in DynamoDB
├── load_music_data.py       # Script to load data into the music table
├── templates/               # HTML templates for the app
│   ├── index.html           # Home page
│   └── results.html         # Results page for music search
├── static/                  # Static files (CSS, JS, images)
├── requirements.txt         # Python dependencies
└── a2.json                  # JSON file containing music data

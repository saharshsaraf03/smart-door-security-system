from flask import Flask, render_template
import boto3
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

dynamodb = boto3.resource('dynamodb',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    region_name=os.getenv('AWS_REGION')
)

TABLE = os.getenv('DYNAMODB_TABLE')

@app.route('/')
def index():
    table = dynamodb.Table(TABLE)
    response = table.scan()
    items = response.get('Items', [])
    
    # Sort by timestamp descending (newest first)
    items = sorted(items, key=lambda x: x['timestamp'], reverse=True)
    
    # Calculate stats
    total = len(items)
    authorized = sum(1 for i in items if i['status'] == 'Authorized')
    unauthorized = sum(1 for i in items if i['status'] == 'Unauthorized')
    
    return render_template('index.html', 
                         items=items,
                         total=total,
                         authorized=authorized,
                         unauthorized=unauthorized)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
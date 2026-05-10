import boto3
import os
from dotenv import load_dotenv

load_dotenv()

# AWS Clients
s3 = boto3.client('s3',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    region_name=os.getenv('AWS_REGION')
)

rekognition = boto3.client('rekognition',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    region_name=os.getenv('AWS_REGION')
)

dynamodb = boto3.resource('dynamodb',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    region_name=os.getenv('AWS_REGION')
)

BUCKET = os.getenv('S3_BUCKET_NAME')
COLLECTION = os.getenv('REKOGNITION_COLLECTION')
TABLE = os.getenv('DYNAMODB_TABLE')

def create_rekognition_collection():
    try:
        rekognition.create_collection(CollectionId=COLLECTION)
        print(f"Collection '{COLLECTION}' created successfully")
    except rekognition.exceptions.ResourceAlreadyExistsException:
        print(f"Collection '{COLLECTION}' already exists")

def upload_to_s3(image_path, s3_key):
    s3.upload_file(image_path, BUCKET, s3_key)
    url = f"https://{BUCKET}.s3.amazonaws.com/{s3_key}"
    return url

def recognize_face(image_path):
    with open(image_path, 'rb') as f:
        image_bytes = f.read()
    try:
        response = rekognition.search_faces_by_image(
            CollectionId=COLLECTION,
            Image={'Bytes': image_bytes},
            MaxFaces=1,
            FaceMatchThreshold=80
        )
        if response['FaceMatches']:
            match = response['FaceMatches'][0]
            name = match['Face']['ExternalImageId']
            confidence = match['Face']['Confidence']
            return 'known', name, confidence
        else:
            return 'unknown', None, None
    except Exception as e:
        print(f"Rekognition error: {e}")
        return 'unknown', None, None

def log_to_dynamodb(timestamp, identity, image_url, status):
    table = dynamodb.Table(TABLE)
    table.put_item(Item={
        'timestamp': timestamp,
        'identity': identity,
        'image_url': image_url,
        'status': status
    })

def register_known_face(image_path, name):
    s3_key = f"known-faces/{name}.jpg"
    s3.upload_file(image_path, BUCKET, s3_key)
    with open(image_path, 'rb') as f:
        image_bytes = f.read()
    rekognition.index_faces(
        CollectionId=COLLECTION,
        Image={'Bytes': image_bytes},
        ExternalImageId=name,
        DetectionAttributes=['ALL']
    )
    print(f"Registered {name} successfully")
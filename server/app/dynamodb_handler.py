import boto3
from decouple import config
from flask import Blueprint

bp = Blueprint('dynamodb', __name__, url_prefix='/dynamodb')

AWS_ACCESS_KEY_ID     = config("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = config("AWS_SECRET_ACCESS_KEY")
REGION_NAME           = config("REGION_NAME")


client = boto3.client(
    'dynamodb',
    aws_access_key_id     = AWS_ACCESS_KEY_ID,
    aws_secret_access_key = AWS_SECRET_ACCESS_KEY,
    region_name           = REGION_NAME,
)

resource = boto3.resource(
    'dynamodb',
    aws_access_key_id     = AWS_ACCESS_KEY_ID,
    aws_secret_access_key = AWS_SECRET_ACCESS_KEY,
    region_name           = REGION_NAME,
)

def CreatATableImages():
    client.create_table(
        AttributeDefinitions = [ # Name and type of the attributes 
            {
                'AttributeName': 'id', # Name of the attribute
                'AttributeType': 'S'   # N -> Number (S -> String, B-> Binary)
            }
        ],
        TableName = 'Images', # Name of the table 
        KeySchema = [       # Partition key/sort key attribute 
            {
                'AttributeName': 'id',
                'KeyType'      : 'HASH' 
                # 'HASH' -> partition key, 'RANGE' -> sort key
            }
        ],
        BillingMode = 'PAY_PER_REQUEST',
        Tags = [ # OPTIONAL 
            {
                'Key' : 'test-resource',
                'Value': 'dynamodb-test'
            }
        ]
    )

ImagesTable = resource.Table('Images')

def addItemToImages(id, path, description):
    response = ImagesTable.put_item(
        Item = {
            'id'     : id,
            'path'  : path,
            'description' : description,
        }
    )
    return response
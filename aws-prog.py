import boto3
import json
ec2 = boto3.client('ec2')
response = ec2.describe_instances()
r=response['Reservations']
for i in r:
    instances = i["Instances"][0]
    print(instances["InstanceId"])


dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('docker_keys')

response = table.get_item(
    Key={
        'key': 'manager'
    }
)

item = response['Item']
print(item['value'])
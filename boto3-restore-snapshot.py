import boto3

session = boto3.Session(profile_name='aranga-dev')
#get the lis tof 

client = session.client('rds',region_name='ap-southeast-2')
response = client.describe_db_cluster_snapshots()

sortedList = response['DBClusterSnapshots']

sortedList.sort(key=lambda k:k['SnapshotCreateTime'],reverse=True)


for s in sortedList:
    if s['DBClusterSnapshotArn'].startswith('auto'):
       print(s['DBClusterSnapshotArn'],"\n\n")

#response = client.describe_db_clusters()
#print(response)

'''
session = boto3.Session(profile_name='aranga-dev')

client = session.client('cloudformation',region_name='ap-southeast-2')

response = client.create_stack(
	StackName="bauuat-aurora-1212",
	TemplateURL="https://s3-ap-southeast-2.amazonaws.com/aranga-dev.cft/aurora-instance.template",
	Capabilities=['CAPABILITY_IAM','CAPABILITY_NAMED_IAM']

		
'''
	

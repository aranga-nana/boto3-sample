import boto3

ec2 = boto3.client('ec2',region_name='ap-southeast-2')
filters = [{'Name': 'tag:Name', 'Values': ['linear.bau*'] }]
reservations=ec2.describe_instances(Filters=filters)
for r in reservations['Reservations']:
    for i in r['Instances']:
        print(i['InstanceId'])
        tags =i['Tags']
        for t in tags:
            print(t['Key'],":", t['Value'],"\n")



autoscale = boto3.client('autoscaling',region_name='ap-southeast-2')
response = autoscale.describe_auto_scaling_groups()
name=response['AutoScalingGroups'][0]['AutoScalingGroupName']
response = autoscale.suspend_processes(AutoScalingGroupName=name)
#response = autoscale.resume_processes(AutoScalingGroupName=name)
print(response)

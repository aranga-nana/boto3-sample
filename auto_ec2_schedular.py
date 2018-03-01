import pytz
import boto3
import datetime
import time
import calendar
from datetime import timedelta
TIME_FORMAT = '%Y-%m-%d %H:%M:%S'

dat = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


local_tz = pytz.timezone ("Australia/Sydney")
datetime_without_tz = datetime.datetime.strptime(dat, "%Y-%m-%d %H:%M:%S")
datetime_with_tz = local_tz.localize(datetime_without_tz) # No daylight saving time
ch= datetime_with_tz.hour
cm= datetime_with_tz.minute

d={"1":"name"}

def findstop(tags):
   v =""
   for x in tags:
	if x['Key'] == 'time:stop':
	   v = x['Value']
   return v
def stopInstance(ec2,iid):
    print('stopiing instance ',iid)
    print ec2.stop_instances(InstanceIds=[iid])   	

def suspendAsg(name):
    client = boto3.client('autoscaling',region_name='ap-southeast-2') 
    print client.suspend_processes(AutoScalingGroupName=name)   


def initaliseall():
    client = boto3.client('autoscaling',region_name='ap-southeast-2')
    response = client.describe_auto_scaling_groups()
    #print response
    #nextToken = response['NextToken']  
    asgs = response['AutoScalingGroups']
    for asg in asgs:
        #print asg['AutoScalingGroupName'],'\n'
        for instance in asg['Instances']:
            iid= instance['InstanceId']
            d[iid] = asg['AutoScalingGroupName']
            
            #d[iid]= asg['AutoScalingGroupName']
initaliseall()
print d

print '============================================='
ec2 = boto3.client('ec2',region_name='ap-southeast-2')
filters = [{'Name': 'tag:Name', 'Values': ['linear*'] },{'Name':'tag:stopinator','Values':['true']}]
reservations=ec2.describe_instances(Filters=filters)
for r in reservations['Reservations']:
    #print(r,"\n\n")
    #print(r,"=======================================")
    for i in r['Instances']:
        iid=i['InstanceId']
        print('checking instance id',iid)
        date= i.get('LaunchTime')
        tags =i['Tags']
        print tags
        strTime = findstop(tags)
	timepart= strTime.split(':')
        print "current",ch,";",cm
        h= int(timepart[0])
	m= int(timepart[1]) 
        print "instance",h,";",m
        print cm > m
        stated = i['State']
        stateId = stated.get('Code') 
        print stateId
        if stateId == 16 or stateId == 0:
	   if ch > h:
              stopInstance(iid)
           if h==ch and cm >= m:
              print "about to stop",iid
              if iid in d:
                 suspendAsg(d[iid]) 
              time.sleep(0.300)               
              stopInstance(ec2,iid) 


#autoscale = boto3.client('autoscaling',region_name='ap-southeast-2')
#response = autoscale.describe_auto_scaling_groups()
#name=response['AutoScalingGroups'][0]['AutoScalingGroupName']
#response = autoscale.suspend_processes(AutoScalingGroupName=name)
#response = autoscale.resume_processes(AutoScalingGroupName=name)
#print(response)

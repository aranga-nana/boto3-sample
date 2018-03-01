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

def start_end_time(arg,tags):
   v =""
   r[0]=11121212
   r[1]=2323323
   for x in tags:
	if x['Key'] == arg:
	   v = x['Value']
           timepart= v.split(':')
           r[0]= int(timepart[0])
           r[1]=int(timepart[1])

   return r

def stopInstance(ec2,iid):
    #print('stopiing instance ',iid)
    print ec2.stop_instances(InstanceIds=[iid]) 
  	
def startInstances(ec2,iid):
    print ec2.start_instances(InstanceIds=[iid])


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

            
initaliseall()

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
        #print tags
        ## stop
        r = start_end_time('time:stop',tags)
        print "instance",r[0],";",r[1]
        stated = i['State']
        stateId = stated.get('Code') 
        print stateId
        executeStop = False
        if stateId == 16 or stateId == 0:
	   if ch > r[0]:
              if iid in d:
                 suspendAsg(d[iid])
              time.sleep(0.300)
              stopInstance(ec2,iid)
              executeStop = True
           if ch == r[0] and cm >= r[1]:
              print "about to stop",iid
              if iid in d:
                 suspendAsg(d[iid]) 
              time.sleep(0.300)               
              stopInstance(ec2,iid)
              executeStop = True 
        ## start
          
        if not executeStop:
           r = start_end_time('time:start',tags)
           print "instance",r[0],";",r[1]
           if stateId == 80 or stateId == 64:
              if ch > r[0]:
                 startInstances(ec2,iid)                 
              if ch == r[0] and cm >= r[1]:
                 startInstances(ec2,iid)

''' 
        stated = i['State']
        stateId = stated.get('Code')
        print stateId
        if stateId == 16 or stateId == 0:
           if ch > r[0]:
              if iid in d:
                 print()
                 #suspendAsg(d[iid])
              #startInstance(iid)
           if ch == r[0] and cm >= r[1]:
              print "about to stop",iid
              if iid in d:
                 #suspendAsg(d[iid])
                 print() 
              time.sleep(0.300)
              #stopInstance(ec2,iid)

'''
#autoscale = boto3.client('autoscaling',region_name='ap-southeast-2')
#response = autoscale.describe_auto_scaling_groups()
#name=response['AutoScalingGroups'][0]['AutoScalingGroupName']
#response = autoscale.suspend_processes(AutoScalingGroupName=name)
#response = autoscale.resume_processes(AutoScalingGroupName=name)
#print(response)

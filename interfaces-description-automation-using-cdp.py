#Importing Libraries
import requests
import json

#to create interface structure using 1/1 for example, we need regex library in python with below import.
import re

#Setting Variables
switchuser = input('username is: ')
switchpassword = input('Password is: ') 

#Enhancing variable input to be once entering switch IP
Targetedswitch = input('Targeted Switch IP is: ')
url = 'https://'+Targetedswitch+'/ins'

#Http requests parameters
myurl = url
myheader = {'content-type':'application/json'}

#Cheating payload from nxapi sandbox in mode cli_show & model is JSON
mypayload = {
  "ins_api": {
    "version": "1.0",
    "type": "cli_show",
    "chunk": "0",
    "sid": "sid",
    "input": "show cdp neighbor",
    "output_format": "json"
  }
}

#Defining response in json dictionary format
response = requests.post(myurl, data=json.dumps(mypayload), headers=myheader, auth=(switchuser,switchpassword),verify=False).json()
#After debugging, print(response) has no use, so we can ignore it by adding it as a comment only
#print(response)

#Login with nxapi REST 
auth_url =  'https://'+Targetedswitch+'/api/mo/aaaLogin.json'
auth_body = {"aaaUser": {"attributes": {"name": switchuser, "pwd":switchpassword}}}

auth_response = requests.post(auth_url, data=json.dumps(auth_body), timeout=5, verify=False).json()
token = auth_response['imdata'][0]['aaaLogin']['attributes']['token']
cookies={}
cookies['APIC-cookie']=token
#After debugging, print(cookies) has no use, so we can ignore it by adding it as a comment only
#print(cookies)

#As we have data from show cdp neighbor, we need to count the interfaces that we will configure them automatically.
counter = 0
nei_count = response['ins_api']['outputs']['output']['body']['neigh_count']
print('The neighbor numbers are: ' + str(nei_count))

#After that we need to loop that based on number of neighbors, we are going to interface description using NXAPI REST
while counter < nei_count:
    hostname = response ['ins_api']['outputs']['output']['body']['TABLE_cdp_neighbor_brief_info']['ROW_cdp_neighbor_brief_info'][counter]['device_id']
    local_int = response ['ins_api']['outputs']['output']['body']['TABLE_cdp_neighbor_brief_info']['ROW_cdp_neighbor_brief_info'][counter]['intf_id']
    remote_int = response ['ins_api']['outputs']['output']['body']['TABLE_cdp_neighbor_brief_info']['ROW_cdp_neighbor_brief_info'][counter]['port_id']
    body = {'l1PhysIf': {'attributes': {'descr':'Connected to ' + hostname +  ' interface remote ' + remote_int}}}
    counter += 1
    if local_int != 'mgmt0':
        int_name = str.lower(str(local_int[:3]))
        int_num = re.search(r'[1-9]/[1-9]*',local_int)
        int_url = 'https://'+Targetedswitch+'/api/mo/sys/intf/phys-['+int_name +str(int_num.group(0))+'].json'
        post_response = requests.post(int_url, data=json.dumps(body), headers=myheader, cookies=cookies, verify=False).json()
        print(post_response)

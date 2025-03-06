import requests
import json
import re

switchuser = 'admin'
switchpassword = 'Admin_1234!'

url = 'https://sbx-nxos-mgmt.cisco.com/ins'
myheaders = {'content-type': 'applicationjson'}
payload = {
  "ins_api": {
    "version": "1.0",
    "type": "cli_show",
    "chunk": "0",
    "sid": "sid",
    "input": "show cdp nei",
    "output_format": "json"
  }
}

response = requests.post(
    url,
    headers=myheaders,
    data=json.dumps(payload),
    auth=(switchuser, switchpassword),
    verify=False
).json()

#################### LOGIN WITH NX-API REST ####################

auth_url = 'https://sbx-nxos-mgmt.cisco.com/api/aaaLogin.json'
auth_body = {
    'aaaUser': {
        'attributes': {
            'name': 'admin',
            'pwd': 'Admin_1234!'
        }
    }
}
auth_response = requests.post(auth_url,
                              data=json.dumps(auth_body),
                              timeout=5,
                              verify=False).json()

token = auth_response['imdata'][0]['aaaLogin']['attributes']['token']
cookies={}
cookies['APIC-cookie']=token

counter = 0
nei_count = response['ins_api']['outputs']['output']['body']['neigh_count']
print(nei_count)

while counter < nei_count:
    hostname = response['ins_api']['outputs']['output']['body']['TABLE_cdp_neighbor_brief_info']['Row_cdp_neighbor_brief_info']['counter']['device_id']
    local_int = response['ins_api']['outputs']['output']['body']['TABLE_cdp_neighbor_brief_info']['Row_cdp_neighbor_brief_info']['counter']['intf_id']
    remote_int = response['ins_api']['outputs']['output']['body']['TABLE_cdp_neighbor_brief_info']['Row_cdp_neighbor_brief_info']['counter']['port_id']

    body = {
        "l1PhysIf": {
            "attributes": {
                "descr": 'Connected to '+hostname+' Remote if is '+remote_int
            }
        } 
    }
    counter += 1

    if local_int != 'mgmt0':
        int_name = str.lower(str(local_int[:3]))
        int_num = re.search(r'[1-9]/[1-9]*', local_int)
        int_url = 'https://sbx-nxos-mgmt.cisco.com/api/mo/sys/intf/phys-['+int_name+str(
            int_num.group(0))+'].json'
        post_response = requests.post(int_url, 
                                      data=json.dumps(body), 
                                      header=myheaders, 
                                      cookies=cookies, 
                                      verify=False).json
        print(post_response)






 
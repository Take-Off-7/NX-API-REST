import requests
import json
import re

switchuser = 'admin'
switchpassword = #(your_password_goes_here)

url = 'https://sbx-nxos-mgmt.cisco.com/ins'
myheaders = {'content-type': 'applicationjson'}
payload = {
  "ins_api": {
    "version": "1.0",
    "type": "cli_show",
    "chunk": "0",
    "sid": "sid",
    "input": "show int",
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
            'pwd': #(your_password_goes_here)
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

#################### AUTOMATE DESCRIPTION FOR MANY INTERFACES ####################

counter = 0
total_if = 10

while counter < total_if:
    interface = response['ins_api']['outputs']['output']['body']['TABLE_interface']['ROW_interface'][counter]['interface']

    payload = {
        'l1PhysIf': {
            'attributes': {
                #'descr': f'TakeOff was in {interface}'
                'descr': ""
            }
        }
    }

    counter += 1

    if interface != 'mgmt0':
        int_name = str.lower(str(interface)[:3])
        int_num = re.search(r'[1-9]/[1-9]*', interface)
        int_url = f'https://sbx-nxos-mgmt.cisco.com/api/node/mo/sys/intf/phys-[{int_name}{str(int_num.group(0))}].json'
        
        post_response = requests.post(
            int_url,
            data=json.dumps(payload),
            cookies=cookies,
            verify=False
        ).json()

        #################### TO GET THE DESCRIPTION OF EACH CONFIGURED INTERFACE ####################

        get_response = requests.get(
            int_url,
            cookies=cookies,
            verify=False
        ).json()

        descr = get_response['imdata'][0]['l1PhysIf']['attributes']['descr']
        print(descr)


    




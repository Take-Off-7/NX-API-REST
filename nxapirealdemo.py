import requests
import json
from nxapidemoreal import cookies
from pprint import pprint

#################### PUT DESCR WITH NX-API REST ####################

link = 'https://sbx-nxos-mgmt.cisco.com/api/node/mo/sys/intf/phys-[eth1/1].json'

payload = {
    'l1PhysIf': {
        'attributes': {
            'descr': ''
        }
    }
}

response = requests.put(link,
                        data=json.dumps(payload),
                        cookies=cookies,
                        verify=False
                        ).json()

#################### GET DESCR WITH NX-API REST ####################

url = 'https://sbx-nxos-mgmt.cisco.com/api/node/mo/sys/intf/phys-[eth1/1].json'

response = requests.get(url,
                        cookies=cookies,
                        verify=False
                        ).json()

descr = response['imdata'][0]['l1PhysIf']['attributes']['descr']
print(descr)

from tenable.io import TenableIO
import requests
import json
import random, string
import pandas as pd 
import csv
import os
import re

scan_running = True
export_status = True

tio = TenableIO(
    access_key='cf81be6d9f5d5a01a197ccaec2010dca667e95f5ef2d4b14e0d2d18e4d4d36ab',
    secret_key='600a16e9302be0cc0f8ef3dd43f65190c968a9f81fbbbc5cf765803cc22e7c38'
)

url = "https://cloud.tenable.com/scans/"

for cred in tio.credentials.list():
#    print(cred)
    if cred['name'] == 'Nessus SSH KEY':
         uuid = cred["uuid"]

"""
Generate random string
"""
def randomword(length):
   letters = string.ascii_lowercase
   return ''.join(random.choice(letters) for i in range(length))

random_string = randomword(10)

new_host_scan2 = tio.scans.create(
    name="ma_Habana_new_scan" + random_string,
    template='advanced',
    credentials={'Host': {'SSH': [{'id': uuid}]}},
   # tags = {'M&A: Habana'},
    scanner='nessus-tenable-01-srv',
    targets=['10.111.59.72'],
)


scans = tio.scans.list()
for scan in scans:
    if scan["name"] == new_host_scan2['name']:
        new_scan_id=scan["id"]


new_scan_id_str=str(new_scan_id)
"""
tio.scans.launch(new_scan_id)





while scan_running == True:
        scan_status_reader = tio.scans.status(new_scan_id)
        if scan_status_reader == 'completed':
            scan_running=False
        else:
             print("scan in progress at status", scan_status_reader)

"""


new_scan_id_str=("1231")  # to del
new_scan_id = 1231



url_for_export = url + new_scan_id_str
url_for_export = url_for_export + "/export"
print("new url is ", url_for_export)



payload = { "format": "csv" }
headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "X-ApiKeys": "accessKey=cf81be6d9f5d5a01a197ccaec2010dca667e95f5ef2d4b14e0d2d18e4d4d36ab;secretKey=600a16e9302be0cc0f8ef3dd43f65190c968a9f81fbbbc5cf765803cc22e7c38"
}

response = requests.post(url_for_export, json=payload, headers=headers)



file_id = response.text
dict_file_id=json.loads(file_id)

type(dict_file_id)
print(dict_file_id.get("file"))

file_id = dict_file_id.get("file")



url_for_status = url_for_export

url_for_status = url_for_status + "/"
#url_for_status = url_for_status + str(new_scan_id)
#url_for_status = url_for_status + "/"
url_for_status = url_for_status + str(file_id)
url_for_status = url_for_status + "/status"

print("new status url is ", url_for_status)

while export_status == True:
    headers = {
        "accept": "application/octet-stream",
        "X-ApiKeys": "accessKey=cf81be6d9f5d5a01a197ccaec2010dca667e95f5ef2d4b14e0d2d18e4d4d36ab;secretKey=600a16e9302be0cc0f8ef3dd43f65190c968a9f81fbbbc5cf765803cc22e7c38"
    }
    response = requests.get(url_for_status, headers=headers)
    respons_dict = json.loads(response.text)
    print(respons_dict["status"])
    export_status = respons_dict["status"]
    if export_status == 'ready':
         export_status = False
    




url_for_download = url_for_export

url_for_download = url_for_download + "/"
url_for_download = url_for_download + str(file_id)
url_for_download = url_for_download + "/download"

print(url_for_download)

headers = {
    "accept": "application/octet-stream",
    "X-ApiKeys": "accessKey=cf81be6d9f5d5a01a197ccaec2010dca667e95f5ef2d4b14e0d2d18e4d4d36ab;secretKey=600a16e9302be0cc0f8ef3dd43f65190c968a9f81fbbbc5cf765803cc22e7c38"
}

response = requests.get(url_for_download, headers=headers)

scan_output=response.text

print(scan_output)
file_one = open("scan_output.csv", "w")
file_one.write(scan_output)

df = pd.read_csv('scan_output.csv')

df = df[['Risk', 'Plugin Output', 'FQDN']]
df.to_csv('scan_output.csv', index=False)   








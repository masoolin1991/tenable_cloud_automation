
from tenable.io import TenableIO

scan_running = True

#credentials = {"uuid":"null"}

tio = TenableIO(
    access_key='cf81be6d9f5d5a01a197ccaec2010dca667e95f5ef2d4b14e0d2d18e4d4d36ab',
    secret_key='600a16e9302be0cc0f8ef3dd43f65190c968a9f81fbbbc5cf765803cc22e7c38'
)

for cred in tio.credentials.list():
    print(cred)
    if cred['name'] == 'Nessus SSH KEY':
         uuid = cred["uuid"]
#         id = cred["id"]


print("uuid is", uuid)

cred = tio.credentials.details(uuid)
print(" cred is ", cred)

#new_host_scan = tio.scans.create(
#    name='ma_Habana_Example_scan',
#    scanner='nessus-tenable-srv',
#    targets=['10.111.59.72'],
#)

new_host_scan2 = tio.scans.create(
    name="ma_Habana_new_scan",
    template='advanced',
    credentials={'Host': {'SSH': [{'id': uuid}]}},
    scanner='nessus-tenable-srv',
    targets=['10.111.59.72'],
)

print(new_host_scan2)
scans = tio.scans.list()
for scan in scans:
    print(f'Scan {scan["id"]} is named {scan["name"]}')
    

scans = tio.scans.list()
for scan in scans:
    print(f'Scan {scan["id"]} is named {scan["name"]}')
    if scan["name"] == "ma_Habana_new_scan":
        new_scan_id=scan["id"]

print(new_scan_id)

#tio.scans.configure(new_scan_id, credentials='Nessus SSH KEY')
tio.scans.launch(new_scan_id)

"""

tio.scans.launch(851,targets=['10.111.59.72'])
"""
while scan_running == True:
        scan_status_reader = tio.scans.status(new_scan_id)
        if scan_status_reader == 'completed':
            scan_running=False
        else:
             print("scan in progress at status", scan_status_reader)

















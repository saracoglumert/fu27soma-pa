from redis import Redis
import requests
import json
import random
import string
import time

url_node1 = "http://10.10.10.201:10000/" #alice
url_node2 = "http://10.10.10.202:10000/" #faber

conn = Redis.from_url(url="redis://10.10.10.200:7000")

alias = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8))

# Step 1 - Create Invitation (node2 - faber)
body = json.loads('{"service_endpoint": "http://10.10.10.202:9000"}')
r=requests.post(url = url_node2+'connections/create-invitation?alias={}'.format(alias), json=body)
cid = json.loads(r.content)['invitation']['@id']
response1 = json.dumps((json.loads(r.content)['invitation']), sort_keys=True, indent=4)
time.sleep(1.5)

# Step 2 - Receive Invitation (node1 - alice)
body = response1
r=requests.post(url = url_node1+'connections/receive-invitation?alias={}'.format(alias), json=body)
cid = json.loads(r.content)['connection_id']
response2 = json.loads(r.content)['connection_id']
time.sleep(1.5)

# Step 3 - Accept Invitation (node1 - alice)
x = url_node1+'connections/{}/accept-invitation?my_label={}&my_endpoint={}'.format(response2,alias,"http://10.10.10.201:9000")
r=requests.post(url = x)
response3 = json.loads(r.content)
time.sleep(1.5)

# Step 4 - Accept Request (node2 - faber)
response4 = json.loads(conn.lrange(str.encode('acapy-record-with-state-base'), -1, -1)[0].decode("utf-8"))['payload']['payload']['connection_id']
x = url_node2+'connections/{}/accept-request?my_endpoint={}'.format(response4,"http://10.10.10.202:9000")
r=requests.post(url = x)
response5 = r.content
time.sleep(5)

conn_id_node1 = response2
conn_id_node2 = response4

print("Connection Alias         : {}".format(alias))
print("Connection ID for Node 1 : {}".format(conn_id_node1))
print("Connection ID for Node 2 : {}".format(conn_id_node2))

# New function - Register into Server - Ledger
# Create & Register DID - Node 1

# Create & Register DID - Node 2

# Create & Register Schema - Node 1

# Create & Register Schema - Node 2

# Create & Register CredDef - Node 1

# Create & Register CredDef - Node 2


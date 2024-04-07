import yaml
import requests
import json

with open('config.yaml', 'r') as file:
    conf = yaml.safe_load(file)

API_node1 = "http://{}:{}/".format(conf['node1']['ip'],conf['node1']['admin'])
API_node2 = "http://{}:{}/".format(conf['node2']['ip'],conf['node2']['admin'])

cid = ''

class Node():
    def __init__(self,endpoint):
        self.ip = endpoint

    def inv_create(self):
        global cid
        body = json.loads('{}')

        r=requests.post(url = API_node2+'connections/create-invitation', json=body)
        cid = json.loads(r.content)['invitation']['@id']
        return json.dumps((json.loads(r.content)['invitation']), sort_keys=True, indent=4)
    
    def inv_receive(body):
        r=requests.post(url = API_node1+'connections/receive-invitation', json=body)
        cid = json.loads(r.content)['connection_id']
        return json.loads(r.content)['connection_id']
        #return '\'invitation\':' + str(json.loads(r.content)['invitation'])

    def inv_accept(conn_id):
        x = API_node1+'connections/{}/accept-invitation'.format(conn_id)
        r=requests.post(url = x)
        return json.loads(r.content)

    def req_accept(req_id):
        x = API_node2+'connections/{}/accept-request'.format(req_id)
        print(x)
        r=requests.post(url = x)
        return r.content

# node2
def create_invitation():
    global cid
    body = json.loads('{}')

    r=requests.post(url = API_node2+'connections/create-invitation', json=body)
    cid = json.loads(r.content)['invitation']['@id']
    return json.dumps((json.loads(r.content)['invitation']), sort_keys=True, indent=4)

# node1
def receive_invitation(body):
    r=requests.post(url = API_node1+'connections/receive-invitation', json=body)
    cid = json.loads(r.content)['connection_id']
    return json.loads(r.content)['connection_id']
    #return '\'invitation\':' + str(json.loads(r.content)['invitation'])

# node1
def accept_invitation(conn_id):
    x = API_node1+'connections/{}/accept-invitation'.format(conn_id)
    r=requests.post(url = x)
    return json.loads(r.content)

# node2
def accept_request(req_id):
    x = API_node2+'connections/{}/accept-request'.format(req_id)
    print(x)
    r=requests.post(url = x)
    return r.content

#a = create_invitation()
#print(a)
#b = receive_invitation(a)
#print('Connection ID :' + b)
#c = accept_invitation(b)
#print(c)
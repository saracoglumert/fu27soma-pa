# fu27soma-pa

# 1. Installation
After a clean installation of Proxmox on a host machine, SSH into it and run the following code block.

```
apt update -y
apt upgrade -y
apt install git -y
apt install sshpass -y
cd -L
git clone https://github.com/saracoglumert/fu27soma-pa.git
cd fu27soma-pa
chmod +x manage.py
```

This will clone the repository to your machine, install the dependencies required for the **manage script** to work and make it an executable. After that, **manage script** can be used to interact with Proxmox and the host machine.

Before starting to build the project, **config.yaml** file must be set according to your network configuration. You **have to** set *host/network_gateway*, *node1/network_ip* and *node2/network_ip* values in a way suitable for your network infrastructure, otherwise the build will fail. **manage script** can you help you with this aswell. Run the script with the following argument and you will see suggestions. Other key values are still open for change, but not mandatory.

```
./manage.py config
```

After editing the **config.yaml** file, run the following command to build the nodes and get them running. The build may take between 15 to 30 minutes depending on your internet connection.
```
./manage.py build
```

Other possible commands are,
```
./manage.py start
./manage.py stop
./manage.py destroy
./manage.py help
```

# 2. Notes
## Procedure
- Register TÜV
- Register Nodes
- Register Product
- Connect Node
- Issue Credential
- Request Proof


# 3. To-Do

## Must
- New UI -- p1
- autopep8
- manage script - status/endpoints -- p2
- OpenAPI Tutorial -> Issue credential / Request proof -- p3
- SD-JWT with PCF in Payload -- p6
- Telegraf / InfluxDB Open Source


## Optional
- change time_sleep name to step
- use disown instead of sshpass
- Update to aca-py v0.12.1
- remove Tails? (build, start, manage, config)
- Prettify logs.
- remove MAC address definition

## Future
- Telegraf and InfluxDB
- OOP manage.py

## Further Reading
- https://github.com/hyperledger/aries-cloudagent-python/issues/1263
- http://aca-py.org
- https://medium.com/@rajatpachauri12345/what-are-redis-cluster-and-how-to-setup-redis-cluster-locally-69e87941d573
- https://github.com/bcgov/von-network/blob/main/docs/UsingVONNetwork.md#building-and-starting
- https://github.com/hyperledger/aries-cloudagent-python/blob/main/docs/demo/AriesOpenAPIDemo.md#sending-a-message-from-alice-to-faber
- https://github.com/hyperledger/aries-cloudagent-python/blob/main/docs/demo/README.md
- https://github.com/hyperledger/aries-cloudagent-python/issues/2124
- https://ldej.nl/post/becoming-a-hyperledger-aries-developer-part-3-connecting-using-swagger/
- https://github.com/bcgov/aries-acapy-plugin-redis-events
- https://github.com/bcgov/openshift-aries-mediator-service
- https://github.com/bcgov/openshift-aries-mediator-service/tree/main/openshift/templates/aries-mediator-agent
- https://github.com/bcgov/openshift-aries-mediator-service/tree/main/openshift/templates/redis
- https://github.com/bcgov/openshift-aries-mediator-service/blob/main/openshift/templates/redis/redis-cluster-deploy.yaml#L1-L37

# To New aca-py Version
https://ldej.nl/post/becoming-a-hyperledger-aries-developer-part-3-connecting-using-didcomm-exchange/
Basically, the /connections/create-invitation and /connections/receive-invitation endpoints have been replaced with the Out-of-Band endpoints /out-of-band/create-invitation and /out-of-band/receive-invitation. Similarly, the /connections/{conn_id}/accept-invitation and /connections/{conn_id}/accept-request endpoints have been replaced with the DID Exchange endpoints /didexchange/{conn_id}/accept-invitation and /didexchange/{conn_id}/accept-request. This makes that the other /connections endpoints are just there to manage connections.

## Notes To Self
Possible Public Ledgers
- https://idu.cloudcompass.ca
- http://test.bcovrin.vonx.io
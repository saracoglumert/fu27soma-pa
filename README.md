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

After editing the **config.yaml** file, run the following command to build the nodes and get them running. The build may between 15 to 30 minutes depending on your internet connection.
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
## Roles
- Issuer (One issues for own product)
- Holder & Verifier (One asks proof for others' products)

# 3. To-Do

## Must
- Notifications - implement timestamp -- p2
- Integration with UI - Notifications -- p2
- manage script - status -- p3
- OpenAPI Tutorial -> Issue credential / Request proof -- p4
- Change Schema as PCF -- p5
- SD-JWT with PCF in Payload -- p6

## Optional
- cleaner file/folder structure in containers
- rename object Node to Company
- Convert Server UI to Web Server (instead of Flask) -- p1
- change time_sleep name to step
- get snapshot name from config_yaml
- use disown instead of sshpass
- Update DB Structure in update function
- Update to aca-py v0.12.1
- python library (app,web,lib,db)
- remove Tails? (build, start, manage, config)
- Prettify logs.
- remove MAC address definition

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

## Notes To Self
Possible Public Ledgers
- https://idu.cloudcompass.ca
- http://test.bcovrin.vonx.io
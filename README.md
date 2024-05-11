# fu27soma-pa

# 1. Installation
After a clean installation of Proxmox on a host machine, SSH into it and run the following code block.

```
apt update -y
apt upgrade -y
apt install git -y
apt install git sshpass -y
cd -L
git clone https://github.com/saracoglumert/fu27soma-pa.git
cd fu27soma-pa
chmod +x manage.py
```

This will clone the repository to your machine, install the dependencies required for the **manage script** to work and make it an executable. After that, **manage script** can be used to interact with Proxmox and the host machine.

Before starting to use **manage script**, **config.yaml** file must be set according to your network configuration, otherwise the build will fail. In order to build the project successfully, you **have to** set *host/network_gateway*, *node1/network_ip* and *node2/network_ip* values in a way suitable for your network infrastructure. Other key values are still open for change, but not mandatory.

After editing the **config.yaml** file, run the following command to build the nodes and get them running. The build may take up to 20 minutes depending on your internet connection.
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

## To-Do
- Complete network scanner in manage script (and add to README)
- Insert endpoints and ips into db.sql
- UI on server node for endpoints
- Solve problems with aca-py Redis plugin integration
- Access Redis cluster from Python
- Complete connection procedure
- UI for connection
- SD-JWT with PCF in Payload

## Further Reading
- https://github.com/bcgov/von-network/blob/main/docs/UsingVONNetwork.md#building-and-starting
- https://github.com/hyperledger/aries-cloudagent-python/blob/main/docs/demo/AriesOpenAPIDemo.md#sending-a-message-from-alice-to-faber
- https://github.com/hyperledger/aries-cloudagent-python/blob/main/docs/demo/README.md
- https://github.com/hyperledger/aries-cloudagent-python/issues/2124
- https://ldej.nl/post/becoming-a-hyperledger-aries-developer-part-3-connecting-using-swagger/
- https://github.com/bcgov/aries-acapy-plugin-redis-events

## Notes To Self
Possible Public Ledgers
- https://idu.cloudcompass.ca
- http://test.bcovrin.vonx.io
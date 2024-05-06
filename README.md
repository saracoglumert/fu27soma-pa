# fu27soma-pa

# 1. Installation
After a clean installation of Proxmox on a host machine, SSH into it and run the following code block.

```
cd -L
https://github.com/saracoglumert/fu27soma-pa.git
cd fu27soma-pa
apt update -y
apt upgrade -y
apt install git sshpass -y
chmod +x manage.py
```

This will clone the repository to your machine, install the dependencies required for the **manage script** to work and make it an executable. After that, **manage script** can be used to interact with Proxmox and the host machine.

Run the following command to build the nodes and get them running.

```
./manage.py build
```

Other possible commands are,

```
./manage.py start
./manage.py stop
```


## To-Do
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
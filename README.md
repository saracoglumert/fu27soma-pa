# fu27soma-project

# 1. Configuration
## 1.1 Host Machine
This repo runs on Proxmox VE 8. Please download it [here](https://www.proxmox.com/en/proxmox-virtual-environment/overview) and install it on a physical or virtual machine. SSH into the machine and follow the procedures below.

The physical machine used for demonstration has the following specifications.
- **Processor :** Intel i5-6500T
- **Memory :** 8 GiB
- **Disk :** 64 GiB
## 1.2 Dependencies
```
git clone https://github.com/saracoglumert/fu27soma-project
cd fu27soma-project
```

First, run **init.sh** script. It will download and install all dependencies, set the permissions, analyze your network and come up with a suggestion for network setup.
```
bash init.sh
```

## 1.3 Network Setup
```
Analyzing network

Found suitable chunk:
Gateway       : 10.10.136.254
IP [server]   : 10.10.136.200
IP [node1]    : 10.10.136.201
IP [node2]    : 10.10.136.202
```

Accorindg to the output from **init.sh**, please edit the *conf/gateway**, **server/ip**, **node1/ip** and **node2/ip** parameters in **config.yaml** file. You can also tinker with other paramters to your liking or your specific network infrastructure.

# 2. Installation
The following command, builds the containers and installs the Hyperledger Indy (von-network) and Hyperledger Aries (aries-cloundagent-python) packages.
```
./manage build
```
To start the nodes, run the following command.
```
./manage start
```
If you want to stop the nodes or destroy the containers, use the following commands.
```
./manage stop
./manage destroy
```
# 3. Architecture and Endpoints
![alt text](https://github.com/saracoglumert/fu27soma-project/blob/main/thesis/img/arch.png)

Container configuration:
- **Disk :** 16 GiB
- **Memory :** 1024 MiB

# 3. Endpoints
| **Description**           | **URL**                         |
|---------------------------|---------------------------------|
| **Server**                | http://10.10.136.200:9000       |
| **Node 1**                | http://10.10.136.201:10001      |
| **Node 2**                | http://10.10.136.202:10002      |

Please note that, the URL for endpoints will probably change in your case, according to your network structure. Refer to *1.3 Network Setup*.

# References

https://github.com/bcgov/von-network/blob/main/docs/UsingVONNetwork.md#building-and-starting

https://github.com/hyperledger/aries-cloudagent-python/blob/main/docs/demo/AriesOpenAPIDemo.md#sending-a-message-from-alice-to-faber

https://github.com/hyperledger/aries-cloudagent-python/blob/main/docs/demo/README.md

Architecture problems
https://github.com/hyperledger/aries-cloudagent-python/issues/2124

https://ldej.nl/post/becoming-a-hyperledger-aries-developer-part-3-connecting-using-swagger/

# To-Do
- improve manage script (pipe outputs to logs)
- init
- manage script arguments
- implement controller

# Notes To Self
LEDGER_URL=http://test.bcovrin.vonx.io
ssh-keygen -R hostname
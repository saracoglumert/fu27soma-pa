# fu27soma-project

# 1. Configuration
## 1.1 Host Machine
This repo runs on Proxmox VE 8. Please download it [here](https://www.proxmox.com/en/proxmox-virtual-environment/overview) and install it on a physical or virtual machine. SSH into the machine and follow the procedures below.
## 1.2 Dependencies
Firts, download and install dependencies
```
apt update -y
apt upgrade -y
apt install git sshpass -y
wget http://ftp.cn.debian.org/proxmox/images/system/debian-11-standard_11.7-1_amd64.tar.zst -O /var/lib/vz/template/cache/fu27soma.tar.zst
```

Then, clone the repository and set permissions.
```
git clone https://github.com/saracoglumert/fu27soma-project
cd fu27soma-project
chmod +x manage
chmod +x controller
```
# 1. Installation
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

# 2. Architecture and Endpoints
![alt text](https://github.com/saracoglumert/fu27soma-project/blob/main/thesis/img/arch.png)
Container configuration:
- **Disk :** 16 GiB
- **Memory :** 1024 MiB
- **Root Passwords :** 12345


| **Description**           | **URL**                       |
|---------------------------|---------------------------------|
| **Server**                | http://10.10.136.200:9000       |
| **Node 1**                | http://10.10.136.201:10001      |
| **Node 2**                | http://10.10.136.202:10002      |

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
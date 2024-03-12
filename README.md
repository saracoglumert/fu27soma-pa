# fu27soma-project
**Project Thesis**

# 0. Configuration

# 1. Installation
```
git clone https://github.com/saracoglumert/fu27soma-project
cd fu27soma-project
chmod +x manage
./manage init
./manage build
```

```
./manage start
./manage stop
```

```
./manage destroy
```

# 2. Architecture
![alt text](https://github.com/saracoglumert/fu27soma-project/blob/main/thesis/img/arch.png)
- *Disk :*              16 GiB
- *Memory :*            1024 MiB
- *Root Passwords :*    12345


# 3. Endpoints
| **Parameters**    | **Value**                       |
|-------------------|---------------------------------|
| **OS**            | Proxmox VE 8.1.4                |
| **IP**            | 10.10.136.100                   |
| **Gateway**       | 10.10.136.254                   |

# Host
| **Parameters**    | **Value**                       |
|-------------------|---------------------------------|
| **OS**            | Proxmox VE 8.1.4                |
| **IP**            | 10.10.136.100                   |
| **Gateway**       | 10.10.136.254                   |


# CT 200 (Server)
| **Parameters**    | **Value**                       |
|-------------------|---------------------------------|
| **OS**            | Debian 11                       |
| **Configuration** | 16 GB / 2GB / 4 core            |
| **Hostname**      | server.local                    |
| **IP**            | 10.10.136.200                   |
| **User**          | root                            |
| **Pass**          | 12345                           |
| **App**           | http://10.10.136.200:9000       |

# CT 201 (Node1 - Faber)
| **Parameters**    | **Value**                       |
|-------------------|---------------------------------|
| **OS**            | Debian 11                       |
| **Configuration** | 8 GB / 1GB / 1 core             |
| **Hostname**      | node1.local                     |
| **IP**            | 10.10.136.201                   |
| **User**          | root                            |
| **Pass**          | 12345                           |
| **Endpoint**      | http://10.10.136.201:8030       |
| **Administration**| http://10.10.136.201:8031       |

# CT 202 (Node 2 - Alice)
| **Parameters**    | **Value**                       |
|-------------------|---------------------------------|
| **OS**            | Debian 11                       |
| **Configuration** | 8 GB / 1GB / 1 core             |
| **Hostname**      | node2.local                     |
| **IP**            | 10.10.136.202                   |
| **User**          | root                            |
| **Pass**          | 12345                           |
| **Endpoint**      | http://10.10.136.202:8030       |
| **Administration**| http://10.10.136.202:8031       |

# Endpoints
| **Parameters**    | **Value**                       |
|-------------------|---------------------------------|
| **Node 200 (Indy)**       | http://10.10.136.200:9000       |
| **Node 200 (Tails)**      | http://10.10.136.200:6543       |
| **Node 201**              | http://10.10.136.201:9010       |
| **Node 201 (admin)**      | http://10.10.136.201:9011       |
| **Node 202**              | http://10.10.136.202:9020       |
| **Node 202 (admin)**      | http://10.10.136.202:9021       |

# CT 250 (Development)
| **Parameters**    | **Value**                       |
|-------------------|---------------------------------|
| **OS**            | Debian 11                       |
| **Configuration** | 16 GB / 4GB / 4 core            |
| **Hostname**      | node2.local                     |
| **IP**            | 10.10.136.250                   |
| **User**          | root                            |
| **Pass**          | 12345                           |

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
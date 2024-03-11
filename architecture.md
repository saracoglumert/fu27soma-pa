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
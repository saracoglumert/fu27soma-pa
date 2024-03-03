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
| **Configuration** | 16 GB Disk / 2GB Memory / 4 core|
| **Hostname**      | server.local                    |
| **IP**            | 10.10.136.200                   |
| **User**          | root                            |
| **Pass**          | 12345                           |
| **App**           | http://10.10.136.200:9000       |

# CT 201 (Node1 - Faber)
| **Parameters**    | **Value**                       |
|-------------------|---------------------------------|
| **OS**            | Debian 11                       |
| **Configuration** | 8 GB Disk / 1GB Memory / 1 core |
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
| **Configuration** | 8 GB Disk / 1GB Memory / 1 core |
| **Hostname**      | node2.local                     |
| **IP**            | 10.10.136.202                   |
| **User**          | root                            |
| **Pass**          | 12345                           |
| **Endpoint**      | http://10.10.136.202:8030       |
| **Administration**| http://10.10.136.202:8031       |

# CT 250 (Development)
| **Parameters**    | **Value**                       |
|-------------------|---------------------------------|
| **OS**            | Debian 11                       |
| **Configuration** | 8 GB Disk / 2GB Memory / 4 core |
| **Hostname**      | node2.local                     |
| **IP**            | 10.10.136.250                   |
| **User**          | root                            |
| **Pass**          | 12345                           |
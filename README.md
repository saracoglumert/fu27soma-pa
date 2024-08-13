# fu27soma-pa

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

After a successful build, you should receive an output like this:
```
Build took 14.9 minutes.

Endpoints:
         http://10.10.10.200:80
         http://10.10.10.201:80
         http://10.10.10.202:80
```
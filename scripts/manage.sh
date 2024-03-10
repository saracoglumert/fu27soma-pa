HOSTNAME_SERVER="server"
HOSTNAME_NODE1="sender"
HOSTNAME_NODE2="receiver"

ID_SERVER="200"
ID_NODE1="201"
ID_NODE2="202"

IP_SERVER="10.10.136.200/24"
IP_NODE1="10.10.136.201/24"
IP_NODE2="10.10.136.202/24"

CONF_MEMORY="1024"
CONF_ROOTPASS="12345"
CONF_GATEWAY="10.10.136.254"

BUILD () {
pct create $ID_SERVER /var/lib/vz/template/cache/debian-11-standard_11.7-1_amd64.tar.zst --hostname "$HOSTNAME_SERVER" --memory "$CONF_MEMORY" --net0 name=eth0,bridge=vmbr0,firewall=1,gw=$CONF_GATEWAY,ip=$IP_SERVER,type=veth --storage local-lvm --rootfs local-lvm:8 --unprivileged 1 --ignore-unpack-errors --ssh-public-keys /root/.ssh/authorized_keys --ostype debian --password="$CONF_ROOTPASS" --start 1
pct create $ID_NODE1 /var/lib/vz/template/cache/debian-11-standard_11.7-1_amd64.tar.zst --hostname "$HOSTNAME_NODE1" --memory "$CONF_MEMORY" --net0 name=eth0,bridge=vmbr0,firewall=1,gw=$CONF_GATEWAY,ip=$IP_NODE1,type=veth --storage local-lvm --rootfs local-lvm:8 --unprivileged 1 --ignore-unpack-errors --ssh-public-keys /root/.ssh/authorized_keys --ostype debian --password="$CONF_ROOTPASS" --start 1
pct create $ID_NODE2 /var/lib/vz/template/cache/debian-11-standard_11.7-1_amd64.tar.zst --hostname "$HOSTNAME_NODE2" --memory "$CONF_MEMORY" --net0 name=eth0,bridge=vmbr0,firewall=1,gw=$CONF_GATEWAY,ip=$IP_NODE2,type=veth --storage local-lvm --rootfs local-lvm:8 --unprivileged 1 --ignore-unpack-errors --ssh-public-keys /root/.ssh/authorized_keys --ostype debian --password="$CONF_ROOTPASS" --start 1

wget https://raw.githubusercontent.com/saracoglumert/fu27soma-project/main/scripts/node200.sh -O res/node200.sh
wget https://raw.githubusercontent.com/saracoglumert/fu27soma-project/main/scripts/node201.sh -O res/node201.sh
wget https://raw.githubusercontent.com/saracoglumert/fu27soma-project/main/scripts/node202.sh -O res/node202.sh

pct push $ID_SERVER res/node200.sh ~/init.sh
pct push $ID_NODE1 res/node201.sh ~/init.sh
pct push $ID_NODE2 res/node202.sh ~/init.sh

pct exec $ID_SERVER -- sh init.sh
pct exec $ID_NODE1 -- sh init.sh
pct exec $ID_NODE2 -- sh init.sh

}

DESTROY () {
pct stop $ID_SERVER
pct stop $ID_NODE1
pct stop $ID_NODE2
pct destroy $ID_SERVER
pct destroy $ID_NODE1
pct destroy $ID_NODE2
}

if [ "$1" == "build" ]; then
    BUILD
fi

if [ "$1" == "destroy" ]; then
    DESTROY
fi
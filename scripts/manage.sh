HOSTNAME_SERVER="server"
HOSTNAME_NODE1="sender"
HOSTNAME_NODE2="receiver"

ID_SERVER="200"
ID_NODE1="201"
ID_NODE2="202"

IP_SERVER="10.10.136.200"
IP_NODE1="10.10.136.201"
IP_NODE2="10.10.136.202"
IP_EXT='/24'

CONF_GATEWAY="10.10.136.254"
CONF_MEMORY="1024"
CONF_ROOTPASS="12345"
CONF_TEMPLATE_PATH="/var/lib/vz/template/cache/debian-11-standard_11.7-1_amd64.tar.zst"
CONF_TEMPLATE_URL='http://ftp.cn.debian.org/proxmox/images/system/debian-11-standard_11.7-1_amd64.tar.zst'

read -p "This will take apprx. 10 minutes. Do you want to proceed? (y/n) " yn

case $yn in 
	y ) echo '';;
	n ) echo '';
		exit;;
	* ) echo 'Invalid response.';
		exit 1;;
esac

if ! test -f $CONF_TEMPLATE_PATH; then
  wget $CONF_TEMPLATE_URL -O $CONF_TEMPLATE_PATH
fi

BUILD () {
  # Create containers
  pct create $ID_SERVER $CONF_TEMPLATE_PATH --hostname "$HOSTNAME_SERVER" --memory "$CONF_MEMORY" --net0 name=eth0,bridge=vmbr0,firewall=1,gw=$CONF_GATEWAY,ip=$(echo ${IP_SERVER}${IP_EXT}),type=veth --storage local-lvm --rootfs local-lvm:8 --unprivileged 1 --ignore-unpack-errors --ostype debian --password="$CONF_ROOTPASS" --start 1 --features nesting=1
  pct create $ID_NODE1 $CONF_TEMPLATE_PATH --hostname "$HOSTNAME_NODE1" --memory "$CONF_MEMORY" --net0 name=eth0,bridge=vmbr0,firewall=1,gw=$CONF_GATEWAY,ip=$(echo ${IP_NODE1}${IP_EXT}),type=veth --storage local-lvm --rootfs local-lvm:8 --unprivileged 1 --ignore-unpack-errors --ostype debian --password="$CONF_ROOTPASS" --start 1 --features nesting=1
  pct create $ID_NODE2 $CONF_TEMPLATE_PATH --hostname "$HOSTNAME_NODE2" --memory "$CONF_MEMORY" --net0 name=eth0,bridge=vmbr0,firewall=1,gw=$CONF_GATEWAY,ip=$(echo ${IP_NODE2}${IP_EXT}),type=veth --storage local-lvm --rootfs local-lvm:8 --unprivileged 1 --ignore-unpack-errors --ostype debian --password="$CONF_ROOTPASS" --start 1 --features nesting=1
  #pct create 455 $CONF_TEMPLATE_PATH --hostname "testest" --memory "$CONF_MEMORY" --net0 name=eth0,bridge=vmbr0,firewall=1,gw=$CONF_GATEWAY,ip='10.10.136.245/24',type=veth --storage local-lvm --rootfs local-lvm:8 --unprivileged 1 --ignore-unpack-errors --ostype debian --password=$CONF_ROOTPASS --start 1 --features nesting=1

  # Fetch init scripts
  mkdir res
  wget --no-check-certificate --no-cache --no-cookies -O res/node200.sh https://raw.githubusercontent.com/saracoglumert/fu27soma-project/main/scripts/node200.sh 
  wget --no-check-certificate --no-cache --no-cookies -O res/node201.sh https://raw.githubusercontent.com/saracoglumert/fu27soma-project/main/scripts/node201.sh
  wget --no-check-certificate --no-cache --no-cookies -O res/node202.sh https://raw.githubusercontent.com/saracoglumert/fu27soma-project/main/scripts/node202.sh

  # Push init scripts
  pct push $ID_SERVER res/node200.sh ~/init.sh
  pct push $ID_NODE1 res/node201.sh ~/init.sh
  pct push $ID_NODE2 res/node202.sh ~/init.sh

  # Run init scripts
  pct exec $ID_SERVER -- bash init.sh
  pct exec $ID_NODE1 -- bash init.sh
  pct exec $ID_NODE2 -- bash init.sh
}

START () {
  pct exec $ID_SERVER -- bash start

}

DESTROY () {
  # Stop containers
  pct stop $ID_SERVER
  pct stop $ID_NODE1
  pct stop $ID_NODE2
  # Destroy containers
  pct destroy $ID_SERVER
  pct destroy $ID_NODE1
  pct destroy $ID_NODE2
}

if [ "$1" == "build" ]; then
  BUILD
fi

if [ "$1" == "start" ]; then
  START
fi

if [ "$1" == "destroy" ]; then
  DESTROY
fi
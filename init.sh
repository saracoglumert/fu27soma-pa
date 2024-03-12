echo 'Installing dependencies'
apt update -y  > /dev/null 2>&1
apt upgrade -y  > /dev/null 2>&1
apt install git sshpass -y  > /dev/null 2>&1

if ! test -f /var/lib/vz/template/cache/debian11.tar.zst; then
  echo 'Downloading container template'
  wget http://ftp.cn.debian.org/proxmox/images/system/debian-11-standard_11.7-1_amd64.tar.zst -O /var/lib/vz/template/cache/debian11.tar.zst > /dev/null 2>&1
fi

echo 'Analyzing network'
GW=$(/sbin/ip route | awk '/default/ { print $3 }')
for i in `seq 10 10 250`
do
    IP_START=$i
    IP_END=$(($IP_START+2))
    IP_RANGE=()
    for i in $(seq $IP_START $IP_END); do IP_RANGE+=("${GW%.*}.$i"); done

    RESULT=0
    for i in "${IP_RANGE[@]}"
    do
        if ! ping -c 1 ${i} &> /dev/null
        then
            RESULT=$(($RESULT+1))
        fi
    done
    if [ $RESULT -eq 3 ]
    then
        echo ''
        echo 'Found suitable chunk:'
        echo "Gateway       : ${GW}"
        echo "IP [server]   : ${IP_RANGE[0]}"
        echo "IP [node1]    : ${IP_RANGE[1]}"
        echo "IP [node2]    : ${IP_RANGE[2]}"
        break
    fi
done

chmod +x manage
chmod +x controller






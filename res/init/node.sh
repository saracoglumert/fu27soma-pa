# init
echo 'en_US.UTF-8 UTF-8' >>  /etc/locale.gen
locale-gen
#echo 'nameserver 1.1.1.1' >> /etc/resolv.conf
apt update -y
apt upgrade -y
apt install git -y
apt install curl -y
apt install python3-pip -y
echo 'PermitRootLogin yes' >> /etc/ssh/sshd_config
echo 'export PATH="/usr/local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc 

# dependencies
pip3 install aries-cloudagent
pip3 install aries_askar
pip3 install indy_credx
pip3 install indy_vdr

pip3 install git+https://github.com/hyperledger/aries-acapy-plugins@main#subdirectory=redis_events
pip3 install git+https://github.com/hyperledger/aries-acapy-plugins@main#subdirectory=basicmessage_storage
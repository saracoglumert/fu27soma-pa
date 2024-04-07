# Initialize OS
echo 'en_US.UTF-8 UTF-8' >>  /etc/locale.gen
locale-gen
echo 'PermitRootLogin yes' >> /etc/ssh/sshd_config
echo 'export PATH="/usr/local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc 

# Updates and dependencies
apt update -y
apt upgrade -y
apt install git -y
apt install curl -y
apt install python3-pip -y

# Install aca-py and dependencises
pip3 install aries-cloudagent
pip3 install aries_askar
pip3 install indy_credx
pip3 install indy_vdr

# Install aca-py plugins
pip3 install git+https://github.com/hyperledger/aries-acapy-plugins@main#subdirectory=redis_events
pip3 install git+https://github.com/hyperledger/aries-acapy-plugins@main#subdirectory=basicmessage_storage

# Setup redis
apt install redis -y
sed -i 's/.*bind 127.0.0.1 ::1*/bind 0.0.0.0/' /etc/redis/redis.conf
sed -i 's/.*# requirepass foobared*/requirepass 12345/' /etc/redis/redis.conf

# Finalize
reboot
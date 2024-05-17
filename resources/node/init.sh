# Initialize OS
echo 'en_US.UTF-8 UTF-8' >>  /etc/locale.gen
locale-gen
echo 'export PATH="/usr/local/bin:$PATH"' >> ~/.bashrc
echo 'Acquire::ForceIPv4 "true";' >> /etc/apt/apt.conf.d/99force-ipv4
echo 'PermitRootLogin yes' >> /etc/ssh/sshd_config
source ~/.bashrc 

# Update & Upgrade
apt install apt-transport-https -y
apt clean -y
apt update -y
apt upgrade -y

# Dependencies - System
apt install git -y
apt install curl -y
apt install python3-pip -y

# Dependencies - Python Packages
pip3 install werkzeug==2.0.1
pip3 install markupsafe==2.0.1
pip3 install flask==2.0.1
pip3 install aries-cloudagent==0.11.0
pip3 install aries_askar==0.3.1
pip3 install indy_credx==1.1.1
pip3 install indy_vdr==0.4.2
pip3 install anoncreds==0.2.0
pip3 install mysql-connector-python==8.4.0

# Dependencies - Aca-py Plugins
pip3 install git+https://github.com/hyperledger/aries-acapy-plugins@main#subdirectory=redis_events
pip3 install git+https://github.com/hyperledger/aries-acapy-plugins@main#subdirectory=basicmessage_storage

# Dependencies - Redis
apt install redis -y
# set redis conf - cluster mode, accessiblity, password
sed -i 's/.*bind 127.0.0.1 ::1*/bind 0.0.0.0/' /etc/redis/redis.conf
sed -i 's/.*# requirepass foobared*/requirepass %redis_pass%/' /etc/redis/redis.conf
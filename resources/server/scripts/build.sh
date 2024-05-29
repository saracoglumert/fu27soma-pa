# Initialize OS
echo 'en_US.UTF-8 UTF-8' >>  /etc/locale.gen
locale-gen
echo 'export PATH="/usr/local/bin:$PATH"' >> ~/.bashrc
echo 'export PYTHONPYCACHEPREFIX="/root/cache"' >> ~/.bashrc
echo 'Acquire::ForceIPv4 "true";' >> /etc/apt/apt.conf.d/99force-ipv4
echo 'PermitRootLogin yes' >> /etc/ssh/sshd_config
source ~/.bashrc
export DEBIAN_FRONTEND=noninteractive

# Update & Upgrade
apt install apt-transport-https -y
apt clean -y
apt update -y
apt upgrade -y

# Dependencies - System
apt install git -y
apt install curl -y
apt install python3-pip -y
apt install lsb-release -y

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
pip3 install redis==5.0.4

# Dependencies - Aca-py Plugins
pip3 install git+https://github.com/hyperledger/aries-acapy-plugins@main#subdirectory=redis_events
pip3 install git+https://github.com/hyperledger/aries-acapy-plugins@main#subdirectory=basicmessage_storage

# Dependencies - Docker Images
curl -4sSL https://get.docker.com/ | sh
mkdir /resources
cd resources
git clone https://github.com/bcgov/von-network
git clone https://github.com/bcgov/indy-tails-server.git
cd -L
/resources/von-network/manage build

# Dependencies - MySQL
wget https://dev.mysql.com/get/mysql-apt-config_0.8.29-1_all.deb
dpkg -i mysql-apt-config_0.8.29-1_all.deb
apt update -y
apt install mysql-server -y
mysql -uroot -e "CREATE USER '%db_user%'@'%' IDENTIFIED BY '%db_pass%'"
mysql -uroot -e "GRANT ALL PRIVILEGES ON *.* TO '%db_user%'@'%' WITH GRANT OPTION"
mysql -uroot -e "FLUSH PRIVILEGES"
mysql -uroot < /root/config/database.sql
rm mysql-apt-config_0.8.29-1_all.deb

# Dependencies - Redis
apt install redis -y
/etc/init.d/redis-server stop
update-rc.d redis-server disable


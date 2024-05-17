# Initialize OS
echo 'en_US.UTF-8 UTF-8' >>  /etc/locale.gen
locale-gen
echo 'export PATH="/usr/local/bin:$PATH"' >> ~/.bashrc
echo 'Acquire::ForceIPv4 "true";' >> /etc/apt/apt.conf.d/99force-ipv4
echo 'PermitRootLogin yes' >> /etc/ssh/sshd_config
source ~/.bashrc

# Update & Upgrade
apt install apt-transport-https -yq
apt clean -yq
apt update -yq
DEBIAN_FRONTEND=noninteractive apt upgrade -yq

# Dependencies - system
apt install git -yq
apt install curl -yq
apt install python3-pip -yq
apt install lsb-release -yq

# Dependencies - Python Packages
pip3 install werkzeug==2.0.1
pip3 install markupsafe==2.0.1
pip3 install flask==2.0.1
pip3 install mysql-connector-python==8.4.0

# Dependencies - Docker
curl -4sSL https://get.docker.com/ | sh

# Dependencies - Images
mkdir /resources
cd resources
git clone https://github.com/bcgov/von-network
git clone https://github.com/bcgov/indy-tails-server.git
cd -L

# Dependencies - MySQL
export DEBIAN_FRONTEND=noninteractive
wget https://dev.mysql.com/get/mysql-apt-config_0.8.29-1_all.deb
dpkg -i mysql-apt-config_0.8.29-1_all.deb
apt update -y
apt install mysql-server -y
mysql -uroot -e "CREATE USER '%db_user%'@'%' IDENTIFIED BY '%db_pass%'"
mysql -uroot -e "GRANT ALL PRIVILEGES ON *.* TO '%db_user%'@'%' WITH GRANT OPTION"
mysql -uroot -e "FLUSH PRIVILEGES"
mysql -uroot < db.sql
rm mysql-apt-config_0.8.29-1_all.deb
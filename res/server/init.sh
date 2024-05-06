# Initialize OS
echo 'en_US.UTF-8 UTF-8' >>  /etc/locale.gen
locale-gen
echo 'export PATH="/usr/local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc 


# Updates and dependencies
apt update -y
apt upgrade -y
apt install git -y
apt install curl -y
apt install python3-pip -y
apt install lsb-release -y

# Install Docker
curl -4sSL https://get.docker.com/ | sh

# Get Repos
cd -L
mkdir res
cd res
git clone https://github.com/bcgov/von-network
git clone https://github.com/bcgov/indy-tails-server.git
cd ..

# Setup MySQL
export DEBIAN_FRONTEND=noninteractive
wget https://dev.mysql.com/get/mysql-apt-config_0.8.29-1_all.deb
dpkg -i mysql-apt-config_0.8.29-1_all.deb
apt update -y
apt install mysql-server -y
mysql -uroot -e "CREATE USER '%db_user%'@'%' IDENTIFIED BY '%db_pass%'"
mysql -uroot -e "GRANT ALL PRIVILEGES ON *.* TO '%db_user%'@'%' WITH GRANT OPTION"
mysql -uroot -e "FLUSH PRIVILEGES"
mysql -uroot < db.sql

# Finalize
rm mysql-apt-config_0.8.29-1_all.deb
echo 'PermitRootLogin yes' >> /etc/ssh/sshd_config
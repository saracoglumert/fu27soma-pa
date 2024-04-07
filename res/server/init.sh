# init
echo 'en_US.UTF-8 UTF-8' >>  /etc/locale.gen
locale-gen
#echo 'nameserver 1.1.1.1' >> /etc/resolv.conf
apt update -y
apt upgrade -y
apt install git -y
apt install curl -y
apt install python3-pip -y
apt install lsb-release -y
echo 'PermitRootLogin yes' >> /etc/ssh/sshd_config
echo 'export PATH="/usr/local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc 

# Install Docker
curl -4sSL https://get.docker.com/ | sh

# Get Repos
cd -L
mkdir res
cd res
git clone https://github.com/bcgov/von-network
git clone https://github.com/bcgov/indy-tails-server.git
cd ..

# Install MySQL
export DEBIAN_FRONTEND=noninteractive
wget https://dev.mysql.com/get/mysql-apt-config_0.8.29-1_all.deb
dpkg -i mysql-apt-config_0.8.29-1_all.deb
apt update
apt install mysql-server -y

mysql -uroot -e "CREATE USER 'root'@'%' IDENTIFIED BY '12345'"
mysql -uroot -e "GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' WITH GRANT OPTION"
mysql -uroot -e "FLUSH PRIVILEGES"

mysql -uroot < db.sql
# init
echo 'en_US.UTF-8 UTF-8' >>  /etc/locale.gen
locale-gen
#echo 'nameserver 1.1.1.1' >> /etc/resolv.conf
apt update -y
apt upgrade -y
apt install git -y
apt install curl -y
apt install python3-pip -y

curl -4sSL https://get.docker.com/ | sh

echo 'PermitRootLogin yes' >> /etc/ssh/sshd_config
echo 'export PATH="/usr/local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc 

# resources
cd -L
mkdir res
cd res
git clone https://github.com/bcgov/von-network
git clone https://github.com/bcgov/indy-tails-server.git
cd ..
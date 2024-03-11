# Initialization
echo 'en_US.UTF-8 UTF-8' >>  /etc/locale.gen
locale-gen
apt update -y
apt upgrade -y
apt install git -y
apt install curl -y
apt install python3-pip -y
curl -sSL https://get.docker.com/ | sh

# set-up
echo 'export PATH="/usr/local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc 
echo 'PermitRootLogin yes' >> /etc/ssh/sshd_config

# resources
cd -L
mkdir res
cd res
git clone https://github.com/bcgov/von-network
git clone https://github.com/bcgov/indy-tails-server.git
cd ..
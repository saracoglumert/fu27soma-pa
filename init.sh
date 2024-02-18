# Locale settings for Docker / Perl
sudo bash -c 'echo "LC_CTYPE=en_US.UTF-8" > /etc/default/locale'
sudo bash -c 'echo "LC_MESSAGES=en_US.UTF-8" > /etc/default/locale'
sudo bash -c 'echo "LC_ALL=en_US.UTF-8" > /etc/default/locale'

sudo apt update -y
sudo apt upgrade -y

# Install some applications
sudo apt install git -y
sudo apt install python3-pip -y
sudo apt install python3-venv -y

# Install docker
curl -sSL https://get.docker.com/ | sudo sh
sudo apt install uidmap -y 
dockerd-rootless-setuptool.sh install
echo 'export PATH=/usr/bin:$PATH' >> ~/.bashrc

# Setup virtual environment for VON-Network
mkdir envs
cd envs
python3 -m venv env-von

# Setup VON-Network
git clone https://github.com/bcgov/von-network

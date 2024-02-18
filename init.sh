sudo apt update -y
sudo apt upgrade -y

# Install some applications
sudo apt install git -y
sudo apt install python3-pip -y

# Locale settings for Docker / Perl
echo "LC_CTYPE=en_US.UTF-8" >> /etc/default/locale
echo "LC_MESSAGES=en_US.UTF-8" >> /etc/default/locale
echo "LC_ALL=en_US.UTF-8" >> /etc/default/locale

# Install docker
curl -sSL https://get.docker.com/ | sudo sh
sudo apt install uidmap -y 
dockerd-rootless-setuptool.sh install

# Setup virtual environment for VON-Network


# Setup VON-Network
git clone https://github.com/bcgov/von-network

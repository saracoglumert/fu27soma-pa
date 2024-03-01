# Initialization
echo 'en_US.UTF-8 UTF-8' >>  /etc/locale.gen
locale-gen
apt update -y
apt upgrade -y
apt install git -y
apt install curl -y
apt install zsh -y
sh -c "$(wget https://raw.github.com/robbyrussell/oh-my-zsh/master/tools/install.sh -O -)"
curl -sSL https://get.docker.com/ | sh

# Get Application
git clone https://github.com/bcgov/von-network

# Create Scripts
# Script - Start
touch start
echo './von-network/manage build' >> start
echo './von-network/manage start' >> start
# Script-Stop
touch stop
echo './von-network/manage stop' >> stop
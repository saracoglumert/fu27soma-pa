# Initialization
echo 'en_US.UTF-8 UTF-8' >>  /etc/locale.gen
locale-gen
apt update -y
apt upgrade -y
apt install git -y
apt install curl -y
apt install zsh -y
curl -sSL https://get.docker.com/ | sh
sh -c "$(wget https://raw.github.com/robbyrussell/oh-my-zsh/master/tools/install.sh -O -)"

# Get Resources
mkdir res
cd res
git clone https://github.com/bcgov/von-network
git clone https://github.com/bcgov/indy-tails-server.git
cd ..

# Create Scripts
# Script - Start
touch start
echo './res/von-network/manage build' >> start
echo './res/von-network/manage start 10.10.136.200 WEB_SERVER_HOST_PORT=9000 LEDGER_INSTANCE_NAME="Thesis"' >> start
echo './res/indy-tails-server/docker/manage start' >> start
chmod +x start

# Script - Start
touch test
echo './res/indy-tails-server/docker/manage test' >> test
chmod +x test
# Initialization
echo 'en_US.UTF-8 UTF-8' >>  /etc/locale.gen
locale-gen
apt update -y
apt upgrade -y
apt install git -y
apt install curl -y
apt install zsh -y
apt install python3-pip
curl -sSL https://get.docker.com/ | sh

# Install Dep
pip3 install aries-cloudagent -y
pip3 install aries_askar -y
pip3 install indy_credx -y
pip3 install indy_vdr -y

# Get Resources
mkdir res
cd res
git clone https://github.com/bcgov/von-network
git clone https://github.com/bcgov/indy-tails-server.git
git clone https://github.com/hyperledger/aries-cloudagent-python
cd ..

# Create Scripts
# Script - start
touch start
cat <<EOT >> start_server
./res/von-network/manage build
./res/von-network/manage start
./res/indy-tails-server/docker/manage start
EOT
chmod +x start

# Script - start_faber
touch start_faber
cat <<EOT >> start_faber
./res/aries-cloudagent-python/demo/run_demo faber
EOT
chmod +x start_faber

# Script - start_alice
touch start_alice
cat <<EOT >> start_alice
./res/aries-cloudagent-python/demo/run_demo alice
EOT
chmod +x start_alice
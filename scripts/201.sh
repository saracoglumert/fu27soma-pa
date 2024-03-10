echo 'en_US.UTF-8 UTF-8' >>  /etc/locale.gen
locale-gen
apt update -y
apt upgrade -y
apt install git -y
apt install curl -y
apt install zsh -y
apt install python3-pip -y
curl -sSL https://get.docker.com/ | sh
sh -c "$(wget https://raw.github.com/robbyrussell/oh-my-zsh/master/tools/install.sh -O -)"

# Get Application
pip3 install aries-cloudagent
pip3 install aries_askar
pip3 install indy_credx
pip3 install indy_vdr

# Create Scripts
# Script - Start
touch start
cat <<EOT >> start
aca-py start --arg-file args.yaml
EOT
chmod +x start

# File - Arguments
touch args.yaml
cat <<EOT >> args.yaml
auto-provision: true
label: faber

inbound-transport:
   - [http, 0.0.0.0, 9040]

outbound-transport: http

wallet-type: askar
wallet-storage-type: default
wallet-name: faber-wallet
wallet-key: faber-wallet-key

admin-insecure-mode: true

admin: [0.0.0.0, 9041]

endpoint: http://localhost:9040

genesis-url: http://10.10.136.200:9000/genesis

# Connections
debug-connections: true
auto-accept-invites: true
auto-accept-requests: true
auto-ping-connection: true

log-level: info

tails-server-base-url: http://localhost:6543 
EOT
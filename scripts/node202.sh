# init
echo 'en_US.UTF-8 UTF-8' >>  /etc/locale.gen
locale-gen
apt update -y
apt upgrade -y
apt install git -y
apt install curl -y
apt install python3-pip -y

# dependencies
pip3 install aries-cloudagent
pip3 install aries_askar
pip3 install indy_credx
pip3 install indy_vdr

# scripts
# start
touch start
cat <<EOT >> start
aca-py start --arg-file args.yaml
EOT
chmod +x start

# files
# arguments
touch args.yaml
cat <<EOT >> args.yaml
auto-provision: true
label: alice

inbound-transport:
   - [http, 0.0.0.0, 9020]

outbound-transport: http

wallet-type: askar
wallet-storage-type: default
wallet-name: alice-wallet
wallet-key: alice-wallet-key

admin-insecure-mode: true

admin: [0.0.0.0, 9021]

endpoint: http://localhost:9020

genesis-url: http://10.10.136.200:9000/genesis

# Connections
debug-connections: true
auto-accept-invites: true
auto-accept-requests: true
auto-ping-connection: true

log-level: info

tails-server-base-url: http://localhost:6543 
EOT
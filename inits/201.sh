# Initialization
echo 'en_US.UTF-8 UTF-8' >>  /etc/locale.gen
locale-gen
apt update -y
apt upgrade -y
apt install git -y
apt install curl -y
apt install jq -y
apt install zsh -y
curl -sSL https://get.docker.com/ | sh

curl https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.tgz --output ngrok.tgz
tar xvzf ngrok.tgz -C /usr/local/bin

sh -c "$(wget https://raw.github.com/robbyrussell/oh-my-zsh/master/tools/install.sh -O -)"

# Get Application
git clone https://github.com/hyperledger/aries-cloudagent-python

# Create Scripts
# Script - Start
touch start
echo 'LEDGER_URL=http://10.10.136.200:9000' >> start
echo './aries-cloudagent-python/demo/run_demo faber -- events --no-auto --bg' >> start
chmod +x start

 curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc | tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null && echo "deb https://ngrok-agent.s3.amazonaws.com buster main" | tee /etc/apt/sources.list.d/ngrok.list && apt update && apt install ngrok
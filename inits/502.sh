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
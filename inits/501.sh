apt update -y
apt upgrade -y

apt install git

curl -sSL https://get.docker.com/ | sh

git clone https://github.com/bcgov/von-network

# Set Static IP for CT
mv /etc/network/interfaces /etc/network/interfaces-backup
cat <<EOT >> /etc/network/interfaces
line 1
line 2
EOT

# Set Start-Up Script
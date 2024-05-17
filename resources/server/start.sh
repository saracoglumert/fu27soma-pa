/resources/von-network/manage build
/resources/von-network/manage start %network_ip% WEB_SERVER_HOST_PORT=%port_ledger% "LEDGER_INSTANCE_NAME=%name%"
/resources/indy-tails-server/docker/manage start
nohup python3 /root/web.py > /dev/null 2>&1 &
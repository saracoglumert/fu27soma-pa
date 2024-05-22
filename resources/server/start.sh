if [ $1 = "redis" ]; then
    nohup redis-server /root/redis.conf > /dev/null 2>&1 &
elif [ $1 = "von" ]; then
    nohup /resources/von-network/manage start %network_ip% WEB_SERVER_HOST_PORT=%port_ledger% "LEDGER_INSTANCE_NAME=%name%"
elif [ $1 = "aca-py" ]; then
    [ ! -e %file_log% ] || rm %file_log%
    nohup aca-py start --arg-file /root/args.yaml > /root/%file_log% 2>&1 &
elif [ $1 = "tails" ]; then
    nohup /resources/indy-tails-server/docker/manage start
elif [ $1 = "web" ]; then
    nohup python3 /root/app.py %port_ui% > /dev/null 2>&1 &
fi
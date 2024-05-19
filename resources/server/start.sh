if [ $1 = "redis" ]; then
    echo ">>redis"
    nohup redis-server /root/redis.conf > /dev/null 2>&1 &
elif [ $1 = "von" ]; then
    echo ">>von"
    nohup /resources/von-network/manage start %network_ip% WEB_SERVER_HOST_PORT=%port_ledger% "LEDGER_INSTANCE_NAME=%name%"
elif [ $1 = "tails" ]; then
    echo ">>tails"
    nohup /resources/indy-tails-server/docker/manage start
elif [ $1 = "web" ]; then
    echo ">>web"
    nohup python3 /root/web.py > /dev/null 2>&1 &
elif [ $1 = "test" ]; then
    echo "test"
    touch /root/test
fi
if [ $1 = "redis" ]; then
    [ ! -e /root/logs/%log_redis% ] || rm /root/logs/%log_redis%
    nohup redis-server /root/config/redis.conf > /root/logs/%log_redis% 2>&1 &
elif [ $1 = "indy" ]; then
    [ ! -e /root/logs/%log_indy% ] || rm /root/logs/%log_indy%
    nohup /resources/von-network/manage start %network_ip% WEB_SERVER_HOST_PORT=%port_ledger% "LEDGER_INSTANCE_NAME=%name%" > /root/logs/%log_indy% 2>&1 &
elif [ $1 = "aries" ]; then
    [ ! -e /root/logs/%log_acapy% ] || rm /root/logs/%log_acapy%
    nohup aca-py start --arg-file /root/config/args.yaml > /root/logs/%log_acapy% 2>&1 &
elif [ $1 = "app" ]; then
    [ ! -e /root/logs/%log_web% ] || rm /root/logs/%log_web%
    nohup python3 /root/app.py %id% %port_ui% > /root/logs/%log_web% 2>&1 &
fi
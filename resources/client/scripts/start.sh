if [ $1 = "redis" ]; then
    [ ! -e /root/logs/%log_redis% ] || rm /root/logs/%log_redis%
    nohup redis-server /root/config/redis.conf > /root/logs/%log_redis% 2>&1 &
elif [ $1 = "aries" ]; then
    [ ! -e /root/logs/%log_acapy% ] || rm /root/logs/%log_acapy%
    nohup aca-py start --arg-file /root/config/args.yaml > /root/logs/%log_acapy% 2>&1 &
elif [ $1 = "app" ]; then
    [ ! -e /root/logs/%log_web% ] || rm /root/logs/%log_web%
    nohup python3 /root/app.py %id% %port_ui% > /root/logs/%log_web% 2>&1 &
fi
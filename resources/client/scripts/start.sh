if [ $1 = "redis" ]; then
    [ ! -e /root/logs/%log_redis% ] || rm /root/logs/%log_redis%
    nohup redis-server /root/config/redis.conf > /root/%log_redis% 2>&1 &
elif [ $1 = "aries" ]; then
    [ ! -e /root/logs/%log_acapy% ] || rm /root/logs/%log_acapy%
    nohup aca-py start --arg-file /root/config/args.yaml > /root/%log_acapy% 2>&1 &
elif [ $1 = "app" ]; then
    [ ! -e /root/logs/%log_app% ] || rm /root/logs/%log_app%
    nohup python3 /root/app.py %id% %port_ui% > /root/%log_app% 2>&1 &
fi
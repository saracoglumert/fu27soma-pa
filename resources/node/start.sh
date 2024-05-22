if [ $1 = "redis" ]; then
    nohup redis-server /root/redis.conf > /dev/null 2>&1 &
elif [ $1 = "aca-py" ]; then
    [ ! -e %file_log% ] || rm %file_log%
    nohup aca-py start --arg-file /root/args.yaml > /root/%file_log% 2>&1 &
elif [ $1 = "web" ]; then
    nohup python3 /root/app.py %id% %port_ui% > /dev/null 2>&1 &
fi
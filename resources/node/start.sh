if [ $1 = "redis" ]; then
    echo ">>redis"
    nohup redis-server /root/redis.conf > /dev/null 2>&1 &
elif [ $1 = "aca-py" ]; then
    echo ">>aca-py"
    [ ! -e %file_log% ] || rm %file_log%
    nohup aca-py start --arg-file /root/args.yaml > /root/%file_log% 2>&1 &
elif [ $1 = "web" ]; then
    echo ">>web"
    nohup python3 /root/web.py %id% > /dev/null 2>&1 &
elif [ $1 = "test" ]; then
    echo "test"
    touch /root/test
fi
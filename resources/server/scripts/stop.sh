kill -9 $(pgrep -f "docker") > /dev/null
kill -9 $(pgrep -f "python3") > /dev/null
kill -9 $(pgrep -f "redis-server") > /dev/null
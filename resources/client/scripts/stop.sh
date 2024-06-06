kill -9 $(pgrep -f "redis-server") > /dev/null
kill -9 $(pgrep -f "aca-py") > /dev/null
kill -9 $(pgrep -f "app.py") > /dev/null
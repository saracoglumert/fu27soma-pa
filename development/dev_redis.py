from redis import Redis
import json

conn = Redis.from_url(url="redis://10.10.10.200:7000")

temp = json.loads(conn.lrange(str.encode('acapy-record-with-state-base'), -1, -1)[0].decode("utf-8"))['payload']['payload']['connection_id']


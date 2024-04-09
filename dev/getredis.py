from redis import Redis

node1 = Redis.from_url(url="redis://default:12345@10.10.10.201:6379")
node2 = Redis.from_url(url="redis://default:12345@10.10.10.202:6379")

#node1.ping()
#node2.ping()
import mysql.connector
import requests
import json
import random
import string
import time
from redis import Redis

conn_db = mysql.connector.connect(
  host="10.10.10.200",
  user="root",
  password="12345",
  database="fu27soma")

conn_redis = Redis.from_url(url="redis://10.10.10.200:7000")
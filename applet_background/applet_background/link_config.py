# 连接配置
import pymysql
import redis
from DBUtils.PooledDB import PooledDB
from elasticsearch import Elasticsearch

es_con = Elasticsearch(['116.63.150.180'],
                       http_auth=('elastic',
                                  'root001@'),
                       timeout=3600)

con_mysql = PooledDB(pymysql, 12, host='116.63.150.180',
                     port=3306,
                     user='root',
                     password='xd@ksh_1',
                     db='escort',
                     charset='utf8')

pool = redis.ConnectionPool(host='116.63.150.180', port=6379)
redis_con = redis.Redis(connection_pool=pool)



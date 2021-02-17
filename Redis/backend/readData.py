import csv
import redis
r = redis.StrictRedis(host='127.0.0.1', port=6379, db=0)

with open('./skr.csv', 'rt', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    i=1

    for row in reader:
        r.hset(str(i), key='name' , value=row['name'])  #将内容写入redis
        r.hset(str(i), key='email' , value=row['email'])  #将内容写入redis
        r.hset(str(i), key='gender' , value=row['gender'])  #将内容写入redis
        r.hset(str(i), key='ip' , value=row['ip'])  #将内容写入redis
        i = i+1
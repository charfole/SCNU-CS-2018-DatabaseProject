"""

This file is intend for generating the data through csv file for redis database.
$ python ./readData.py
repo: https://github.com/charfole/SCNU-CS-2018-DatabaseProject

"""

import csv
import redis
r = redis.StrictRedis(host='127.0.0.1', port=6379, db=0)

with open('./charfole.csv', 'rt', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    i=1

    # write the content(charfole.csv) into database
    for row in reader:
        r.hset(str(i), key='carId' , value=row['carId'])  
        r.hset(str(i), key='carType' , value=row['carType'])  
        r.hset(str(i), key='carModel' , value=row['carModel'])  
        r.hset(str(i), key='carYear' , value=row['carYear'])  
        i = i+1
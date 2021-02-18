# -*- coding: utf-8 -*-
"""

This file is the backend file for the redis project.
$ gunicorn -b :5000 app:app
repo: https://github.com/charfole/SCNU-CS-2018-DatabaseProject

"""

import datetime
import json
import os
import time
import traceback
import redis
from flask import (Flask, Response, flash, jsonify, redirect, render_template,
                   request, session)
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/charfoleSearch',methods=['GET'])
def charfole():
    """get the content in redis database

    arguments
    -----------
    methods : 'GET'
        You can get the data to show in home page.
    
    return
    -----------
    json
        return the content.

    """

    r = redis.StrictRedis(host='127.0.0.1', port=6379, db=0, decode_responses=True) # connect to the database 0
    rowsName = sorted(r.keys())
    data = []
    for i in range(len(rowsName)):
        dt_1 = {'rows':rowsName[i]}
        dt_2 = r.hgetall(rowsName[i])
        dt_1.update(dt_2)
        data.append(dt_1)

    return jsonify(data)

@app.route('/charfoleCRUD',methods=['POST'])
def charfoleString():
    """implement the CRUD function in redis database

    arguments
    -----------
    methods : 'POST'
        POST the content of the name, key or value
    name : string
        name of the key-value
    key : string
        name of the key
    value : string
        name of the value
    action : 'CREATE'
        create a new key-value pair
    action : 'READ'
        read the key-balue by name
    action : 'UPDATE'
        update a key-value pair
    action : 'DELETE'
        delete a key-value pair

    return
    -----------
    string
        return the implemention status.

    """

    r = redis.Redis(host='localhost', port=6379, db=0,decode_responses=True) # connect to the database 0
    action = request.form.get('action')
    name = request.form.get('name')
    key = request.form.get('key')
    value = request.form.get('value')

    if(action=='CREATE'):
        if(r.hexists(name,key) == True):
                return 'This key already exists.'
            
        else:
            r.hsetnx(name,key,value)
            return 'Sussessfully added.'
 
    # number of keys may change
    elif(action=='READ'):
        result = r.hgetall(name)
        rows = {'rows':name}
        result.update(rows)
        if (result != None):
            return jsonify(result)
        else:
            return 'This name doesn\'t exist.'

    elif(action=='UPDATE'):
        if(r.hexists(name,key) != True):
            return 'This key doesn\'t exist.'
        else:
            r.hset(name,key,value)
            
        return 'Sussessfully updated.'

    elif(action=='DELETE'):
        if(r.hexists(name,key) != True):
            return 'This key doesn\'t exist.'
        else:
            r.hdel(name,key)
            
        return 'Sussessfully Deleted.'

    return 'The action must be in this list:[CREATE,READ,UPDATE,DELETE]!'

@app.route('/charfoleHyperloglog',methods=['POST'])
def charfoleHyperloglog():
    """cardinal number query

    arguments
    -----------
    methods : 'POST'
        post the value of the scale
    scale : int
        value of the scale

    return
    -----------
    json
        return the hyperloglog result.

    """
    
    redisHyper= redis.StrictRedis(host='127.0.0.1', port=6379, db=1, decode_responses=True) # connect to the database 1
    redisHyper.flushdb()
    scale = request.form.get('scale')
    scale = int(scale)
    _startRedisAdd = time.time()
    redisList = [scale]
    originalList = [scale]
    for i in range(scale):
        redisHyper.pfadd(1,i)
    _startRedisAddok = time.time()
    redisAddTime = _startRedisAddok - _startRedisAdd
    redisCount = redisHyper.pfcount(1)
    redisSearchTime = time.time() - _startRedisAddok
    print('Redis添加{}个不同元素时间为：{}'.format( scale,redisAddTime) )
    print('Redis查询{}个不同元素的基数值为：{}'.format(scale,redisCount))
    print('Redis查询{}个不同元素基数的时间为：{}'.format(scale,redisSearchTime))
    redisList.append(redisAddTime)
    redisList.append(redisCount)
    redisList.append(redisSearchTime)

    count = []
    _startOriginalAdd = time.time()
    for i in range(scale):
        count.append(i)
    _startOriginalAddOk = time.time()
    originalAddTime = _startOriginalAddOk - _startOriginalAdd
    originalCount = len(set(count))
    originalSearchTime = time.time() - _startOriginalAddOk
    print('常规添加{}个不同元素时间为：{}'.format( scale, originalAddTime) )
    print('常规查询{}个不同的基数值为：{}'.format( scale, originalCount ))
    print('常规查询{}个不同元素基数的时间为：{}'.format(scale,originalSearchTime))
    originalList.append(originalAddTime)
    originalList.append(originalCount)
    originalList.append(originalSearchTime)

    return jsonify(redisList,originalList)

if __name__ == '__main__':
    app.run()

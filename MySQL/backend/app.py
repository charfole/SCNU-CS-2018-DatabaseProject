"""

This file is the backend file for the redis project.
$ gunicorn -b :5000 app:app
repo: https://github.com/charfole/SCNU-CS-2018-DatabaseProject

"""

import pymysql
import time,datetime
from flask import Flask,flash
from flask import render_template
from flask import request, Response,redirect,session,jsonify
from flask_cors import CORS
import traceback
from flask_sqlalchemy import SQLAlchemy
import time
import os
import subprocess

app = Flask(__name__)
CORS(app)
charfoleSqlList=[]

@app.route('/charfole',methods=['POST','GET'])
def charfole():
    """basic function for MySQL

    arguments
    -----------
    methods : 'GET'
        You can get the information from userTable to show in home page.
    methods : 'POST'
        You can upload SQL statement(string) through POST method 
        to implement the basic function of MySQL.
    
    return
    -----------
    json
        return the content of SQL statement.

    """

    conn = pymysql.connect(host='127.0.0.1', user='root', password='', db='charfoleTable', charset='utf8') # connect to the database
    cur = conn.cursor()
    if request.method=='GET':
        sql = "SELECT * FROM userTable"
        cur.execute(sql)
        cols = cur.description # get the name of column
        col = []
        for i in cols:
            col.append(i[0])
        u = list(cur.fetchall())
        u = jsonify(col,u)
        return u

    if request.method=='POST':
        sql = request.form.get('SQL')
        judgeString = sql.split(' ',1)[0]
        sss={'SELECT','select'}
        if judgeString in sss:
            cur.execute(sql)
            cols = cur.description # get the name of column
            col = []
            for i in cols:
                col.append(i[0])
            u = list(cur.fetchall()) # fetch all the content of the table
            u = jsonify(col,u)
            return u
        else:
            try:
                cur.execute(sql)
                conn.commit()
                return "SQL is successfully excuted!"
            except:
                return "You have an error in your SQL syntax, please check and try again!",250

@app.route('/charfoleTransaction',methods=['POST'])
def charfoleTransaction(myList = charfoleSqlList):
    """transaction function for MySQL

    arguments
    -----------
    methods : 'POST'
        You can upload the transaction statement(string) through POST method 
        to implement the basic function of MySQL.
    action : 'execute'
        execute the SQL statement.
    action : 'commit'
        commit to the database.
    action : 'rollback'
        rollback the execution.
    
    return
    -----------
    string
        return the implemention status of SQL statement.

    """

    conn = pymysql.connect(host='127.0.0.1', user='root', password='', db='charfoleTable', charset='utf8') # connect to the database
    cur = conn.cursor()
    sql = request.form.get('SQL')
    action = request.form.get('action')
    ddl={'CREATE','create','DROP','drop','ALTER','alter','SELECT','select'} # DDL is not supported by the transaction
    judgeString = sql.split(' ',1)[0] # judge the SQL is DDL or not
    if judgeString in ddl and action=='execute': # execute the DDL directly
        try:
            cur.execute(sql)
            return "SQL is successfully excuted!"
        except:
            return "You have an error in your SQL syntax, please check and try again!"
    else: # three actions in transaction
        if(action == 'execute'):
            try:
                cur.execute(sql)
                myList.append(sql)
                return "SQL is successfully excuted!"
            except:
                return "You have an error in your SQL syntax, please check and try again!",250

        elif(action == 'commit'):
            for i in myList:
                cur.execute(i)
            conn.commit()
            myList.clear()
            return "Successfully commit!"

        elif(action == 'rollback'):
            conn.rollback()
            myList.clear()
            return "Successfully rollback!"


@app.route('/charfoleMultipleUserEfficiency',methods=['GET'])
def charfoleMultipleUserEfficiency():
    """query the user information (PS: only available in the backend)

    arguments
    -----------
    methods : 'GET'
        get the information through GET method.
    
    return
    -----------
    json
        return the information of the users.

    """

    cmd = [["mysqladmin","-uroot","variables","status"],["mysqladmin","-uadmin1","variables","status"],
            ["mysqladmin","-uadmin2","variables","status"],["mysqladmin","-uadmin3","variables","status"],
            ["mysqladmin","-uadmin4","variables","status"]] # excute the command in terminal through python
    result = []
    users = ["root","admin1","admin2","admin3","admin4"] # maybe the users' names need to be changed
    for i in range(len(cmd)):
        print(cmd[i])
        tempShell = subprocess.Popen(cmd[i], stdout = subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            stdin=subprocess.PIPE)
        out,err = tempShell.communicate()
        out = str(out)
        result.append(out.split('+\\n')[-1])
    
    return jsonify(users,result)


if __name__ == '__main__':
    app.run()

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

# charfole首页 增删查改/索引/join
@app.route('/charfole',methods=['POST','GET'])
def charfole():
    conn = pymysql.connect(host='127.0.0.1', user='root', password='', db='charfoleTable', charset='utf8')
    cur = conn.cursor()
    if request.method=='GET':
        sql = "SELECT * FROM userTable"
        cur.execute(sql)
        cols = cur.description #获取列名
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
            cols = cur.description #获取列名
            col = []
            for i in cols:
                col.append(i[0])
            u = list(cur.fetchall())
            u = jsonify(col,u)
            return u
        else:
            try:
                # 提交到数据库执行
                cur.execute(sql)
                conn.commit()
                return "SQL is successfully excuted!"
            except:
                return "You have an error in your SQL syntax, please check and try again!",250

# 输入SQL语句执行，创建删除表，增删改查，支持事务
@app.route('/charfoleTransaction',methods=['POST'])
def charfoleTransaction(myList = charfoleSqlList):
    conn = pymysql.connect(host='127.0.0.1', user='root', password='', db='charfoleTable', charset='utf8')
    cur = conn.cursor()
    sql = request.form.get('SQL')
    action = request.form.get('action')
    ddl={'CREATE','create','DROP','drop','ALTER','alter','SELECT','select'}
    judgeString = sql.split(' ',1)[0]
    if judgeString in ddl and action=='execute':
        try:
            cur.execute(sql)
            return "SQL is successfully excuted!"
        except:
            return "You have an error in your SQL syntax, please check and try again!"
    else:
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
    cmd = [["mysqladmin","-uroot","variables","status"],["mysqladmin","-uadmin1","variables","status"],
            ["mysqladmin","-uadmin2","variables","status"],["mysqladmin","-uadmin3","variables","status"],
            ["mysqladmin","-uadmin4","variables","status"]]
    result = []
    users = ["root","admin1","admin2","admin3","admin4"]
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

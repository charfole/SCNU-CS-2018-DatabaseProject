## SCNU-CS-2018-DatabaseProject

华南师范大学计算机学院2018级数据库课程项目。课程一共有两阶段的任务，要求分别选取一款传统型数据库和 NoSQL 数据库，在 Linux 环境下部署服务端，以 C/S 架构实现数据库的各项基本功能和部分特色操作。

本项目选用的是 MySQL 和 Redis ，由于课程不对性能作要求，因此为了能够快速实现要求的功能，项目选用了 Flask 作为服务端，并以 web 的方式开发客户端，具体的项目框架请参照下图。

![架构图](https://github.com/charfole/SCNU-CS-2018-DatabaseProject/blob/master/information/MySQL%E6%9E%B6%E6%9E%84%E5%9B%BE.png)


## 开发环境与依赖

**CentOS Linux release 8.3.2011** 
(项目使用阿里云 ECS 开发，程序可兼容 Linux 系统，尚未在其它类型的系统实现，因此不保证兼容性)

**python 3.6**

**MySQL 8.0.21**

**Redis 5.0.3**

其余依赖均包含在项目对应的虚拟环境文件夹 (DatabaseVenv) 



## 部署流程

1. clone 本仓库

   ```shell
   git clone https://github.com/charfole/SCNU-CS-2018-DatabaseProject.git
   cd SCNU-CS-2018-DatabaseProject
   ```

2. 在 Linux 环境下安装相关依赖

   安装Python、MySQL和Redis，安装教程可参照菜鸟教程([Python](https://www.runoob.com/python3/python3-install.html), [MySQL](https://www.runoob.com/mysql/mysql-install.html), [Redis](https://www.runoob.com/redis/redis-install.html))

3. 部署 MySQL 项目

   - 创建数据表

     ```shell
     cd MySQL/data
     # 在连接mysql数据库后执行
     source cardTable.sql
     source geoTable.sql
     source userTable.sql
     
     # PS:除此之外，也可以通过Navicat等DBMS修改并执行三个sql文件
     ```

   - 修改数据库连接信息

     ```python
     # 打开 MySQL/backend/app.py
     # 根据个人情况修改user、password和db三个参数，确保连接到希望操纵的数据库
     conn = pymysql.connect(host='127.0.0.1', user='root', password='', db='charfoleTable', charset='utf8') # connect to the database
     ```

   - 部署后端代码

     ```shell
     source ../DatabaseVenv/bin/activate
     cd MySQL/backend
     gunicorn -b :5000 app:app # debug模式运行
     gunicorn -c config.py app:app # config模式运行
     ```

4. 修改 MySQL 客户端对应的 IP 地址

   ```javascript
   // 打开 MySQL/web/page.html
   // 根据个人情况，将所有出现yourIPAddress语句中的yourIPAddress替换为你部署flask的ip（服务器ip或者是虚拟机的ip）
   
   url: "http://yourIPAddress:5000/charfoleTransaction"
   
   // 修改完后，打开page.html并刷新即可成功运行项目
   ```

5. 部署 Redis 项目

   - 创建数据

     ```shell
     cd Redis/data
     
     # 将 Redis/data/charfole.csv 中的数据写入redis的第0号数据库
     python3 readData.py
     ```

   - 部署后端代码

     ```shell
     source ../DatabaseVenv/bin/activate
     cd MySQL/backend
     gunicorn -b :5000 app:app # debug模式运行
     gunicorn -c config.py app:app # config模式运行
     ```

6. 修改 Redis 客户端对应的 IP 地址

   ```javascript
   // 打开 Redis/web/page.html
   // 根据个人情况，将所有出现yourIPAddress语句中的yourIPAddress替换为你部署flask的ip（服务器ip或者是虚拟机的ip）

   url: "http://yourIPAddress:5000/charfoleCRUD"

   // 修改完后，打开page.html并刷新即可成功运行项目
   ```



## 实现的功能

1. MySQL项目
   - 执行基本的 SQL 语句，包括但不限于增删查改、索引、跨表操作
   - 事务支持（execute、commit、rollback）
   - 用户性能查询（仅在后端实现、需提前创建对应的用户并修改后端代码）
2. Redis项目
   - Redis 的基本功能，对数据库中所包含的键值对进行增删查改
   - [基数查询](https://www.runoob.com/redis/redis-hyperloglog.html)（Hyperloglog）功能

由于篇幅所限，更多的功能说明请参照[项目文档](https://github.com/charfole/SCNU-CS-2018-DatabaseProject/tree/master/information/%E9%A1%B9%E7%9B%AE%E6%96%87%E6%A1%A3)。



## 项目截图

1. MySQL

   ![](https://github.com/charfole/SCNU-CS-2018-DatabaseProject/blob/master/information/MySQL%E9%A1%B9%E7%9B%AE%E6%88%AA%E5%9B%BE.png)

2. Redis

   ![](https://github.com/charfole/SCNU-CS-2018-DatabaseProject/blob/master/information/Redis%E9%A1%B9%E7%9B%AE%E6%88%AA%E5%9B%BE.png)

## 写在后面

为了快速兑现课程要求的相关功能，因此项目在性能、鲁棒性方面有所欠缺。如发现有错误或不足，十分欢迎 issue 或 pr。希望能帮助到学习该门课程的同学。
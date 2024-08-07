TinyHttpMysqlServer
=================
### 1. 简介
基于三方库实现C/C++的程序，可以通过使用http服务达到操作数据库(Mysql)的效果
### 2. 使用
#### 1.环境
- linux
- c/c++ 工具链
- mysql数据库，并且开启远端访问
- mysql开发库(mysqlclient)
``` shell
sudo apt update
sudo apt install libmysqlclient-dev
```
#### 2. 运行
``` shell
chmod a+x build.sh
./build.sh
```
#### 3. 配置文件
k=v;为一行;键值对等号附近没有空格<br/>
``` shell 
# 数据库远端ip地址
url=
# 远端登录的用户名
user=
# 远端登录的用户密码
password=
# 要操作的数据库名字
databasename=
# 程序监听的端口
listenport=
```
#### 4. 访问示例
访问地址:http://{ip}:{listenport}/operatorMysql<br/>
ip:这里是程序运行的ip地址<br/>
都是POST方法,以下是报文正文(序列化后的json字符串)，以下是json
##### 1. 增加
``` json
{
    "action":"insert",
    "table_name":"user",
    "username":"tt",
    "passwd":"12345"
}
```
#### 2. 删除
``` json
{
    "action":"delete",
    "table_name":"user",
    "condition":{
        "username":"ttt"
    }
}
```
#### 3. 修改
``` json
{
    "action":"update",
    "table_name":"user",
    "passwd":"123",
    "condition":{
        "username":"tt"
    }
}
```
#### 4. 查询
``` json
{
    "action":"select",
    "table_name":"user",
    "cols":[],
    "order":{
        "column_name":null,
        "end":"asc"
    },
    "limit":3
}
```
#### 5. 返回
``` json
{
    "errno": 0,
    "message": "操作成功",
    "return": [
        {
            "passwd": "123",
            "username": "tt"
        },
        {
            "passwd": "123456",
            "username": "ttt"
        }
    ]
}
```
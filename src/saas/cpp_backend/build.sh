#! /bin/bash

config_file="server.conf"

if [ -f "$config_file" ]; then
    echo "配置文件已存在"
else 
    echo "生成配置文件$config_file ..."

    cat <<EOF > "$config_file"
# 这是配置文件
# 数据库远端ip地址
url=192.168.28.128
# 远端登录的用户名
user=root
# 远端登录的用户密码
password=123456
# 要操作的数据库名字
databasename=testdb
# 程序监听的端口
listenport=8085
EOF
    echo "生成配置文件完成"
fi

make

echo "启动CloudServer..."
./CloudServer $config_file&
echo "CloudServer已启动"
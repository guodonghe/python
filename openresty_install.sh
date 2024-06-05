#!/bin/bash

# 定义OpenResty版本
OPENRESTY_VERSION="1.21.4.2"

# 更新系统并安装必要的依赖
sudo apt update
#sudo apt upgrade -y
sudo apt install -y build-essential libpcre3 libpcre3-dev libssl-dev perl make wget

# 下载并解压OpenResty
wget https://openresty.org/download/openresty-${OPENRESTY_VERSION}.tar.gz
tar -zxvf openresty-${OPENRESTY_VERSION}.tar.gz
cd openresty-${OPENRESTY_VERSION}

# 配置和编译OpenResty
./configure --prefix=/data/sysadmin/soft_installed/openresty \
            --with-luajit \
            --without-http_redis2_module \
            --with-http_iconv_module
            --with-pcre-jit \
            --with-ipv6 \
            --with-http_ssl_module \
            --with-http_realip_module \
            --with-http_stub_status_module \
            --with-http_v2_module

make
sudo make install

# 添加OpenResty路径到环境变量
echo 'export PATH=/data/sysadmin/soft_installed/openresty/nginx/sbin:$PATH' >> ~/.bashrc
source ~/.bashrc

# 验证安装
nginx -v

# 创建简单的OpenResty配置文件
sudo mkdir -p /data/sysadmin/soft_installed/openresty/nginx/conf
sudo bash -c 'cat > /data/sysadmin/soft_installed/openresty/nginx/conf/nginx.conf <<EOF
worker_processes  1;

events {
    worker_connections  1024;
}

http {
    server {
        listen       80;
        server_name  localhost;

        location / {
            default_type "text/plain";
            content_by_lua_block {
                ngx.say("Hello, OpenResty!")
            }
        }
    }
}
EOF'

# 创建systemd服务文件
sudo bash -c 'cat > /etc/systemd/system/openresty.service <<EOF
[Unit]
Description=OpenResty
After=network.target

[Service]
Type=forking
ExecStart=/data/sysadmin/soft_installed/openresty/nginx/sbin/nginx -c /data/sysadmin/soft_installed/openresty/nginx/conf/nginx.conf
ExecReload=/data/sysadmin/soft_installed/openresty/nginx/sbin/nginx -s reload
ExecStop=/data/sysadmin/soft_installed/openresty/nginx/sbin/nginx -s stop
PIDFile=/data/sysadmin/soft_installed/openresty/nginx/logs/nginx.pid
Restart=on-failure

[Install]
WantedBy=multi-user.target
EOF'

# 启动并启用OpenResty服务
sudo systemctl daemon-reload
sudo systemctl start openresty
sudo systemctl enable openresty

# 清理
cd ..
rm -rf openresty-${OPENRESTY_VERSION}
rm openresty-${OPENRESTY_VERSION}.tar.gz

echo "OpenResty ${OPENRESTY_VERSION} 安装和配置完成。请访问 http://localhost 进行验证。"


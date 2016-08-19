# nginx-ssl-docker

参考了umputun/nginx-le https://github.com/umputun/nginx-le

#使用
git clone git@github.com:yalove/nginx-ssl-docker.git

cd nginx-ssl-docker.git 

docker-compose up -d

你需要修改的

-docker-compose.yml
   environment:
   
   TZ=Asia/Shanghai
   
   LETSENCRYPT=true
   
   LE_EMAIL=excia000@gmail.com
   
   LE_FQDN=yalove.me
   
   改为自己的email和domain 
   
-app.conf
   设置自己的nginx siteapp.conf
   
-Dockerfiles\app
   blog目录为app
   
   Dockerfile 通过 ADD 加入app 修改为自己的app
   
   编译安装nginx 可以自己增加删减功能
   

FROM ubuntu:16.04

ENV NGINX_VERSION 1.11.3

#ADD ./conf/sources.list /etc/apt/

RUN apt-get update && apt-get install -y python python-pip python-dev gunicorn supervisor wget libpcre3 libpcre3-dev zlib1g-dev libssl-dev build-essential letsencrypt

RUN useradd -ms /bin/bash nginx

RUN wget http://www.openssl.org/source/openssl-1.0.2d.tar.gz \
  && tar -xvzf openssl-1.0.2d.tar.gz -C /usr/local/src

ADD ./source/nginx-${NGINX_VERSION}.tar.gz /tmp

RUN cd /tmp/nginx-${NGINX_VERSION} \
    && ./configure \
    --prefix=/usr/local/nginx \
    --sbin-path=/usr/sbin/nginx \
    --conf-path=/etc/nginx/nginx.conf \
    --pid-path=/var/run/nginx.pid \
    --user=nginx \
    --group=nginx \
    --error-log-path=/var/log/nginx/error.log \
    --http-log-path=/var/log/nginx/access.log \
    --with-http_ssl_module \
    --with-http_v2_module \
    --with-openssl=/usr/local/src/openssl-1.0.2d \
    --with-http_realip_module \
    --with-http_stub_status_module \
    --with-threads \
    && make \
    && make install

RUN ln -sf /dev/stdout /var/log/nginx/access.log \
    && ln -sf /dev/stderr /var/log/nginx/error.log \
    &&  echo "\ndaemon off;" >> /etc/nginx/nginx.conf \
    && mkdir -p /var/log/supervisor \
    && mkdir -p /usr/share/nginx/html

ADD ./conf/nginx.conf /etc/nginx/nginx.conf

ADD ./conf/supervisord.conf /etc/supervisor/conf.d/supervisord.conf
ADD ./conf/gunicorn.conf /etc/supervisor/conf.d/gunicorn.conf

ADD ./script/run.sh /run.sh
ADD ./script/le.sh /le.sh
RUN chmod 755 /*.sh

RUN mkdir -p /www
ADD ./blog /www
RUN pip install --upgrade pip \
    && pip install -i http://pypi.douban.com/simple -r /www/requirements.txt --trusted-host pypi.douban.com

#RUN pip install --upgrade pip \
#    && pip install  -r /www/requirements.txt

VOLUME /etc/nginx/sites-enabled/
VOLUME /etc/nginx/ssl/
CMD ["/run.sh"]
EXPOSE 80 443

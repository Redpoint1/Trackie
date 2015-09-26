FROM nginx
RUN rm -rf /etc/nginx/conf.d/*
RUN rm /etc/nginx/sites-enabled/default -f
RUN rm /etx/nginx/nginx.conf -f
ADD nginx.conf /etc/nginx/nginx.conf
ADD sites-enabled/ /etc/nginx/sites-enabled

FROM nginx
RUN rm /etx/nginx/nginx.conf -f
ADD uwsgi_params /etc/nginx/uwsgi_params
ADD nginx.conf /etc/nginx/nginx.conf
ADD sites-enabled/ /etc/nginx/sites-enabled

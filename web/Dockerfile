FROM python:3.5-onbuild

#RUN curl -sL https://deb.nodesource.com/setup_7.x | bash -
RUN apt-get update
RUN apt-get install -y binutils libproj-dev gdal-bin
#RUN apt-get install -y nodejs
#RUN npm install -g bower
#RUN npm install
#RUN bower install --allow-root
RUN wget -q https://raw.githubusercontent.com/vishnubob/wait-for-it/b638c190275dc8f9abea5edd3faa69540e0395a9/wait-for-it.sh
RUN chmod --quiet 755 wait-for-it.sh

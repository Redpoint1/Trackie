python manage.py migrate && python manage.py collectstatic --noinput && /usr/local/bin/uwsgi --yaml ./trackie/uwsgi.yml --wsgi-file trackie/wsgi.py --enable-threads

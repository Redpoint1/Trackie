#!/usr/bin/env bash
python manage.py migrate && python manage.py loaddata fixture.json && python manage.py collectstatic --noinput && /usr/local/bin/uwsgi --yaml ./trackie/uwsgi.yml --wsgi-file trackie/wsgi.py --enable-threads

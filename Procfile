web: gunicorn nickstagram.wsgi
release: python manage.py migrate
worker: python manage.py celery worker --loglevel=info
celery_beat: python manage.py celery beat --loglevel=info


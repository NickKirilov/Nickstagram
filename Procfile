web: gunicorn nickstagram.wsgi
release: python manage.py migrate
main_worker: python manage.py celery worker --beat --loglevel=info


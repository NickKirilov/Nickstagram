web: gunicorn nickstagram.wsgi
release: python manage.py migrate
release: celery -A nickstagram worker

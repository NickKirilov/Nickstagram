web: gunicorn nickstagram.wsgi
release: python manage.py migrate
worker: celery worker --app=tasks.app


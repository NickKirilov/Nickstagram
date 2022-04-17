web: gunicorn nickstagram.wsgi
release: python manage.py migrate
worker: nickstagram worker --app=tasks.app

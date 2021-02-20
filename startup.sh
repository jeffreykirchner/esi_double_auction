python manage.py migrate
python manage.py collectstatic
daphne -b 0.0.0.0 ESIDoubleAuction.asgi:application
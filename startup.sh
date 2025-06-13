echo "*** Startup.sh ***"
echo "Run Migrations:"
python manage.py migrate
apt-get update
echo "Install htop:"
apt-get -y install htop
echo "Install redis"
apt-get -y install redis
echo "Start Daphne:"
redis-server & daphne -b 0.0.0.0 _esi_double_auction.asgi:application
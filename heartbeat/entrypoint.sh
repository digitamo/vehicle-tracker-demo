flask db upgrade
cd /
gunicorn -b 0.0.0.0:4000 heartbeat.app:application
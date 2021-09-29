#!bin/bash

# Create necessary directories
mkdir $HOME/web
mkdir $HOME/web/my_site

# Nginx configuration
if apt list nginx; then
	echo "Nginx is already installed"
else
	apt-get install -y nginx
fi
cp $HOME/web/my_site/virtual-machine/nginx.vm.sh /etc/nginx/conf.d
sudo -Hiu johnvorsten bash -c  'envsubst \${WEBAPP_HOSTNAME},\${WEBAPP_INTERNAL_PORT},\${REVERSE_PROXY_HOSTNAME} < /etc/nginx/conf.d/nginx.vm.template' | sudo tee /etc/nginx/conf.d/nginx.conf
chown --recursive johnvorsten:johnvorsten /var/log/nginx

# ODBC
bash $HOME/auto-config/install-odbc.sh
apt install -y unixodbc-dev gcc g++
if apt list python3-pip; then
	echo "python3-pip is already installed"
else
	sudo apt install -y python3-pip
fi


# Certbot
if apt list certbot; then
	echo "Certbot is already installed"
else
	apt-get install -y certbot python-certbot-nginx
	mkdir /etc/letsencrypt/live
	mkdir /etc/letsencrypt/live/johnvorsten.me
	cp "$HOME/web/my_site/virtual-machine/fullchain.pem" "/etc/letsencrypt/live/johnvorsten.me"
	cp "$HOME/web/my_site/virtual-machine/privkey.pem" "/etc/letsencrypt/live/johnvorsten.me"
fi

# Supervisor
apt-get -y install supervisor
# mkdir -p /var/log/supervisor
# mkdir -p /etc/supervisor/conf.d
chown -R johnvorsten:johnvorsten /var/log/supervisor
cp "$HOME/web/my_site/virtual-machine/supervisor.vm.conf" "/etc/supervisor.conf"

# Create virtual env
if apt list virtualenv; then
	echo "Virtualenv is already installed"
else
	apt-get install -y virtualenv
fi

if apt list python3.7; then
	echo "Python 3.7 is already installed"
else
	apt-get install -y python3.7-dev
fi

if [ -d "$HOME/django" ]; then
	echo "Virtual environment already exists at $HOME/django"
else
	virtualenv -p /usr/bin/python3.7 "$HOME/django"
fi

source "$HOME/django/bin/activate"

# Install python packages
if ! pip list --format=columns | grep "^pyodbc" -; then
	pip install -r "$HOME/web/my_site/virtual-machine/requirements.txt"
else
	echo "Python packages already installed"
fi

# Start supervisor (nginx and gunicorn start)
sudo -E 'supervisord -c /etc/supervisor.conf'


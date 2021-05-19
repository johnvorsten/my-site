#!/bin/bash

## This is the main setup script for my Django website ##
## Before running this script, meet the following requirements and dependencies ##
# 1. Install MySQL if not already installed
# 2. Create your database for serving if not already installed
# 3. Create all necessary environment variables (In .bash_profile or .profile)


### Stop supervisord child processes with supervisorctl ###
if supervisorctl status all; then
	supervisorctl stop all
fi

### Create necessary directories ##
if [[ ! -e $HOME/web ]]; then
	mkdir $HOME/web
else
	echo "Directory $HOME/web already exists"
fi
if [[ ! -e $HOME/web/my-site ]]; then
	mkdir $HOME/web/my-site
else
	echo "Directory $HOME/web/my-site already exists"
fi
if [[ ! -e $HOME/web/temp ]]; then
	mkdir $HOME/web/temp
else
	echo "Directory $HOME/web/temp already exists"
fi

### Nginx configuration ###
if dpkg -s nginx; then
	echo "Nginx is already installed"
else
	apt-get install -y nginx
fi
# If a nginx configuration script exists then delete it
if [[ -e /etc/nginx/conf.d/johnvorsten.me.conf ]]; then
	rm /etc/nginx/conf.d/johnvorsten.me.conf
fi
if [[ -e /etc/nginx/conf.d/nginx.vm.template ]]; then
	rm /etc/nginx/conf.d/nginx.vm.template
fi
# Copy template file to nginx configuration directory
cp $HOME/web/temp/deploy-rpi/nginx.vm.template /etc/nginx/conf.d
# Substitute env variables to template file, and generate
# Nginx configuration file
# Try WEBAPP_HOSTNAME=$WEBAPP_HOSTNAME WEBAPP_INTERNAL_PORT=$WEBAPP_INTERNAL_PORT REVERSE_PROXY_HOSTNAME=$REVERSE_PROXY_HOSTNAME
# sudo -Hiu johnvorsten bash -c  'envsubst \${WEBAPP_HOSTNAME},\${WEBAPP_INTERNAL_PORT},\${REVERSE_PROXY_HOSTNAME} < /etc/nginx/conf.d/nginx.vm.template' | sudo tee /etc/nginx/conf.d/nginx.conf
envsubst \${WEBAPP_HOSTNAME},\${WEBAPP_INTERNAL_PORT},\${REVERSE_PROXY_HOSTNAME},\${HOME} < /etc/nginx/conf.d/nginx.vm.template | sudo tee /etc/nginx/conf.d/johnvorsten.me.conf
chown $USER /etc/nginx/conf.d/johnvorsten.me.conf
cat /etc/nginx/conf.d/johnvorsten.me.conf # Send to stdout for verification
# chown --recursive $USER:$USER /var/log/nginx # For logging


### Certbot ###
if dpkg -s certbot; then
	echo "Certbot is already installed"
else
	# https://certbot.eff.org/lets-encrypt/debianstretch-nginx.html
	apt install snapd
	snap install core
	snap refresh core
	snap install --classic certbot
	ln -s /snap/bin/certbot /usr/bin/certbot

	mkdir /etc/letsencrypt/live
	mkdir /etc/letsencrypt/live/johnvorsten.me
	certbot --nginx
	certbot renew --dry-run
fi

### Supervisor ###
# Dont copy configuration file - just run it from its directory
# in "$HOME/web/my_site/virtual-machine/my-site/deploy-rpi/supervisor.vm.conf"
if dpkg -s supervisor; then
	echo "supervisor is already installed"
else
	apt install -y install supervisor
	mkdir -p /var/log/supervisor/johnvorsten.me
	chown -R $USER:$USER /var/log/supervisor/johnvorsten.me
fi

### Create virtual env ###
if dpkg -s virtualenv; then
	echo "Virtualenv is already installed"
else
	apt install -y virtualenv
fi

# Install MySQL C API files with python header files
apt install -y python3-dev default-libmysqlclient-dev build-essential

# Activate virtual environment
if [ -d "$HOME/django" ]; then
	echo "Virtual environment already exists at $HOME/django"
else
	virtualenv -p /usr/bin/python3 "$HOME/django"
fi
source "$HOME/django/bin/activate"

### Install python packages ###
pip install -r "$HOME/web/temp/deploy-rpi/requirements.txt"

### Delete files of old setup and replace ###
rm -r $HOME/web/my-site/my_site
cp -r $HOME/web/temp/my_site $HOME/web/my-site

### Make migrations to SQL database ###
export DEBUG=FALSE
python $HOME/web/my-site/my_site/manage.py makemigrations --settings=my_site.settings
python $HOME/web/my-site/my_site/manage.py migrate

### Start supervisor (nginx and gunicorn start) ###
# With environment HOME=$HOME WEBAPP_INTERNAL_PORT=$WEBAPP_INTERNAL_PORT 
# sudo -E 'supervisord -c /etc/supervisor.conf'
if ps -ef | grep supervsiord; then
	# Supervisord dameon is running, dont restart
	supervisorctl start all
else
	# start supervisord dameon
	supervisord -c $HOME/web/temp/deploy-rpi/supervisor.vm.conf
	# NOTE - The supervisor daemon will not inherit the environment variables
	# From the user unless we pass the sudo -E option
	# This means gunicorn / django will not be able to read important
	# Environment variables (Like SECRET_KEY)
fi
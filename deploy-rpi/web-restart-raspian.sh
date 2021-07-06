#!/bin/bash
# This script attempts to restart the website if it is not running (after a power reset)
# Checks for the following conditions

# Load environment variables
source $HOME/.profile

### Check if supervisord is installed and running ###
supervisord_pid=$(pgrep -f "supervisord")
if [[ supervisord_pid -eq "" ]]; then
    # Supervisord is not running. Attempt to start
    # supervisord -c $HOME/web/temp/deploy-rpi/supervisor.vm.conf
    echo "Supervisord is not running. Attempting to start"
else
    echo "Supervisord is running on PID $supervisord_pid."
fi

### Check if supervisord configuraiton is correct ###
# "(?:(?!grep).)*(supervisord).*$" # Why doesn't this work?
if ps -ef | grep -G "[/]etc/supervisord.conf"; then
    # Change configuration file from default
    # supervisorctl -c $HOME/web/temp/deploy-rpi/supervisor.vm.conf
    # supervisorctl reread
    # supervisorctl update all
    echo "ERROR! supervisord has an incorrect configuration"
    echo ps -ef | grep "[/]etc/supervisord.conf"
else
    echo "Supervisord has the correct configuration"
    echo ps-ef | grep -G "[s]upervisord"
fi


### Everything below is unnecessary.. Supervisor restarts failed processes..
# ### Check if the Gunicorn web app is running via supervisor child process ###
# if supervisorctl status jv-webbap-server; then
#     # Web server is running successfully
#     echo "jv-webapp-server Process is running successfully"
# else
#     # supervisorctl start jv-webapp-server
#     echo "ERROR! jv-webapp-server is not running"
# fi

# ### Check if the proxy server is running ###
# if supervisorctl status jv-proxy; then
#     # Proxy is running successfully
#     echo "jv-proxy Process is running successfully"
# else
#     # supervisorctl start jv-proxy
#     echo "ERROR! jv-proxy is not running"
# fi

# ### If both the Gunicorn web gateway + proxy is running successfully, ###
# if [[ (supervisorctl status jv-proxy) && (supervisorctl status jv-webapp-server) ]]; then
#     # exit 0
#     echo "Success! Exiting script"
# else
#     # exit 1
#     echo "ERROR! Exiting script"
# fi
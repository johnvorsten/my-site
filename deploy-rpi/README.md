## Server management
It is only possible to change the supervisord configuration file by restarting the supervisor daemon.
Kill the supervisord process with `sudo kill -SIGTERM <pid>` where pid is the process ID of supervisord. Then restart supervisord with `sudo supervisord -c $HOME/web/temp/deploy-rpi/supervisor.vm.conf`

## Reverse proxy is not starting...
Figure out what the nginx logs are saying
`sudo supervisorctl tail jv-proxy` will give the log details of a supervisor process
If the nginx process is already started because of an unexpected power failure, then first stop the nginx service using systemd/systemctl
`sudo systemctl stop nginx`
Then, start the proxy using supervisord using `sudo supervisorctl start jv-proxy`

## Issues with power cycle
When the power cycles, Nginx and Supervisord start with their default configurations under either a) /etc/init.d or /etc/systemd/system
The default init script is stored under /etc/init.d/supervisor. Change the default configuration script location in the init.d script as follows:
```bash
if [ -f /home/web/app/temp/deploy-rpi/supervisor.vm.conf ] ; then
  DAEMON_OPTS="-c /home/web/temp/deploy-rpi/supervisor.vm.conf $DAEMON_OPTS"
else
  DAEMON_OPTS="-c /etc/supervisor/supervisord.conf $DAEMON_OPTS"
fi
```

## Transferring letsencrypt archive and backup files
Backup files `tar cvzf /home/web/letsencrypt_archive.tar.gz /etc/letsencrypt`
Transfer files with SCP `scp username@hostname:/home/web/letsencrypt_archive.tar.gz C:\path\to\save\letsencrypt_archive.tar.gz`
Decompress once copied to new server `tar zxvf /path/to/letsencrypt_archive.tar.gz -C /`. This will docompress to /etc/letsencrypt with all symlinks preserved
Check if certificates landed correctly `certbot renew --dry-run

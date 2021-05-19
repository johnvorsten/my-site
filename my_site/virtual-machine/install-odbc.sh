#!bin/bash
curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
echo "Key added to apt-key successfully"

# Download appropriate package for the OS version

# Ubuntu 18.04
curl https://packages.microsoft.com/config/ubuntu/18.04/prod.list | tee /etc/apt/sources.list.d/mssql-release.list

apt-get update
if dpkg --get-selections | grep "^msodbcsql17" -; then
	echo "msodbcsql17 is already installed"
else
	ACCEPT_EULA=Y apt-get install msodbcsql17
fi

if dpkg --get-selections | grep "^mssql-tools" -; then
	echo "mssql-tools is already installed"
else
	# optional: for bcp and sqlcmd
	ACCEPT_EULA=Y apt-get install mssql-tools
fi

if [[ "$PATH" == *"/opt/mssql-tools/bin"* ]]; then
	echo "/opt/mssql-tools/bin is already in PATH"
else
	echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bashrc
	echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >>~/.bash_profile
fi

source ~/.bashrc
# optional: for unixODBC development headers
apt-get install unixodbc-dev
apt install -y unixodbc-dev gcc g++

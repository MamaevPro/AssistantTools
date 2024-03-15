#!/bin/bash

# Help
if [ "$#" -ne 1 ]; then
    echo "#-------------------------------------------------#"
    echo "# Запуск сервиса Ассистент от имени пользователя  #"
    echo "# This script for start assistant service as user #"
    echo "#-------------------------------------------------#"
    echo "Example usage: bash $0 [username]"
    exit 1
fi

# Check run as root?
if [ "x$(id -u)" != 'x0' ]; then
    echo 'Error: this script can only be executed by root'
    exit 1
fi

# Check user $1 exists?
if [ -z "$(grep ^$1: /etc/passwd)" ] && [ ! -z "$1" ]; then
    echo "Error: user $1 not exists"
    exit 1
fi

# Check user group $1 exists?
if [ -z "$(grep ^$1: /etc/group)" ] && [ ! -z "$1" ]; then
    echo "Error: group $1 not exists"
    exit 1
fi

systemctl stop assistant
chown -R $1 /opt/assistant/log/
chmod 765 /opt/assistant/bin/asts

sed -i "s/\(User *= *\).*/\1$1/" /lib/systemd/system/assistant.service
sed -i "s/\(Group *= *\).*/\1$1/" /lib/systemd/system/assistant.service

systemctl daemon-reload
systemctl start assistant
echo "Done!"
sleep 3
systemctl status assistant
ps -aux | grep /opt/assistant/bin/asts | grep $1
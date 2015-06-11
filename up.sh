#!/bin/bash

function refresh_hosts {
	# Clear existing rabbit entries if any
	cat /etc/hosts | grep -v rabbit | sudo tee /etc/hosts > /dev/null
	sudo blockade status | grep -v NODE | awk '{ print $4 " " $1}' | sudo tee --append /etc/hosts > /dev/null
}

if [ "$1" = "--refresh" ]; then
	echo "Refreshing hosts"
	refresh_hosts
	exit
fi;

# Bring up the containers and add the new entries
sudo blockade up

refresh_hosts

echo "Waiting for rabbit to come up and setting HA policy"
sleep 5
sudo rabbitmqctl -n rabbit@rabbit1 set_policy ha-all "^ha\." '{"ha-mode":"all"}'

echo "Blockade up and host entries added"

VAGRANTFILE_API_VERSION = "2"
BOX_NAME = ENV['BOX_NAME'] || "ubuntu/trusty64"
script = <<SCRIPT
#!/bin/bash -e

if [ ! -f /etc/default/docker ]; then
  echo "/etc/default/docker not found -- is docker installed?" >&2
  exit 1
fi

apt-get update
apt-get -y install lxc python-pip python-virtualenv

if (source /etc/default/docker && [[ $DOCKER_OPTS != *lxc* ]]); then

  echo "Adjusting docker configuration to use LXC driver, and restarting daemon." >&2

  echo '# Blockade requires the LXC driver for now' >> /etc/default/docker
  echo 'DOCKER_OPTS="$DOCKER_OPTS -e lxc"' >> /etc/default/docker
  service docker restart

fi

cd /vagrant

export PIP_DOWNLOAD_CACHE=/vagrant/.pip_download_cache

pip install blockade

curl -L https://github.com/docker/compose/releases/download/1.2.0/docker-compose-`uname -s`-`uname -m` > /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

SCRIPT

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|

  config.vm.box = BOX_NAME

  if Vagrant.has_plugin?("vagrant-cachier")
    config.cache.scope = :box
  end

  config.vm.network "private_network", ip: "192.168.59.19"

  config.vm.provider :virtualbox do |vb, override|
  end

  config.vm.provision "docker",
    images: ["ubuntu"]

  # setup our env
  config.vm.provision "shell", inline: script
end

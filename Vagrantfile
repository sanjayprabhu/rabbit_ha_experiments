
VAGRANTFILE_API_VERSION = "2"
BOX_NAME = ENV['BOX_NAME'] || "ubuntu/trusty64"
script = <<SCRIPT
#!/bin/bash -e

if [ ! -f /etc/default/docker ]; then
  echo "/etc/default/docker not found -- is docker installed?" >&2
  exit 1
fi

# Get latest rabbitmq for rabbitmqctl
echo "deb http://www.rabbitmq.com/debian/ testing main" >> /etc/apt/sources.list

wget https://www.rabbitmq.com/rabbitmq-signing-key-public.asc
apt-key add rabbitmq-signing-key-public.asc
rm rabbitmq-signing-key-public.asc

apt-get update
apt-get -y install lxc python-pip python-virtualenv rabbitmq-server

# We don't need the server on the vagrant box
rabbitmqctl stop

# use the same cookie so we can talk to the remote instances
cp /vagrant/rabbitmq-cluster/server/erlang.cookie /var/lib/rabbitmq/.erlang.cookie

if (source /etc/default/docker && [[ $DOCKER_OPTS != *lxc* ]]); then

  echo "Adjusting docker configuration to use LXC driver, and restarting daemon." >&2

  echo '# Blockade requires the LXC driver for now' >> /etc/default/docker
  echo 'DOCKER_OPTS="$DOCKER_OPTS -e lxc"' >> /etc/default/docker
  service docker restart

fi

cd /vagrant

export PIP_DOWNLOAD_CACHE=/vagrant/.pip_download_cache

pip install -r requirements.txt

curl -L https://github.com/docker/compose/releases/download/1.2.0/docker-compose-`uname -s`-`uname -m` > /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

docker build -t rabbitmq-base rabbitmq-cluster/base
docker build -t rabbitmq-cluster rabbitmq-cluster/server

SCRIPT

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|

  config.vm.box = BOX_NAME

  if Vagrant.has_plugin?("vagrant-cachier")
    config.cache.scope = :box
  end

  config.vm.network "private_network", ip: "192.168.59.19"

  config.vm.provider :virtualbox do |vb, override|
    vb.memory = 1024
  end

  config.vm.provision "docker",
    images: ["ubuntu"]

  # setup our env
  config.vm.provision "shell", inline: script
end

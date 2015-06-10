Install vagrant.

And then:

```
vagrant up
vagrant ssh
# now, within vagrant
cd /vagrant
./up.sh
```


This should give you a rabbitmq cluster accessible at `rabbit1`, `rabbit2` etc.

You can publish and consume by running `python rabbit_test.py`

Credits:
 - https://github.com/bijukunjummen/docker-rabbitmq-cluster
 - https://github.com/dcm-oss/blockade
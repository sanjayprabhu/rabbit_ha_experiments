Install vagrant.

And then:

```
vagrant up
vagrant ssh
# now, within vagrant
cd /vagrant
sudo blockade up
```


This should give you a rabbitmq cluster.

You can publish and consume by running `python rabbit_test.py`
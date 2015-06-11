import time

import argparse
import pika

QUEUE = 'ha.hello'

def keep_producing(channel, key, sleep_time=0.5, body='Hello World!'):
  props = pika.BasicProperties(delivery_mode = 2) # make message persistent
  i = 0
  while True:
    text = "%s [%d]" % (body, i)
    channel.basic_publish(exchange='', routing_key=key, body=text, properties=props)
    print " [x] Sent '%s'" % text
    i += 1
    time.sleep(sleep_time)

def keep_consuming(channel, queue):
  def callback(ch, method, properties, body):
    print " [x] Received %r" % (body,)
    ch.basic_ack(delivery_tag=method.delivery_tag)

  print ' [*] Waiting for messages. To exit press CTRL+C'
  channel.basic_consume(callback, queue=queue, no_ack=False)
  channel.start_consuming()

def get_channel(host, port, queue):
  connection = pika.BlockingConnection(pika.ConnectionParameters(host=args.host, port=args.port))
  channel = connection.channel()
  channel.queue_declare(queue=queue, durable=True)
  return channel


if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='RabbitMq Tester', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
  parser.add_argument('mode', type=str, default='produce', choices=['produce', 'consume'])
  parser.add_argument('--host', type=str, default="localhost", help='Rabbitmq Host')
  parser.add_argument('--port', type=int, default=5672, help='RabbitMq port')
  args = parser.parse_args()

  channel = get_channel(args.host, args.port, queue=QUEUE)

  if args.mode == 'produce':
    keep_producing(channel, key=QUEUE)
  elif args.mode == 'consume':
    keep_consuming(channel, queue=QUEUE)


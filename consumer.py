import os

import pika
from dotenv import load_dotenv

load_dotenv()

username = os.getenv('RABBIT_MQ_ID')
password = os.getenv('RABBIT_MQ_PASSWORD')
vhost_name = os.getenv('RABBIT_MQ_VHOST')
host = os.getenv('RABBIT_MQ_HOST')
port = os.getenv('RABBIT_MQ_PORT')

credentials = pika.PlainCredentials(username=username, password=password)
connection = pika.BlockingConnection(pika.ConnectionParameters(host=host, port=port, credentials=credentials, virtual_host=vhost_name))
channel = connection.channel()

exchange_name = 'interceptor.ex'
channel.exchange_declare(exchange=exchange_name, exchange_type='topic')

result = channel.queue_declare('dflex.interceptor.q', exclusive=True)
queue_name = result.method.queue

binding_key = 'interceptor.*.*'
channel.queue_bind(exchange=exchange_name, queue=queue_name, routing_key=binding_key)

print(' [*] Waiting for logs. To exit press CTRL+C')


def callback(ch, method, properties, body):
    print(f" [x] {method.routing_key} - {body}")


channel.basic_consume(
    queue=queue_name, on_message_callback=callback, auto_ack=True)

channel.start_consuming()
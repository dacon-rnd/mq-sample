import os
import sys
from dotenv import load_dotenv
import pika

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

routing_key = sys.argv[1] if len(sys.argv) > 1 else 'interceptor.p1.s1'
message = 'Hello World!'
channel.basic_publish(
    exchange=exchange_name, routing_key=routing_key, body=message)
print(f" [x] Sent {routing_key}:{message}")
connection.close()
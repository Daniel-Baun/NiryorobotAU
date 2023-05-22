#!/usr/bin/env python3
import pika
import json
import time
from datetime import datetime, timezone
from DB_functions import is_order_processing, is_order_waiting
import psycopg2
import configparser

#The user needs to input database name, user name, password, host and port in config.ini
config = configparser.ConfigParser()
config.read('config.ini')

db_name = config.get('database', 'db_name')
user = config.get('database', 'user')
password = config.get('database', 'password')
host = config.get('database', 'host')
port = config.get('database', 'port')

#connect to the database
connection = psycopg2.connect(database = db_name, user = user, password = password, host = host, port = port)
cur = connection.cursor()

#Connect to the RabbitMQ server
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
print("Declaring exchange")
#Declare the exchange on the RabbitMQ server, when using RabbitMQFMU, the exchange name must be fmi_digital_twin for the direct exchange
channel.exchange_declare(exchange='fmi_digital_twin', exchange_type='direct')

#The code below can be needed if you want data from the co-simulation
#print("Creating queue")
#result = channel.queue_declare(queue='', exclusive=True)
#queue_name = result.method.queue
#channel.queue_bind(exchange='fmi_digital_twin', queue=queue_name,
#                   routing_key='data.from_cosim')

#The time_sleep variable is used to set the time between each message is sent to the RabbitMQ server
#This is the time between each time the function publish() is called
time_sleep = 0.1

print(' [*] Waiting for logs. To exit press CTRL+C, sleep time [ms]: ', time_sleep*1000)

def publish():
    while True:
        msg = {}
        msg['time']= datetime.now(timezone.utc).astimezone().isoformat(timespec='milliseconds')
        msg['waiting'] = is_order_waiting(cur)
        msg['processing'] = is_order_processing(cur)
        print(" [x] Sent %s" % json.dumps(msg))
        channel.basic_publish(exchange='fmi_digital_twin',
	    			routing_key='data.to_cosim',
	    			body=json.dumps(msg))
        time.sleep(time_sleep)

publish()

#The code below can be needed if you want data from the co-simulation (added in another script)
#def callback(ch, method, properties, body):
#    print(" [x] %r" % body)
#    if "waiting for input data for simulation" in str(body):
#      publish()

#channel.basic_consume(
#   queue=queue_name, on_message_callback=callback, auto_ack=True)
#channel.start_consuming()
connection.close()
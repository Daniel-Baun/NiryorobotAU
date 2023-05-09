#!/usr/bin/env python3
import pika
import json
import time
from datetime import datetime, timezone
from DB_functions import is_order_waiting

import psycopg2


connection = psycopg2.connect(database = "main_db", user = "au682915", password = "admin", host = "localhost", port = "5432")
cur = connection.cursor()

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
print("Declaring exchange")
channel.exchange_declare(exchange='fmi_digital_twin', exchange_type='direct')
#print("Creating queue")
#result = channel.queue_declare(queue='', exclusive=True)
#queue_name = result.method.queue
#channel.queue_bind(exchange='fmi_digital_twin', queue=queue_name,
#                   routing_key='data.from_cosim')
time_sleep = 1

print(' [*] Waiting for logs. To exit press CTRL+C, sleep time [ms]: ', time_sleep*1000)

def publish():
    while True:
        #if (is_order_waiting(cur)):
        dt=datetime.strptime('2019-01-04T16:41:24+0200', "%Y-%m-%dT%H:%M:%S%z")
        print(dt)
        msg = {}
        msg['time']= dt.isoformat()
        msg['time']= datetime.now(tz = datetime.now().astimezone().tzinfo).isoformat(timespec='milliseconds')
        msg['waiting'] = is_order_waiting(cur)
        print(" [x] Sent %s" % json.dumps(msg))
        channel.basic_publish(exchange='fmi_digital_twin',
	    			routing_key='data.to_cosim',
	    			body=json.dumps(msg))
        time.sleep(time_sleep)
        #else:
            #time.sleep(time_sleep)

publish()
#def callback(ch, method, properties, body):
#    print(" [x] %r" % body)
#    if "waiting for input data for simulation" in str(body):
#      publish()

#channel.basic_consume(
#   queue=queue_name, on_message_callback=callback, auto_ack=True)
#channel.start_consuming()
connection.close()
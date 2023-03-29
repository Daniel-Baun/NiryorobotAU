import os
import sys
import math
import copy
import random
import time
import yaml
from threading import Lock, Thread
from pyniryo import *
from poses import *
from odoo import *
from settings import *
import queue
from multiprocessing import Process, Queue


connection = psycopg2.connect(database = "main_db", user = "au682915", password = "admin", host = "localhost", port = "5432")

cur = connection.cursor()



def match_table_ref_to_robots(order: str):
    try:
        match order:
                case 'GR01':
                    return (ObjectShape.SQUARE, ObjectColor.GREEN)
                case 'GC01':
                    return (ObjectShape.CIRCLE, ObjectColor.GREEN)
                case 'RR01':
                    return (ObjectShape.SQUARE, ObjectColor.RED)
                case 'RC01':
                    return (ObjectShape.CIRCLE, ObjectColor.RED)
                case 'BR01':
                    return (ObjectShape.SQUARE, ObjectColor.BLUE)
                case 'BC01':
                    return (ObjectShape.CIRCLE, ObjectColor.BLUE)
    except:
        print("Input invalid or does not exist in database")


def execute_order_66(order: str):
    shape = match_table_ref_to_robots(order)[0]
    color = match_table_ref_to_robots(order)[1]
    
    return shape, color

def while_loop(q):
    restart = True
    while restart:       
        while True:
            restart = False
            print("Got here 0")
            #user_input = "GR01"
            user_input = input("Enter order id: ")
            print("Got here 1")
            
            if user_input.lower() == "exit":
                break
            
            check_connection('main_db', 'au682915', 'admin', 'localhost', '5432')
            if (get_quantity_product(user_input, cur)==0):
                print("Error, no avaliable stock for your order id")
                restart = True
                break
            
            sanitised_input = match_table_ref_to_robots(user_input)
            q.put(sanitised_input)
            print(q)
            change_quantity_product(user_input, cur, connection)
if __name__ == "__main__":
    q = Queue()
    p = Process(target=while_loop, args=(q,))
    p.start()
    #p.join()


#SELECT id as temp_id,desc_item
#FROM public.orders
#WHERE id = (SELECT MIN(id) FROM public.orders) AND status = 'WAITING';
#UPDATE public.orders 
#SET status='PROCESSING' 
#WHERE id = (SELECT Min(id) FROM public.orders WHERE status = 'WAITING');



                
         
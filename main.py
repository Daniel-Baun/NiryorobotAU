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
import multiprocessing

connection = psycopg2.connect(database = "main_db", user = "au682915", password = "admin", host = "localhost", port = "5432")

cur = connection.cursor()


orders_queue = queue.Queue()


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

def while_loop():
    print(match_table_ref_to_robots("GR01"))
    restart = True
    while restart:       
        while True:
            restart = False
            user_input = input("Enter order id ")
            
            if user_input.lower() == "exit":
                break
            
            check_connection('main_db', 'au682915', 'admin', 'localhost', '5432')
            if (get_quantity_product(user_input, cur)==0):
                print("Error, no avaliable stock for your order id")
                restart = True
                break
            
            sanitised_input = match_table_ref_to_robots(user_input)
            orders_queue.put(sanitised_input)
            print(orders_queue)
            change_quantity_product(user_input, cur, connection)
if __name__ == "__main__":
    while_loop()



                
         
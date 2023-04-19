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
from DB_functions import *
from settings import *
import queue
from multiprocessing import Process, Queue


connection = psycopg2.connect(database = "main_db", user = "au682915", password = "admin", host = "localhost", port = "5432")

cur = connection.cursor()






def execute_order_66(order: str):
    shape = match_table_ref_to_robots(order)[0]
    color = match_table_ref_to_robots(order)[1]
    
    return shape, color

def send_order(order: str, number: str):
    check_connection('main_db', 'au682915', 'admin', 'localhost', '5432')
    if not(product_avaliable(order, number, cur)):
        print("Error, no avaliable stock for your order id")
        
        change_quantity_product(order, cur, connection)
        put_queue(cur, connection, order, number)

def while_loop():
    restart = True
    while restart:       
        while True:
            restart = False
            print("Got here 0")
            #user_input = "GR01"
            user_input_item_desc = input("Enter order item description: ")
            user_input_product_no = int(input("Enter no items: "))

            print("Got here 1")
            
            if user_input_item_desc.lower() == "exit":
                break
            
            check_connection('main_db', 'au682915', 'admin', 'localhost', '5432')
            if not(product_avaliable(user_input_item_desc, user_input_product_no, cur)):
                print("Error, no avaliable stock for your order id")
                restart = True
                break
            
            change_quantity_product(user_input_item_desc, cur, connection)
            put_queue(cur, connection, user_input_item_desc, user_input_product_no)
if __name__ == "__main__":
    #put_queue(cur, connection, "GR01", 1)
    while_loop()










                
         
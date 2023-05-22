import psycopg2
from pyniryo import *
import pyautogui as pg

#Function to check connection to database
def check_connection(database: str, user: str, password: str, host: str, port: str):
    try:
        conn = psycopg2.connect(database = database, user = user, password = password, host = host, port = port, connect_timeout=1)
        conn.close()
        return True
    except psycopg2.Error:
        return False

#Function to match table reference in the database to the Niryo Ned 2 robot
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

#Function to get quantity of product in database
#The quantity is the number of products in stock, which is inserted in Odoo
def get_quantity_product(product: str, cursor):

    query = ("SELECT public.stock_quant.quantity "+ 
            "FROM public.stock_quant " + 
            "JOIN public.product_product ON public.stock_quant.product_id = public.product_product.id "+
            "WHERE public.product_product.default_code = %s AND public.stock_quant.quantity > -1")
    cursor.execute(query, (product,))
    data = cursor.fetchone()
    if data == None:
        return 0
    return int(data[0])

#Function to change quantity of product in database by subtratcing 1
def change_quantity_product(product: str, cursor, conn):
    query = ("UPDATE public.stock_quant " +
            "SET quantity = quantity - 1 " +
            "FROM public.product_product " +
            "WHERE public.stock_quant.product_id = public.product_product.id " +
            "AND public.product_product.default_code = %s AND public.stock_quant.quantity > 0")
    cursor.execute(query, (product,))
    conn.commit()
    return

#Function to get the minimum id of the order that is waiting and where the failure status is false
def pop_queue(cursor):
    query = ("SELECT id, desc_item "+
            "FROM public.orders "+
            "WHERE id = (SELECT MIN(id) FROM public.orders WHERE status = 'WAITING' AND failure_status = false)")
    cursor.execute(query)
    return cursor.fetchone()

#Function to get the minimum id of the order that is processing and where the failure status is false
def finished_order(cursor):
    query = ("SELECT id, desc_item "+
            "FROM public.orders "+
            "WHERE id = (SELECT MIN(id) FROM public.orders WHERE status = 'PROCESSING' AND failure_status = false)")
    cursor.execute(query)
    return cursor.fetchone()

#Function to update the status of the order to either waiting, processing or done
def update_order_status(cursor, conn, id, status):
    query = ("UPDATE public.orders "+
             "SET status =%s "+ 
             "WHERE id = %s")
    cursor.execute(query,(status,id,))
    conn.commit()
    return

#Function to check if the product is avaliable in the database based on the quantity
def product_avaliable(product, no_product, cursor):
    return (get_quantity_product(product, cursor) >= no_product)

#Function to put things in a queue, so that multiple orders can be waiting
def put_queue(cursor, conn, desc_item, no_product):
    if (product_avaliable(desc_item, no_product, cursor)):
        query = ("INSERT INTO public.orders (desc_item, no_product)"+
                 "VALUES(%s, %s)")
        cursor.execute(query, (desc_item, no_product,))
        conn.commit()
        return
    else:
        print("Stock not avaliable for order")
        return

#Function to check if there is an order waiting in the database
def is_order_waiting(cursor):
    query = ("SELECT status "+
            "FROM public.orders "+
            "WHERE status = 'WAITING' AND failure_status = false")
    cursor.execute(query)
    if (cursor.rowcount == 0):
        return False
    return True

#Function to check if there is an order processing in the database
def is_order_processing(cursor):
    query = ("SELECT status "+
            "FROM public.orders "+
            "WHERE status = 'PROCESSING' AND failure_status = false")
    cursor.execute(query)
    if (cursor.rowcount == 0):
        return False
    return True

def check_order_failed(cursor, id):
    query = ("SELECT failure_status "+
            "FROM public.orders "+
            "WHERE id = (SELECT max(id) FROM public.orders)")
    cursor.execute(query)
    bool_value = cursor.fetchone()
    if(cursor.rowcount == 0):
        return False
    else:
        if(bool_value[0]):
            pg.alert(text="Time limit exceeded for order \n Fix system manually and reset the system", title="Order failed", button="OK")
            return True
        return False
    
    







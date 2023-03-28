#from odoo import api, models, fields
import psycopg2

connection = psycopg2.connect(database = "main_db", user = "au682915", password = "admin", host = "localhost", port = "5432")
#def connect_to_database():
#   
#    
#
#    return connection
product_chosen = 'GR01'

cur = connection.cursor()

def check_connection(database: str, user: str, password: str, host: str, port: str):
    try:
        conn = psycopg2.connect(database = database, user = user, password = password, host = host, port = port, connect_timeout=1)
        conn.close()
        return True
    except psycopg2.Error:
        return False


def get_quantity_product(product: str, cursor):

    query = ("SELECT public.stock_quant.quantity, public.product_product.id "+ 
            "FROM public.stock_quant " + 
            "JOIN public.product_product ON public.stock_quant.product_id = public.product_product.id "+
            "WHERE public.product_product.default_code = %s AND public.stock_quant.quantity > -1")
    cursor.execute(query, (product,))
    
    return cursor.fetchone()

def change_quantity_product():

    
print(get_quantity_product('GR01', cur))

connection.close()  

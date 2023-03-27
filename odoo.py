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

cur.execute("SELECT public.stock_quant.quantity, public.product_product.id "+ 
            "FROM public.stock_quant " + 
            "JOIN public.product_product ON public.stock_quant.product_id = public.product_product.id "+
            "WHERE public.product_product.default_code = 'GR01' AND public.stock_quant.quantity > -1")

rows = cur.fetchall()

for row in rows:
    print(row)

connection.close()  

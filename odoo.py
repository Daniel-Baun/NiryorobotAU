#from odoo import api, models, fields
import psycopg2



def check_connection(database: str, user: str, password: str, host: str, port: str):
    try:
        conn = psycopg2.connect(database = database, user = user, password = password, host = host, port = port, connect_timeout=1)
        conn.close()
        return True
    except psycopg2.Error:
        return False


def get_quantity_product(product: str, cursor):

    query = ("SELECT public.stock_quant.quantity "+ 
            "FROM public.stock_quant " + 
            "JOIN public.product_product ON public.stock_quant.product_id = public.product_product.id "+
            "WHERE public.product_product.default_code = %s AND public.stock_quant.quantity > -1")
    cursor.execute(query, (product,))
    
    return int(cursor.fetchone()[0])

def change_quantity_product( product: str, cursor, conn):
    query = ("UPDATE public.stock_quant " +
            "SET quantity = quantity - 1 " +
            "FROM public.product_product " +
            "WHERE public.stock_quant.product_id = public.product_product.id " +
            "AND public.product_product.default_code = %s AND public.stock_quant.quantity > 0")
    cursor.execute(query, (product,))
    conn.commit()
    return

def pop_queue(cursor):
    query = ("SELECT id, desc_item "+
            "FROM public.orders "+
            "WHERE id = (SELECT MIN(id) FROM public.orders WHERE status = 'WAITING')")
    cursor.execute(query)
    return cursor.fetchone()

def update_order_status(cursor, conn, id, status):
    query = ("UPDATE public.orders "+
             "SET status =%s "+ 
             "WHERE id = %s")
    cursor.execute(query,(status,id,))
    conn.commit()
    return

def put_queue(cursor, conn, desc_item, no_product):
    query = ("INSERT INTO public.orders (desc_item, no_product)"+
             "VALUES(%s, %s)")
    cursor.execute(query, (desc_item, no_product,))
    conn.commit()
    return


#SELECT id as temp_id,desc_item
#FROM public.orders
#WHERE id = (SELECT MIN(id) FROM public.orders) AND status = 'WAITING';
#UPDATE public.orders 
#SET status='PROCESSING' 
#WHERE id = (SELECT Min(id) FROM public.orders WHERE status = 'WAITING');

    
#print(check_connection('main_db', 'au682915', 'admin', 'localhost', '5432'))
#print(get_quantity_product('GR01', cur))
#change_quantity_product('GR01', cur)
#print(type(get_quantity_product('GR01', cur)))
#print(get_quantity_product('GR01', cur))


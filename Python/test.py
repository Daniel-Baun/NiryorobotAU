import unittest
import psycopg2

from DB_functions import *

class TestDBFunctions(unittest.TestCase):
    def test_check_connection(self):
        database = "main_db"
        user = "au682915"
        password = "admin"
        host = "localhost"
        port = "5432"
        port1 = "5433"
        result = check_connection(database, user, password, host, port)
        result1 = check_connection(database, user, password, host, port1)
        self.assertEqual(result, True)
        self.assertEqual(result1, False)


    def test_match_table_ref_to_robots(self):
        green_rectangle = "GR01"
        green_circle = "GC01"
        red_rectangle = "RR01"
        red_circle = "RC01"
        blue_rectangle = "BR01"
        blue_circle = "BC01"
        not_in_database = "not_in_database"

        result_GR = match_table_ref_to_robots(green_rectangle)
        result_GC = match_table_ref_to_robots(green_circle)
        result_RR = match_table_ref_to_robots(red_rectangle)
        result_RC = match_table_ref_to_robots(red_circle)
        result_BR = match_table_ref_to_robots(blue_rectangle)
        result_BC = match_table_ref_to_robots(blue_circle)
        result_not_in_database = match_table_ref_to_robots(not_in_database)

        self.assertEqual(result_GR, (ObjectShape.SQUARE, ObjectColor.GREEN))
        self.assertEqual(result_GC, (ObjectShape.CIRCLE, ObjectColor.GREEN))
        self.assertEqual(result_RR, (ObjectShape.SQUARE, ObjectColor.RED))
        self.assertEqual(result_RC, (ObjectShape.CIRCLE, ObjectColor.RED))
        self.assertEqual(result_BR, (ObjectShape.SQUARE, ObjectColor.BLUE))
        self.assertEqual(result_BC, (ObjectShape.CIRCLE, ObjectColor.BLUE))
        self.assertEqual(result_not_in_database, None)

    def test_get_quantity_product(self):

        product = "GR01"
        DB_conn = psycopg2.connect(database = "main_db", user = "au682915", password = "admin", host = "localhost", port = "5432")
        cursor = DB_conn.cursor()
        result = get_quantity_product(product, cursor)
        self.assertEqual(type(result), int)
        self.assertGreaterEqual(result, 0)
        product1 = "not_in_database"
        result = get_quantity_product(product1, cursor)
        self.assertEqual(result, False)

    def test_pop_queue(self):

        DB_conn = psycopg2.connect(database = "main_db", user = "au682915", password = "admin", host = "localhost", port = "5432")
        cursor = DB_conn.cursor()
        result = pop_queue(cursor)
        self.assertEqual(result, None)

    def test_finished_order(self):

        DB_conn = psycopg2.connect(database = "main_db", user = "au682915", password = "admin", host = "localhost", port = "5432")
        cursor = DB_conn.cursor()
        result = finished_order(cursor)
        self.assertEqual(result, None)

    def test_product_avaliable(self):

        DB_conn = psycopg2.connect(database = "main_db", user = "au682915", password = "admin", host = "localhost", port = "5432")
        cursor = DB_conn.cursor()
        product = "BR01"
        product_no = 1
        result = product_avaliable(product, product_no, cursor)
        self.assertEqual(result, True)

    def test_is_order_waiting(self):

        DB_conn = psycopg2.connect(database = "main_db", user = "au682915", password = "admin", host = "localhost", port = "5432")
        cursor = DB_conn.cursor()
        result = is_order_waiting(cursor)
        self.assertEqual(result, False)

    def test_is_order_processing(self):
        DB_conn = psycopg2.connect(database = "main_db", user = "au682915", password = "admin", host = "localhost", port = "5432")
        cursor = DB_conn.cursor()
        result = is_order_processing(cursor)
        self.assertEqual(result, False)






if __name__ == '__main__':
    unittest.main()


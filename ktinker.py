import tkinter as tk
import customtkinter as ct
from DB_functions import *
from settings import *

connection = psycopg2.connect(database = "main_db", user = "au682915", password = "admin", host = "localhost", port = "5432")

cur = connection.cursor()

#window = tk.Tk()
#
#label = tk.Label(text="Hello World", font=("Roboto", 20))
#label.pack()
#window.mainloop()
root = ct.CTk()
root.geometry("500x500")
ct.set_appearance_mode("dark")
text_box = ct.CTkTextbox(master=root, font=("Roboto", 20), width=300, height=70)
def send_order():
    print(type(text_box.get("0.0", tk.END)))
    print(text_box.get("0.0", tk.END) == "1 - Green Rectangle")

    if(str(text_box.get("0.0", tk.END)) == "1 - Green Rectangle"):
        print("got here")
        check_connection('main_db', 'au682915', 'admin', 'localhost', '5432')
        print("got here 2")
        if not(product_avaliable("GR01", "1", cur)):
            print("got here 3")
            print("Error, no avaliable stock for your order id")
            print("got here 4")
            change_quantity_product("GRO1", cur, connection)
            print("got here 5")
            put_queue(cur, connection, "GR01", "1")
            print("got here 6")
    elif(text_box.get("0.0", tk.END) == "1 - Green Circle"):
        check_connection('main_db', 'au682915', 'admin', 'localhost', '5432')
        if not(product_avaliable("GC01", "1", cur)):
            print("Error, no avaliable stock for your order id")

            change_quantity_product("GC01", cur, connection)
            put_queue(cur, connection, "GC01", "1")
    elif(text_box.get("0.0", tk.END) == "1 - Red Rectangle"):
        check_connection('main_db', 'au682915', 'admin', 'localhost', '5432')
        if not(product_avaliable("RR01", "1", cur)):
            print("Error, no avaliable stock for your order id")

            change_quantity_product("RR01", cur, connection)
            put_queue(cur, connection, "RR01", "1")
    elif(text_box.get("0.0", tk.END) == "1 - Red Circle"):
        check_connection('main_db', 'au682915', 'admin', 'localhost', '5432')
        if not(product_avaliable("RC01", "1", cur)):
            print("Error, no avaliable stock for your order id")

            change_quantity_product("RC01", cur, connection)
            put_queue(cur, connection, "RC01", "1")
    elif(text_box.get("0.0", tk.END) == "1 - Blue Rectangle"):
        check_connection('main_db', 'au682915', 'admin', 'localhost', '5432')
        if not(product_avaliable("BR01", "1", cur)):
            print("Error, no avaliable stock for your order id")

            change_quantity_product("BR01", cur, connection)
            put_queue(cur, connection, "BR01", "1")
    elif(text_box.get("0.0", tk.END) == "1 - Blue Circle"):
        check_connection('main_db', 'au682915', 'admin', 'localhost', '5432')
        if not(product_avaliable("BC01", "1", cur)):
            print("Error, no avaliable stock for your order id")

            change_quantity_product("BC01", cur, connection)
            put_queue(cur, connection, "BC01", "1")
    else:
        text_box.configure(state="normal")
        text_box.delete("0.0", tk.END)
        text_box.insert("0.0", "Error, please select a product")
        text_box.configure(state="disabled")

# Setting window size



def change_text_box(text, bool):
    if (bool):
        text_box.configure(state="normal")
        text_box.delete("0.0", tk.END)
        text_box.insert("0.0", text)
        text_box.configure(state="disabled")
    return
def change_text_box_green_rec():
        text_box.configure(state="normal")
        text_box.delete("0.0", tk.END)
        text_box.insert("0.0", "1 - Green Rectangle")
        text_box.configure(state="disabled")
def change_text_box_green_cir():
        text_box.configure(state="normal")
        text_box.delete("0.0", tk.END)
        text_box.insert("0.0", "1 - Green Circle")
        text_box.configure(state="disabled")
def change_text_box_red_rec():
        text_box.configure(state="normal")
        text_box.delete("0.0", tk.END)
        text_box.insert("0.0", "1 - Red Rectangle")
        text_box.configure(state="disabled")
def change_text_box_red_cir():
        text_box.configure(state="normal")
        text_box.delete("0.0", tk.END)
        text_box.insert("0.0", "1 - Red Circle")
        text_box.configure(state="disabled")
def change_text_box_blue_rec():
        text_box.configure(state="normal")
        text_box.delete("0.0", tk.END)
        text_box.insert("0.0", "1 - Blue Rectangle")
        text_box.configure(state="disabled")
def change_text_box_blue_cir():
        text_box.configure(state="normal")
        text_box.delete("0.0", tk.END)
        text_box.insert("0.0", "1 - Blue Circle")
        text_box.configure(state="disabled")

button_green_rectangle = ct.CTkButton(master=root, text="Rectangle", font=("Roboto", 20),fg_color="green",  command=change_text_box_green_rec)
button_green_circle = ct.CTkButton(master=root, text="Circle", font=("Roboto", 20),fg_color="green", command=change_text_box_green_cir)
button_red_rectangle = ct.CTkButton(master=root, text="Rectangle", font=("Roboto", 20),fg_color="red", command=change_text_box_blue_rec)
button_red_circle = ct.CTkButton(master=root, text="Circle", font=("Roboto", 20),fg_color="red", command=change_text_box_blue_cir)
button_blue_rectangle = ct.CTkButton(master=root, text="Rectangle", font=("Roboto", 20),fg_color="blue", command=change_text_box_red_rec)
button_blue_circle = ct.CTkButton(master=root, text="Circle", font=("Roboto", 20),fg_color="blue", command=change_text_box_red_cir)
button_send_order = ct.CTkButton(master=root, text="Send Order", font=("Roboto", 20),fg_color="white", command=send_order, text_color="black")

text_box.grid(row=0, column=0, sticky="we", padx=(10,0), pady=(10,0))
text_box.insert("0.0","Click a button to prepare an\n order for the robots")
text_box.configure(state="disabled")

button_green_rectangle.place(relx=0.2, rely=0.2, anchor=tk.CENTER)
button_green_circle.place(relx=0.8, rely=0.2, anchor=tk.CENTER)
button_red_rectangle.place(relx=0.2, rely=0.8, anchor=tk.CENTER)
button_red_circle.place(relx=0.8, rely=0.8, anchor=tk.CENTER)
button_blue_rectangle.place(relx=0.2, rely=0.5, anchor=tk.CENTER)
button_blue_circle.place(relx=0.8, rely=0.5, anchor=tk.CENTER)
button_send_order.place(relx=0.8, rely=0.05, anchor=tk.CENTER)
finished = True
root.mainloop()

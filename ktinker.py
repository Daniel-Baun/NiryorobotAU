import tkinter as tk
import customtkinter as ct
#window = tk.Tk()
#
#label = tk.Label(text="Hello World", font=("Arial", 20))
#label.pack()
#window.mainloop()

root = ct.CTk()

# Setting window size
root.geometry("500x500")
ct.set_appearance_mode("dark")
def my_print():
    print("hello")
button_green_rectangle = ct.CTkButton(master=root, text="Click Me", font=("Roboto", 20),fg_color="green", hover_color="green", command=my_print)
button_green_circle = ct.CTkButton(master=root, text="Click Me", font=("Arial", 20),fg_color="green", hover_color="green", command=my_print)
button_red_rectangle = ct.CTkButton(master=root, text="Click Me", font=("Arial", 20),fg_color="red", hover_color="red", command=my_print)
button_red_circle = ct.CTkButton(master=root, text="Click Me", font=("Arial", 20),fg_color="red", hover_color="red", command=my_print)
button_blue_rectangle = ct.CTkButton(master=root, text="Click Me", font=("Arial", 20),fg_color="blue", hover_color="blue", command=my_print)
button_blue_circle = ct.CTkButton(master=root, text="Click Me", font=("Arial", 20),fg_color="blue", hover_color="blue", command=my_print)
button_send_order = ct.CTkButton(master=root, text="Send Order", font=("Arial", 20),fg_color="white", command=my_print, text_color="black")
text_box = ct.CTkTextbox(master=root, font=("Roboto", 20), width=200, height=50)
text_box.grid(row=0, column=0, sticky="we", padx=(10,0), pady=(10,0))
text_box.insert("0.0","Hello World")
text_box.configure(state="disabled")



button_green_rectangle.place(relx=0.2, rely=0.2, anchor=tk.CENTER)
button_green_circle.place(relx=0.8, rely=0.2, anchor=tk.CENTER)
button_red_rectangle.place(relx=0.2, rely=0.8, anchor=tk.CENTER)
button_red_circle.place(relx=0.8, rely=0.8, anchor=tk.CENTER)
button_blue_rectangle.place(relx=0.2, rely=0.5, anchor=tk.CENTER)
button_blue_circle.place(relx=0.8, rely=0.5, anchor=tk.CENTER)
button_send_order.place(relx=0.8, rely=0.05, anchor=tk.CENTER)
root.mainloop()
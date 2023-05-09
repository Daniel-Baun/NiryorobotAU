import pickle
from GUI import send_order
import time
import tkinter as tk
import customtkinter as ct
from DB_functions import *
from settings import *

class Model:
    def __init__(self) -> None:
        self.real_a = 0.0 
        self.real_b = 0.0
        self.integer_a = 0 
        self.integer_b = 0 
        self.boolean_a = False
        self.boolean_b = False
        self.string_a = "" 
        self.string_b = ""

        self.reference_to_attribute = {
            0: "real_a",
            1: "real_b",
            2: "real_c",
            3: "integer_a", # start time to make order
            4: "integer_b",
            5: "integer_c", #Time elapsed since order was made
            6: "boolean_a",
            7: "boolean_b",
            8: "boolean_c",
            9: "string_a",
            10: "string_b",
            11: "string_c",
        }
        self._update_outputs()

    def fmi2DoStep(self, current_time, step_size, no_step_prior):
        
        send_order()
        #Should be triggered when the order is sent
        self.integer_a = time.time()    

        #Should be triggered when the order is made
        self.integer_c = time.time() - self.integer_a
        
        if self.integer_c > 25.0:
            return Fmi2Status.warning
        else:
            return Fmi2Status.ok

    def fmi2EnterInitializationMode(self):
        
        root = ct.CTk()
        root.geometry("500x500")
        ct.set_appearance_mode("dark")
        text_box = ct.CTkTextbox(master=root, font=("Roboto", 20), width=300, height=70)
        button_green_rectangle = ct.CTkButton(master=root, text="Rectangle", font=("Roboto", 20),fg_color="green",  command=change_text_box_green_rec)
        button_green_circle = ct.CTkButton(master=root, text="Circle", font=("Roboto", 20),fg_color="green", command=change_text_box_green_cir)
        button_red_rectangle = ct.CTkButton(master=root, text="Rectangle", font=("Roboto", 20),fg_color="blue", command=change_text_box_blue_rec)
        button_red_circle = ct.CTkButton(master=root, text="Circle", font=("Roboto", 20),fg_color="blue", command=change_text_box_blue_cir)
        button_blue_rectangle = ct.CTkButton(master=root, text="Rectangle", font=("Roboto", 20),fg_color="red", command=change_text_box_red_rec)
        button_blue_circle = ct.CTkButton(master=root, text="Circle", font=("Roboto", 20),fg_color="red", command=change_text_box_red_cir)
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
        return Fmi2Status.ok

    def fmi2ExitInitializationMode(self):
        self._update_outputs()
        return Fmi2Status.ok

    def fmi2SetupExperiment(self, start_time, stop_time, tolerance):
        return Fmi2Status.ok

    def fmi2SetReal(self, references, values):
        return self._set_value(references, values)

    def fmi2SetInteger(self, references, values):
        return self._set_value(references, values)

    def fmi2SetBoolean(self, references, values):
        return self._set_value(references, values)

    def fmi2SetString(self, references, values):
        return self._set_value(references, values)

    def fmi2GetReal(self, references):
        return self._get_value(references)

    def fmi2GetInteger(self, references):
        return self._get_value(references)

    def fmi2GetBoolean(self, references):
        return self._get_value(references)

    def fmi2GetString(self, references):
        return self._get_value(references)

    def fmi2Reset(self):
        return Fmi2Status.ok

    def fmi2Terminate(self):
        return Fmi2Status.ok

    def fmi2ExtSerialize(self):

        bytes = pickle.dumps(
            (
                self.real_a,
                self.real_b,
                self.integer_a,
                self.integer_b,
                self.boolean_a,
                self.boolean_b,
                self.string_a,
                self.string_b,
            )
        )
        return Fmi2Status.ok, bytes

    def fmi2ExtDeserialize(self, bytes) -> int:
        (
            real_a,
            real_b,
            integer_a,
            integer_b,
            boolean_a,
            boolean_b,
            string_a,
            string_b,
        ) = pickle.loads(bytes)
        self.real_a = real_a
        self.real_b = real_b
        self.integer_a = integer_a
        self.integer_b = integer_b
        self.boolean_a = boolean_a
        self.boolean_b = boolean_b
        self.string_a = string_a
        self.string_b = string_b
        self._update_outputs()

        return Fmi2Status.ok

    def _set_value(self, references, values):

        for r, v in zip(references, values):
            setattr(self, self.reference_to_attribute[r], v)

        return Fmi2Status.ok

    def _get_value(self, references):

        values = []

        for r in references:
            values.append(getattr(self, self.reference_to_attribute[r]))

        return Fmi2Status.ok, values

    def _update_outputs(self):
        
        self.real_c = self.real_a + self.real_b
        self.integer_c = self.integer_a + self.integer_b
        self.boolean_c = self.boolean_a or self.boolean_b
        self.string_c = self.string_a + self.string_b
    


class Fmi2Status:
    """Represents the status of the FMU or the results of function calls.

    Values:
        * ok: all well
        * warning: an issue has arisen, but the computation can continue.
        * discard: an operation has resulted in invalid output, which must be discarded
        * error: an error has ocurred for this specific FMU instance.
        * fatal: an fatal error has ocurred which has corrupted ALL FMU instances.
        * pending: indicates that the FMu is doing work asynchronously, which can be retrived later.

    Notes:
        FMI section 2.1.3

    """

    ok = 0
    warning = 1
    discard = 2
    error = 3
    fatal = 4
    pending = 5


if __name__ == "__main__":
    m = Model()

    assert m.integer_a == 0
    assert m.integer_b == 0
    assert m.string_a == ""
  
    m.real_a = 1.0
    m.real_b = 2.0
    m.integer_a = 1
    m.integer_b = 2
    m.boolean_a = True
    m.boolean_b = False
    m.string_a = "Hello "
    m.string_b = "World!"

    m.fmi2EnterInitializationMode()

    var = m.fmi2DoStep(0.0, 1.0, False)

    print("status", var)

    #assert m.real_c == 3.0
    #assert m.integer_c == 3
    #assert m.boolean_c == True
    #assert m.string_c == "Hello World!"

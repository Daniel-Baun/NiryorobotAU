import pickle
import time 
import psycopg2
import configparser

class Model:
    def __init__(self) -> None:
        self.waiting_boolean = False
        self.processing_boolean = False
        self.message_string = ""
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')
    
        self.db_name = self.config.get('database', 'db_name')
        self.user = self.config.get('database', 'user')
        self.password = self.config.get('database', 'password')
        self.host = self.config.get('database', 'host')
        self.port = self.config.get('database', 'port')
        self.DB_conn = psycopg2.connect(database = self.db_name, user = self.user, password = self.password, host = self.host, port = self.port)
        self.cursor = self.DB_conn.cursor()

        self.reference_to_attribute = {
            0: "time_for_finished_order",
            1: "waiting_boolean",
            2: "processing_boolean",
            3: "message_string",
        }

        self._update_outputs()
        self._update_failure_status()

    def fmi2DoStep(self, current_time, step_size, no_step_prior):
        self._update_outputs()
        return Fmi2Status.ok

    def fmi2EnterInitializationMode(self):
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
                self.waiting_boolean,
                self.processing_boolean,
                self.message_string,
            )
        )
        return Fmi2Status.ok, bytes

    def fmi2ExtDeserialize(self, bytes) -> int:
        (
            waiting_boolean,
            processing_boolean,
            message_string,
        ) = pickle.loads(bytes)
        self.waiting_boolean = waiting_boolean
        self.processing_boolean = processing_boolean
        self.message_string = message_string
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
        
    def _update_failure_status(self):
        query = ("UPDATE public.orders "+
                 "SET failure_status = true "+ 
                 "WHERE id = (SELECT MIN(id) FROM public.orders WHERE status = 'PROCESSING' AND failure_status = false)")
        self.cursor.execute(query,)
        self.DB_conn.commit()
        return

    def __update_outputs(self):
        global start_time
        self.time_for_finished_order = 0.0
        self.message_string = ""
        if self.waiting_boolean and 'start_time' not in globals():
            start_time = time.time()
            print("I am in if statement")
        elif not self.waiting_boolean and not self.processing_boolean and 'start_time' in globals():
            print("I am in elif statement")
            end_time = time.time()
            duration = end_time - start_time
            del globals()['start_time']
            self.time_for_finished_order = duration
            if duration > 32:   
                self._update_failure_status()
                self.message_string = "Order took too long to process"
    
    def _update_outputs(self):
        self.time_for_finished_order = 0.0
        self.message_string = ""
        if self.waiting_boolean:
            if not hasattr(self, "start_time"):
                self.start_time = time.time()
        else:
            if hasattr(self, "start_time"):
                end_time = time.time()
                duration = end_time - self.start_time
                delattr(self, "start_time")
                self.time_for_finished_order = duration
                if duration > 32:   
                    self._update_failure_status()
                    self.message_string = "Order took too long to process"
    



class Fmi2Status:
    """Represents the status of the FMU or the results of function calls.

    Values:
        * ok: all wellelif group == "Fmi2FreeInstance":
            result = Fmi2FreeInstanceReturn()
            logger.info(f"Fmi2FreeInstance received, shutting down")
            sys.exit(0)
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
    assert m.time_for_finished_order == 0.0
    assert m.waiting_boolean == False
    assert m.processing_boolean == False
    
    m.waiting_boolean = True
    assert m.fmi2DoStep(0.0, 1.0, False) == Fmi2Status.ok
    m.waiting_boolean = False
    m.processing_boolean = True
    time.sleep(33)
    m.processing_boolean = False
    assert m.fmi2DoStep(0.0, 1.0, False) == Fmi2Status.ok
    assert m.time_for_finished_order != 0.0
    print(m.time_for_finished_order)

import pickle
import time 

class Model:
    def __init__(self) -> None:
        self.boolean_a = False


        self.reference_to_attribute = {
            0: "real_c",
            1: "boolean_a",
        }

        self._update_outputs()

    def fmi2DoStep(self, current_time, step_size, no_step_prior):
        self._update_outputs()
        return Fmi2Status.ok

    def fmi2EnterInitializationMode(self):

        return Fmi2Status.ok

    def fmi2ExitInitializationMode(self):
        self._update_outputs()
        return Fmi2Status.ok

    def fmi2SetupExperiment(self, start_time, stop_time, tolerance):
        start_time = 0
        stop_time = 16
        self.start_time = start_time
        self.stop_time = stop_time
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
                self.boolean_a,
            )
        )
        return Fmi2Status.ok, bytes

    def fmi2ExtDeserialize(self, bytes) -> int:
        (
            boolean_a,
        ) = pickle.loads(bytes)
        self.boolean_a = boolean_a
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
        global start_time
        self.real_c = 0.0
        if self.boolean_a and 'start_time' not in globals():
            start_time = time.time()
            print("I am in if statement")
        elif not self.boolean_a and 'start_time' in globals():
            print("I am in elif statement")
            end_time = time.time()
            duration = end_time - start_time
            del globals()['start_time']
            self.real_c = duration
            
     
        #self.real_c = self.real_a + self.real_b
        #self.integer_c = self.integer_a + self.integer_b
        #self.boolean_c = self.boolean_a or self.boolean_b
        #self.string_c = self.string_a + self.string_b


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
    assert m.real_c == 0.0
    assert m.boolean_a == False
    
    m.boolean_a = True
    assert m.fmi2DoStep(0.0, 1.0, False) == Fmi2Status.ok
    time.sleep(10)
    m.boolean_a = False
    assert m.fmi2DoStep(0.0, 1.0, False) == Fmi2Status.ok
    assert m.real_c != 0.0
    print(m.real_c)

def generate_sensor_inputs_class(di_pins):
    headerstring = '''
class SensorInputs:
    """
    Entity class for Sensor Inputs
    """
    
    def __init__(self):'''

    pins_initialisation = ""
    for pins in di_pins:
        val = "\t" +"\t"+'self.'+ pins+ " = 1"
        pins_initialisation += val + "\n"

    registration = "\t" + "def register(self, fmi3slave: Fmi3Slave):" + "\n"
    for pins in di_pins:
        reg =  "\t" +"\t"+'''fmi3slave.register_variable(
            Int32(
                "sensor_inputs.''' + pins +'''",
                causality=Fmi3Causality.input,
                description="Sensor input",
            )
        )'''
        registration += reg + "\n"

    finalstring = headerstring + "\n" + pins_initialisation + "\n" + registration + "\n"


    return finalstring
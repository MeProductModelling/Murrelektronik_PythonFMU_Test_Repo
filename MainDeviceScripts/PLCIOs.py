def generate_plcios_class():
    return '''class PLCIs:
    """
    Entity class for IOs going in and out of PLC
    """

    def __init__(self):

        self.inByte1 = 255
        self.inByte2 = 255
      
      

    def register(self, fmi3slave: Fmi3Slave):

        fmi3slave.register_variable(
            Int32(
                "plc_is.inByte1",
                causality=Fmi3Causality.input,
                description="From PLC: Integer value to set the actuators from the module",
            )
        )
        fmi3slave.register_variable(
            Int32(
                "plc_is.inByte2",
                causality=Fmi3Causality.input,
                description="From PLC: Integer value to set the actuators from the module",
            )
        )


class PLCOs:
    """
    Entity class for IOs going in and out of PLC
    """

    def __init__(self):
        self.outByte1 = 0
        self.outByte2 = 0


    def register(self, fmi3slave: Fmi3Slave):
        fmi3slave.register_variable(
            Int32(
                "plc_os.outByte1",
                causality=Fmi3Causality.output,
                description="To PLC: Sensor bits converted to Integer",
            )
        )
        fmi3slave.register_variable(
            Int32(
                "plc_os.outByte2",
                causality=Fmi3Causality.output,
                description="To PLC: Sensor bits converted to Integer",
            )
        )'''
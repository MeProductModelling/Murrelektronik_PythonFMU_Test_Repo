def User_Interfaces_IO ():
    return '''
class UserInterfaceIs:
    """
    Entity class for User Interface IOs of the Simulation Module
    """

    def __init__(self):
        self.Sensor_Voltage = 24.0
        self.Actuator_Voltage = 24.0
        self.actuator_short_circuit_trigger_value = 0
        self.sensor_short_circuit_trigger_value = 0

    def register(self, fmi3slave: Fmi3Slave):
        fmi3slave.register_variable(
            Float64("user_interface_is.Sensor_Voltage", causality=Fmi3Causality.input)
        )
        fmi3slave.register_variable(
            Float64(
                "user_interface_is.Actuator_Voltage", causality=Fmi3Causality.input
            )
        )

        fmi3slave.register_variable(
            Int32(
                "user_interface_is.actuator_short_circuit_trigger_value",
                causality=Fmi3Causality.input,
                description="Short circuit can be triggered by changing values from 255 to 0-255",
            )
        )
        fmi3slave.register_variable(
            Int32(
                "user_interface_is.sensor_short_circuit_trigger_value",
                causality=Fmi3Causality.input,
                description="Actuator circuit can be triggered by changing values from 255 to 0-255",
            )
        )

class UserInterfaceOs:
    """
    Entity class for User Interface IOs of the Simulation Module
    """

    def __init__(self):

        self.LED_Off = 0
        self.LED_Red = 0
        self.LED_Green = 0


    def register(self, fmi3slave: Fmi3Slave):

        fmi3slave.register_variable(
            Int32("user_interface_os.LED_Green", causality=Fmi3Causality.output)
        )
        fmi3slave.register_variable(
            Int32("user_interface_os.LED_Red", causality=Fmi3Causality.output)
        )
        fmi3slave.register_variable(
            Int32("user_interface_os.LED_Off", causality=Fmi3Causality.output)
        )'''
def generate_actuator_outputs_class(do_pins):
    header_String = '''class ActuatorOutputs:
    """
    Entity class for Actuator Outputs
    """
    
    def __init__(self):'''

    pins_initialisation = ""
    for pins in do_pins:
        val = "\t" + "\t" + 'self.' + pins + " = 1"
        pins_initialisation += val + "\n"

    registration = "\t" + "def register(self, fmi3slave: Fmi3Slave):" + "\n"
    for pins in do_pins:
        reg = "\t" + "\t" + '''fmi3slave.register_variable(
                Int32(
                    "actuator_outputs.''' + pins + '''",
                    causality=Fmi3Causality.output,
                    description="Actuator output",
                )
            )'''
        registration += reg + "\n"

    final_String = header_String + "\n" + pins_initialisation + "\n" + registration + "\n"

    '''class ActuatorOutputs:
    """
    Entity class for actuator Outputs
    """

    def __init__(self):
        # Variables for actuator outputs...
        self.X0_2 = 1
        self.X0_4 = 1
        self.X1_2 = 1
        self.X1_4 = 1
        self.X2_2 = 1
        self.X2_4 = 1
        self.X3_2 = 1
        self.X3_4 = 1

    def register(self, fmi3slave: Fmi3Slave):
        fmi3slave.register_variable(
            Int32(
                "actuator_outputs.X0_2",
                causality=Fmi3Causality.output,
                description="Actuator output",
            )
        )
        fmi3slave.register_variable(
            Int32(
                "actuator_outputs.X0_4",
                causality=Fmi3Causality.output,
                description="Actuator output",
            )
        )
        fmi3slave.register_variable(
            Int32(
                "actuator_outputs.X1_2",
                causality=Fmi3Causality.output,
                description="Actuator output",
            )
        )
        fmi3slave.register_variable(
            Int32(
                "actuator_outputs.X1_4",
                causality=Fmi3Causality.output,
                description="Actuator output",
            )
        )
        fmi3slave.register_variable(
            Int32(
                "actuator_outputs.X2_2",
                causality=Fmi3Causality.output,
                description="Actuator output",
            )
        )
        fmi3slave.register_variable(
            Int32(
                "actuator_outputs.X2_4",
                causality=Fmi3Causality.output,
                description="Actuator output",
            )
        )
        fmi3slave.register_variable(
            Int32(
                "actuator_outputs.X3_2",
                causality=Fmi3Causality.output,
                description="Actuator output",
            )
        )
        fmi3slave.register_variable(
            Int32(
                "actuator_outputs.X3_4",
                causality=Fmi3Causality.output,
                description="Actuator output",
            )
        )
'''
    return final_String
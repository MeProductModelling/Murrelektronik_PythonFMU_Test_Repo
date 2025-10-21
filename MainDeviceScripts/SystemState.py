def generate_systemstate_class():
    return '''class SystemStates:
    """
    Entity class for IOs going in and out of PLC
    """

    def __init__(self):
        
        self.system_state_byte_1 = 0
        self.system_state_byte_2 = 0
        self.system_state_byte_3 = 0
        self.system_state_byte_4 = 0

    def register(self, fmi3slave: Fmi3Slave):
        fmi3slave.register_variable(
            Int32(
                "system_state.system_state_byte_1",
                causality=Fmi3Causality.output,
                description="To PLC: shows state of the module",
            )
        )
        fmi3slave.register_variable(
            Int32(
                "system_state.system_state_byte_2",
                causality=Fmi3Causality.output,
                description="To PLC: shows state of the module",
            )
        )
        fmi3slave.register_variable(
            Int32(
                "system_state.system_state_byte_3",
                causality=Fmi3Causality.output,
                description="To PLC: shows state of the module",
            )
        )
        fmi3slave.register_variable(
            Int32(
                "system_state.system_state_byte_4",
                causality=Fmi3Causality.output,
                description="To PLC: shows state of the module",
            )
        )
'''
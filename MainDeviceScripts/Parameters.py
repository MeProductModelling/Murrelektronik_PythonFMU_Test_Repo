def generate_parameters_class():
    return '''class Parameters:
    """
    Entity class for Parameters of the Simulation Module
    """

    def __init__(self):
        self.PinBased = True
        self.PortBased = False
        self.Compact = False

    def register(self, fmi3slave: Fmi3Slave):
        fmi3slave.register_variable(
            Boolean(
                "parameters.PinBased",
                causality=Fmi3Causality.parameter,
                variability=Fmi3Variability.tunable,
                description="Pin based mapping of inputs",
            )
        )
        fmi3slave.register_variable(
            Boolean(
                "parameters.PortBased",
                causality=Fmi3Causality.parameter,
                variability=Fmi3Variability.tunable,
                description="Port based mapping of inputs",
            )
        )
        fmi3slave.register_variable(
            Boolean(
                "parameters.Compact",
                causality=Fmi3Causality.parameter,
                variability=Fmi3Variability.tunable,
                description="Compact based mapping of inputs",
            )
        )
'''
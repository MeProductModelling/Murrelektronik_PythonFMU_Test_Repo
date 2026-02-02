def generate_qualifier_dis_class():
    return '''class QualifierDIs:
    """
    Entity class for IOs going in and out of PLC
    """

    def __init__(self):
        
        self.qualifier_di_8_byte1 = 0
        self.qualifier_di_8_byte2 = 0
        
        
    def register(self, fmi3slave: Fmi3Slave):
  
        fmi3slave.register_variable(
            Int32(
                "qualifier_dis.qualifier_di_8_byte1",
                causality=Fmi3Causality.output,
                description="To PLC: shows location of error in the module in inputs",
            )
        )
        fmi3slave.register_variable(
            Int32(
                "qualifier_dis.qualifier_di_8_byte2",
                causality=Fmi3Causality.output,
                description="To PLC: shows location of error in the module in inputs",
            )
        )
'''

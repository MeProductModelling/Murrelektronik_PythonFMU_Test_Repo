import numpy as np
from pythonfmu3 import (
    Fmi3Causality,
    Fmi3Slave,
    Float64,
    Int32,
    Boolean,
    Fmi3Variability,
    Enumeration,
)

from Modules.QualifierDI8 import qualifier_di_8
from Modules.QualifierDO8 import qualifier_do_8
from Modules.MVKLEDConfig import led
from Modules.DI8 import digital_inputs
from Modules.DO8 import digital_outputs
from Modules.Shortcircuittrigger import short_circuit_trigger
from Modules.SystemState import System_State




class MVK55531(Fmi3Slave):
    """
    Main class for MVK device 55531
    """

    def __init__(self, **kwargs):
        """
        Constructor
        :param kwargs: All keyword arguments are passed to the base class.
        """
        super().__init__(**kwargs)

        self.parameters = Parameters()
        self.parameters.register(self)

        self.plc_ios = PLCIOs()
        self.plc_ios.register(self)

        self.sensor_inputs = SensorInputs()
        self.sensor_inputs.register(self)

        self.actuator_outputs = ActuatorOutputs()
        self.actuator_outputs.register(self)

        self.user_interface_ios = UserInterfaceIOs()
        self.user_interface_ios.register(self)

        self.author = "Raj Kumar"
        self.description = "A simple description of DIO 8 module from Murrelektronik catalogue"
        self.time = 0.0
        self.register_variable(Float64("time", causality=Fmi3Causality.independent))
        
        
  def do_step(self, current_time, step_size):
        
  #TODO: Commission initialised variables to make work together
        
  return True

class Parameters:
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


class SensorInputs:
    """
    Entity class for Sensor Inputs
    """

    def __init__(self):
        self.X4_2 = 1
        self.X4_4 = 1
        self.X5_2 = 1
        self.X5_4 = 1
        self.X6_2 = 1
        self.X6_4 = 1
        self.X7_2 = 1
        self.X7_4 = 1

    def register(self, fmi3slave: Fmi3Slave):
        fmi3slave.register_variable(
            Int32(
                "sensor_inputs.X4_2",
                causality=Fmi3Causality.input,
                description="Sensor input",
            )
        )
        fmi3slave.register_variable(
            Int32(
                "sensor_inputs.X4_4",
                causality=Fmi3Causality.input,
                description="Sensor input",
            )
        )
        fmi3slave.register_variable(
            Int32(
                "sensor_inputs.X5_2",
                causality=Fmi3Causality.input,
                description="Sensor input",
            )
        )
        fmi3slave.register_variable(
            Int32(
                "sensor_inputs.X5_4",
                causality=Fmi3Causality.input,
                description="Sensor input",
            )
        )
        fmi3slave.register_variable(
            Int32(
                "sensor_inputs.X6_2",
                causality=Fmi3Causality.input,
                description="Sensor input",
            )
        )
        fmi3slave.register_variable(
            Int32(
                "sensor_inputs.X6_4",
                causality=Fmi3Causality.input,
                description="Sensor input",
            )
        )
        fmi3slave.register_variable(
            Int32(
                "sensor_inputs.X7_2",
                causality=Fmi3Causality.input,
                description="Sensor input",
            )
        )
        fmi3slave.register_variable(
            Int32(
                "sensor_inputs.X7_4",
                causality=Fmi3Causality.input,
                description="Sensor input",
            )
        )

class ActuatorOutputs:
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

class QualifierDIs:
    """
    Entity class for IOs going in and out of PLC
    """

    def __init__(self):
        
        self.qualifier_di_8_byte1 = 0
        self.qualifier_di_8_byte2 = 0
        
        
    def register(self, fmi3slave: Fmi3Slave):
  
        fmi3slave.register_variable(
            Int32(
                "plc_ios.qualifier_di_8_byte1",
                causality=Fmi3Causality.output,
                description="To PLC: shows location of error in the module in inputs",
            )
        )
        fmi3slave.register_variable(
            Int32(
                "plc_ios.qualifier_di_8_byte2",
                causality=Fmi3Causality.output,
                description="To PLC: shows location of error in the module in inputs",
            )
        )

 class QualiferDOs:
    """
    Entity class for IOs going in and out of PLC
    """

    def __init__(self):
        
        self.qualifier_do_8_byte1 = 0
        self.qualifier_do_8_byte2 = 0
        

    def register(self, fmi3slave: Fmi3Slave):
        fmi3slave.register_variable(
            Int32(
                "plc_ios.qualifier_do_8_byte1",
                causality=Fmi3Causality.output,
                description="To PLC: shows location of error in the module in outputs",
            )
        )
        fmi3slave.register_variable(
            Int32(
                "plc_ios.qualifier_do_8_byte2",
                causality=Fmi3Causality.output,
                description="To PLC: shows location of error in the module in outputs",
            )
        )
       
class SystemStates:
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
                "plc_ios.system_state_byte_1",
                causality=Fmi3Causality.output,
                description="To PLC: shows state of the module",
            )
        )
        fmi3slave.register_variable(
            Int32(
                "plc_ios.system_state_byte_2",
                causality=Fmi3Causality.output,
                description="To PLC: shows state of the module",
            )
        )
        fmi3slave.register_variable(
            Int32(
                "plc_ios.system_state_byte_3",
                causality=Fmi3Causality.output,
                description="To PLC: shows state of the module",
            )
        )
        fmi3slave.register_variable(
            Int32(
                "plc_ios.system_state_byte_4",
                causality=Fmi3Causality.output,
                description="To PLC: shows state of the module",
            )
        )


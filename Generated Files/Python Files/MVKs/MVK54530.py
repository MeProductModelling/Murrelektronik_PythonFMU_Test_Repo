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
from Modules.DI16 import digital_inputs_16
from Modules.DO16 import digital_outputs_16
from Modules.Shortcircuittrigger import short_circuit_trigger
from Modules.SystemState import System_State




class MVK54530(Fmi3Slave):
    """
    Main class for MVK device 54530
    """

    def __init__(self, **kwargs):
        """
        Constructor
        :param kwargs: All keyword arguments are passed to the base class.
        """
        super().__init__(**kwargs)

        self.parameters = Parameters()
        self.parameters.register(self)

        self.sensor_inputs = SensorInputs()
        self.sensor_inputs.register(self)

        self.qualifier_dis = QualifierDIs()
        self.qualifier_dis.register(self)

        self.system_state = SystemStates()
        self.system_state.register(self)

        self.plc_ios = PLCIOs()
        self.plc_ios.register(self)

        self.user_interface_ios = UserInterfaceIOs()
        self.user_interface_ios.register(self)

        self.author = "Raj Kumar"
        self.description = "A simple description of DIO 8 module from Murrelektronik catalogue"
        self.time = 0.0
        self.register_variable(Float64("time", causality=Fmi3Causality.independent))
        
        


    def do_step(self, current_time, step_size):
        """
        This is the function that is called at every simulation step.
        """
    

        def _get_out_bytes():
            # This following section is to convert bits to bytes...i.e sensor values to a bit.
            # DI 8. These Inputs are from Sensor which are usually connected in simulation tool.
            self.plc_ios.outByte1, self.plc_ios.outByte2 = digital_inputs(
                np.array(
                    [
                    
                    self.sensor_inputs.X4_2,
                    self.sensor_inputs.X4_4,
                    self.sensor_inputs.X5_2,
                    self.sensor_inputs.X5_4,
                    self.sensor_inputs.X6_2,
                    self.sensor_inputs.X6_4,
                    self.sensor_inputs.X7_2,
                    self.sensor_inputs.X7_4

                ]
            ),
            self.parameters.PinBased,
            self.parameters.PortBased,
            self.parameters.Compact,
        )
        

        def _get_out_bits():
            # The following section is to convert byte to bits....triggering the actuator values.
            # DO 8. These Outputs are connected to actuators in simulation tool.
            (
            self.actuator_outputs.X4_2,
            self.actuator_outputs.X4_4,
            self.actuator_outputs.X5_2,
            self.actuator_outputs.X5_4,
            self.actuator_outputs.X6_2,
            self.actuator_outputs.X6_4,
            self.actuator_outputs.X7_2,
            self.actuator_outputs.X7_4

            ) = digital_outputs(
                self.plc_ios.inByte1,
                self.plc_ios.inByte2,
                self.parameters.PinBased,
                self.parameters.PortBased,
                self.parameters.Compact,
            )
            

        def _get_qualifier_di_bytes():
            # Qualifier DI. These outputs from block are connected to PLC
            (self.qualifier_dis.qualifier_di_8_byte1, self.qualifier_dis.qualifier_di_8_byte2) = (
                qualifier_di_8(
                    short_circuit_sensor_trigger_as_bits,
                    self.parameters.PinBased,
                    self.parameters.PortBased,
                    self.parameters.Compact,
                )
            )


        def _get_system_state_bytes():
            # System State. These outputs from block are connected to PLC
            (
                self.system_state.system_state_byte_1,
                self.system_state.system_state_byte_2,
                self.system_state.system_state_byte_3,
                self.system_state.system_state_byte_4,
            ) = System_State(
                self.qualifier_dis.qualifier_di_8_byte1,
                self.qualifier_dis.qualifier_di_8_byte2,
                0,
                0,
                False,
                False,
                self.user_interface_ios.Sensor_Voltage,
                self.user_interface_ios.Actuator_Voltage,
            )


        _get_out_bytes()
        _get_out_bits()


        # LED Config behaviour
        (
            self.user_interface_ios.LED_Green,
            self.user_interface_ios.LED_Red,
            self.user_interface_ios.LED_Off,
        ) = led(self.user_interface_ios.Sensor_Voltage, current_time)

        # Short circuit bits for sensor and actuator
        short_circuit_result = short_circuit_trigger(
            self.user_interface_ios.sensor_short_circuit_trigger_value,
            self.user_interface_ios.actuator_short_circuit_trigger_value,
        )
        [
            short_circuit_actuator_trigger_as_bits,
            short_circuit_sensor_trigger_as_bits,
        ] = short_circuit_result

        _get_qualifier_di_bytes()

        _get_system_state_bytes()

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

class PLCIOs:
    """
    Entity class for IOs going in and out of PLC
    """

    def __init__(self):
        self.outByte1 = 0
        self.outByte2 = 0
        self.inByte1 = 255
        self.inByte2 = 255
      
      

    def register(self, fmi3slave: Fmi3Slave):
        fmi3slave.register_variable(
            Int32(
                "plc_ios.outByte1",
                causality=Fmi3Causality.output,
                description="To PLC: Sensor bits converted to Integer",
            )
        )
        fmi3slave.register_variable(
            Int32(
                "plc_ios.outByte2",
                causality=Fmi3Causality.output,
                description="To PLC: Sensor bits converted to Integer",
            )
        )
        fmi3slave.register_variable(
            Int32(
                "plc_ios.inByte1",
                causality=Fmi3Causality.input,
                description="From PLC: Integer value to set the actuators from the module",
            )
        )
        fmi3slave.register_variable(
            Int32(
                "plc_ios.inByte2",
                causality=Fmi3Causality.input,
                description="From PLC: Integer value to set the actuators from the module",
            )
        )

class UserInterfaceIOs:
    """
    Entity class for User Interface IOs of the Simulation Module
    """

    def __init__(self):
        self.Sensor_Voltage = 24.0
        self.Actuator_Voltage = 24.0
        self.LED_Off = 0.0
        self.LED_Red = 0.0
        self.LED_Green = 0.0
        self.actuator_short_circuit_trigger_value = 0
        self.sensor_short_circuit_trigger_value = 0

    def register(self, fmi3slave: Fmi3Slave):
        fmi3slave.register_variable(
            Float64("user_interface_ios.Sensor_Voltage", causality=Fmi3Causality.input)
        )
        fmi3slave.register_variable(
            Float64(
                "user_interface_ios.Actuator_Voltage", causality=Fmi3Causality.input
            )
        )
        fmi3slave.register_variable(
            Float64("user_interface_ios.LED_Green", causality=Fmi3Causality.output)
        )
        fmi3slave.register_variable(
            Float64("user_interface_ios.LED_Red", causality=Fmi3Causality.output)
        )
        fmi3slave.register_variable(
            Float64("user_interface_ios.LED_Off", causality=Fmi3Causality.output)
        )
        fmi3slave.register_variable(
            Int32(
                "user_interface_ios.actuator_short_circuit_trigger_value",
                causality=Fmi3Causality.input,
                description="Short circuit can be triggered by changing values from 255 to 0-255",
            )
        )
        fmi3slave.register_variable(
            Int32(
                "user_interface_ios.sensor_short_circuit_trigger_value",
                causality=Fmi3Causality.input,
                description="Actuator circuit can be triggered by changing values from 255 to 0-255",
            )
        )

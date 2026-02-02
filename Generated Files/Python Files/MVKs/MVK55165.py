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




class MVK55165(Fmi3Slave):
    """
    Main class for MVK device 55165
    """

    def __init__(self, **kwargs):
        """
        Constructor
        :param kwargs: All keyword arguments are passed to the base class.
        """
        super().__init__(**kwargs)

        self.PinBased = True
        self.PortBased = False
        self.Compact = False

        self.OUT_X4_2 = 1
        self.OUT_X4_4 = 1
        self.OUT_X5_2 = 1
        self.OUT_X5_4 = 1
        self.OUT_X6_2 = 1
        self.OUT_X6_4 = 1
        self.OUT_X7_2 = 1
        self.OUT_X7_4 = 1


        self.qualifier_do_8_byte1 = 0
        self.qualifier_do_8_byte2 = 0

        self.inByte1 = 255
        self.inByte2 = 255

        self.system_state_byte_1 = 0
        self.system_state_byte_2 = 0
        self.system_state_byte_3 = 0
        self.system_state_byte_4 = 0

        self.Sensor_Voltage = 24.0
        self.Actuator_Voltage = 24.0
        self.actuator_short_circuit_trigger_value = 0
        self.sensor_short_circuit_trigger_value = 0

        self.LED_Off = 0
        self.LED_Red = 0
        self.LED_Green = 0

        self.register_variable(Boolean('PinBased',causality=Fmi3Causality.parameter,variability=Fmi3Variability.tunable,description='Pin based mapping of inputs',))
        self.register_variable(Boolean('PortBased',causality=Fmi3Causality.parameter,variability=Fmi3Variability.tunable,description='Port based mapping of inputs',))
        self.register_variable(Boolean('Compact',causality=Fmi3Causality.parameter,variability=Fmi3Variability.tunable,description='Compact based mapping of inputs',))

        self.register_variable(Int32('OUT_X4_2',causality=Fmi3Causality.output,description='Actuator Output',))
        self.register_variable(Int32('OUT_X4_4',causality=Fmi3Causality.output,description='Actuator Output',))
        self.register_variable(Int32('OUT_X5_2',causality=Fmi3Causality.output,description='Actuator Output',))
        self.register_variable(Int32('OUT_X5_4',causality=Fmi3Causality.output,description='Actuator Output',))
        self.register_variable(Int32('OUT_X6_2',causality=Fmi3Causality.output,description='Actuator Output',))
        self.register_variable(Int32('OUT_X6_4',causality=Fmi3Causality.output,description='Actuator Output',))
        self.register_variable(Int32('OUT_X7_2',causality=Fmi3Causality.output,description='Actuator Output',))
        self.register_variable(Int32('OUT_X7_4',causality=Fmi3Causality.output,description='Actuator Output',))


        self.register_variable(Int32('qualifier_do_8_byte1',causality=Fmi3Causality.output,description='To PLC: shows location of error in the module in outputs',))
        self.register_variable(Int32('qualifier_do_8_byte2',causality=Fmi3Causality.output,description='To PLC: shows location of error in the module in outputs',))

        self.register_variable(Int32('inByte1',causality=Fmi3Causality.input,description='From PLC: Integer value to set the actuators from the module',))
        self.register_variable(Int32('inByte2',causality=Fmi3Causality.input,description='From PLC: Integer value to set the actuators from the module',))

        self.register_variable(Int32('system_state_byte_1',causality=Fmi3Causality.output,description='To PLC: shows state of the module',))
        self.register_variable(Int32('system_state_byte_2',causality=Fmi3Causality.output,description='To PLC: shows state of the module',))
        self.register_variable(Int32('system_state_byte_3',causality=Fmi3Causality.output,description='To PLC: shows state of the module',))
        self.register_variable(Int32('system_state_byte_4',causality=Fmi3Causality.output,description='To PLC: shows state of the module',))

        self.register_variable(Float64('Sensor_Voltage',causality=Fmi3Causality.input,description='User Interface control of sensor voltage',))
        self.register_variable(Float64('Actuator_Voltage',causality=Fmi3Causality.input,description='User Interface control of sensor voltage',))
        self.register_variable(Int32('actuator_short_circuit_trigger_value',causality=Fmi3Causality.input,description='Sensor Short circuit can be triggered by changing values from 255 to 0-255',))
        self.register_variable(Int32('sensor_short_circuit_trigger_value',causality=Fmi3Causality.input,description='Actuator Short circuit can be triggered by changing values from 255 to 0-255',))

        self.register_variable(Int32('LED_Green',causality=Fmi3Causality.output,description='LED behaviour of the device',))
        self.register_variable(Int32('LED_Red',causality=Fmi3Causality.output,description='LED behaviour of the device',))
        self.register_variable(Int32('LED_Off',causality=Fmi3Causality.output,description='LED behaviour of the device',))

        self.author = "Raj Kumar"
        self.description = "A simple description of DIO 8 module from Murrelektronik catalogue"
        self.time = 0.0
        self.register_variable(Float64("time", causality=Fmi3Causality.independent))
        
        


    def do_step(self, current_time, step_size):
        """
        This is the function that is called at every simulation step.
        """
    


        def _get_out_bits():
            # The following section is to convert byte to bits....triggering the actuator values.
            # DO 8. These Outputs are connected to actuators in simulation tool.
            (
			self.OUT_X4_2,
			self.OUT_X4_4,
			self.OUT_X5_2,
			self.OUT_X5_4,
			self.OUT_X6_2,
			self.OUT_X6_4,
			self.OUT_X7_2,
			self.OUT_X7_4

                  ) = digital_outputs(
                      self.inByte1,
                      self.inByte2,
                      self.PinBased,
                      self.PortBased,
                      self.Compact,
                  )
                  


        def _get_qualifier_do_bytes():
            # Qualifier DO.  These outputs from block are connected to PLC
            (self.qualifier_do_8_byte1, self.qualifier_do_8_byte2) = (
                qualifier_do_8(
                    self.inByte1,
                    self.inByte2,
                    short_circuit_actuator_trigger_as_bits,
                    self.PinBased,
                    self.PortBased,
                    self.Compact,
                )
            )

        def _get_system_state_bytes():
            # System State. These outputs from block are connected to PLC
            (
                self.system_state_byte_1,
                self.system_state_byte_2,
                self.system_state_byte_3,
                self.system_state_byte_4,
            ) = System_State(
                0,
                0,
                self.qualifier_do_8_byte1,
                self.qualifier_do_8_byte2,
                False,
                False,
                self.Sensor_Voltage,
                self.Actuator_Voltage,
            )


 
        _get_out_bits()


        # LED Config behaviour
        (
            self.LED_Green,
            self.LED_Red,
            self.LED_Off,
        ) = led(self.Sensor_Voltage, current_time)

        # Short circuit bits for sensor and actuator
        short_circuit_result = short_circuit_trigger(
            self.sensor_short_circuit_trigger_value,
            self.actuator_short_circuit_trigger_value,
        )
        [
            short_circuit_actuator_trigger_as_bits,
            short_circuit_sensor_trigger_as_bits,
        ] = short_circuit_result

        _get_qualifier_do_bytes()

        _get_system_state_bytes()

        return True


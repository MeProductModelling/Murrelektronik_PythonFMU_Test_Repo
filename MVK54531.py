import numpy as np
from pythonfmu3 import Fmi3Causality, Fmi3Slave, Float64, Int32, Boolean, Fmi3Variability, Enumeration

from Modules.QualifierDI8 import qualifier_di_8
from Modules.QualifierDO8 import qualifier_do_8
from Modules.MVKLEDConfig import led
from Modules.DI8 import digital_inputs
from Modules.DO8 import digital_outputs
from Modules.Shortcircuittrigger import short_circuit_trigger
from Modules.SystemState import System_State

class MVK54531(Fmi3Slave):

    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)

        #Parameters Pin, port, ComplexBased IOs
        self.PinBased = True
        self.PortBased = False
        self.ComplexBased = False
        #self.IOLayout = {self.PinBased, self.PortBased, self.ComplexBased}


        self.LED_Off = 0.0
        self.LED_Red = 0.0
        self.LED_Green = 0.0
        self.Sensor_Voltage = 24.0
        self.Actuator_Voltage = 24.0
        self.author = "Raj Kumar"
        self.description = "A simple description of DIO 8 module from Murrelektronik catalogue"

        self.time = 0.0


        self.outByte1 = 10
        self.outByte2 = 10
        self.inByte1 = 10
        self.inByte2 = 10
        self.qualifier_di_8_byte1 = 0
        self.qualifier_di_8_byte2 = 0
        self.qualifier_do_8_byte1 = 0
        self.qualifier_do_8_byte2 = 0
        self.system_state_byte_1 = 0
        self.system_state_byte_2 = 0
        self.system_state_byte_3 = 0
        self.system_state_byte_4 = 0
        self.actuator_short_circuit_trigger_value = 255
        self.sensor_short_circuit_trigger_value = 255

        #Variables for sensor inputs...
        self.X0_2 = 1
        self.X0_4 = 1
        self.X1_2 = 1
        self.X1_4 = 1
        self.X2_2 = 1
        self.X2_4 = 1
        self.X3_2 = 1
        self.X3_4 = 1

        #Variables for actuator variables..
        self.X4_2 = 1
        self.X4_4 = 1
        self.X5_2 = 1
        self.X5_4 = 1
        self.X6_2 = 1
        self.X6_4 = 1
        self.X7_2 = 1
        self.X7_4 = 1

        self.register_variable(Float64("time", causality=Fmi3Causality.independent))
        self.register_variable(Float64("Sensor_Voltage", causality=Fmi3Causality.input))
        self.register_variable(Float64("Actuator_Voltage", causality=Fmi3Causality.input))

        #Parameter Declarations
        self.register_variable(Boolean("PinBased", causality=Fmi3Causality.parameter,variability=Fmi3Variability.tunable, description= "Pin based mapping of inputs"))
        self.register_variable(Boolean("PortBased", causality=Fmi3Causality.parameter,variability=Fmi3Variability.tunable, description= "Port based mapping of inputs"))
        self.register_variable(Boolean("ComplexBased", causality=Fmi3Causality.parameter,variability=Fmi3Variability.tunable, description= "Complex based mapping of inputs"))


        self.register_variable(Int32("X0_2", causality=Fmi3Causality.output, description= "Actuator output"))
        self.register_variable(Int32("X0_4", causality=Fmi3Causality.output, description= "Actuator output"))
        self.register_variable(Int32("X1_2", causality=Fmi3Causality.output, description= "Actuator output"))
        self.register_variable(Int32("X1_4", causality=Fmi3Causality.output, description= "Actuator output"))
        self.register_variable(Int32("X2_2", causality=Fmi3Causality.output, description= "Actuator output"))
        self.register_variable(Int32("X2_4", causality=Fmi3Causality.output, description= "Actuator output"))
        self.register_variable(Int32("X3_2", causality=Fmi3Causality.output, description= "Actuator output"))
        self.register_variable(Int32("X3_4", causality=Fmi3Causality.output, description= "Actuator output"))
        

        self.register_variable(Float64("LED_Green", causality=Fmi3Causality.output))
        self.register_variable(Float64("LED_Red", causality=Fmi3Causality.output))
        self.register_variable(Float64("LED_Off", causality=Fmi3Causality.output))
        self.register_variable(Int32("outByte1", causality=Fmi3Causality.output, description="To PLC: Sensor bits converted to Integer"))
        self.register_variable(Int32("outByte2", causality=Fmi3Causality.output, description="To PLC: Sensor bits converted to Integer"))
        self.register_variable(Int32("qualifier_di_8_byte1", causality=Fmi3Causality.output, description= "To PLC: shows location of error in the module in inputs"))
        self.register_variable(Int32("qualifier_di_8_byte2", causality=Fmi3Causality.output, description= "To PLC: shows location of error in the module in inputs"))
        self.register_variable(Int32("qualifier_do_8_byte1", causality=Fmi3Causality.output, description= "To PLC: shows location of error in the module in outputs"))
        self.register_variable(Int32("qualifier_do_8_byte2", causality=Fmi3Causality.output, description= "To PLC: shows location of error in the module in outputs"))
        self.register_variable(Int32("system_state_byte_1", causality=Fmi3Causality.output, description= "To PLC: shows state of the module"))
        self.register_variable(Int32("system_state_byte_2", causality=Fmi3Causality.output, description= "To PLC: shows state of the module"))
        self.register_variable(Int32("system_state_byte_3", causality=Fmi3Causality.output, description= "To PLC: shows state of the module"))
        self.register_variable(Int32("system_state_byte_4", causality=Fmi3Causality.output, description= "To PLC: shows state of the module"))

        self.register_variable(Int32("X4_2", causality=Fmi3Causality.input, description= "Sensor input"))
        self.register_variable(Int32("X4_4", causality=Fmi3Causality.input, description= "Sensor input"))
        self.register_variable(Int32("X5_2", causality=Fmi3Causality.input, description= "Sensor input"))
        self.register_variable(Int32("X5_4", causality=Fmi3Causality.input, description= "Sensor input"))
        self.register_variable(Int32("X6_2", causality=Fmi3Causality.input, description= "Sensor input"))
        self.register_variable(Int32("X6_4", causality=Fmi3Causality.input, description= "Sensor input"))
        self.register_variable(Int32("X7_2", causality=Fmi3Causality.input, description= "Sensor input"))
        self.register_variable(Int32("X7_4", causality=Fmi3Causality.input, description= "Sensor input"))
        self.register_variable(Int32("inByte1", causality=Fmi3Causality.input, description="From PLC: Integer value to set the actuators from the module"))
        self.register_variable(Int32("inByte2", causality=Fmi3Causality.input, description="From PLC: Integer value to set the actuators from the module"))
        self.register_variable(Int32("actuator_short_circuit_trigger_value", causality=Fmi3Causality.input, description="Short circuit can be triggered by changing values from 255 to 0-255"))
        self.register_variable(Int32("sensor_short_circuit_trigger_value", causality=Fmi3Causality.input, description="Actuator circuit can be triggered by changing values from 255 to 0-255" ))


    def do_step(self, current_time, step_size):

        #This following section is to convert bits to bytes...i.e sensor values to a bit.
        #DI 8. These Inputs are from Sensor which are usually connected in simulation tool.
        self.outByte1,self.outByte2 = digital_inputs(np.array([self.X4_2, self.X4_4, self.X5_2, self.X5_4, self.X6_2, self.X6_4, self.X7_2, self.X7_4]), self.PinBased, self.PortBased, self.ComplexBased)


        #The following section is to convert byte to bits....triggering the actuator values.
        #DO 8. These Outputs are connected to actuators in simulation tool.
        self.X0_2, self.X0_4, self.X1_2, self.X1_4, self.X2_2, self.X2_4, self.X3_2, self.X3_4 = digital_outputs(self.inByte1, self.inByte2, self.PinBased, self.PortBased, self.ComplexBased)


        #LED Config behaviour
        self.LED_Green,self.LED_Red,self.LED_Off = led(self.Sensor_Voltage, current_time)

        #Short circuit bits for sensor and actuator
        [short_circuit_actuator_trigger_as_bits, short_circuit_sensor_trigger_as_bits] = short_circuit_trigger(self.sensor_short_circuit_trigger_value, self.actuator_short_circuit_trigger_value)

        #Qualifier DI. These outputs from block are connected to PLC
        self.qualifier_di_8_byte1,self.qualifier_di_8_byte2 = qualifier_di_8(short_circuit_sensor_trigger_as_bits, self.PinBased, self.PortBased, self.ComplexBased)

        #Qualifier DO.  These outputs from block are connected to PLC
        self.qualifier_do_8_byte1, self.qualifier_do_8_byte2 = qualifier_do_8(self.inByte1, self.inByte2, short_circuit_actuator_trigger_as_bits, self.PinBased, self.PortBased, self.ComplexBased)

        #LED behaviour. These outputs are connected to UI which are created for blocs in respective simulation tools.


        #System State. These outputs from block are connected to PLC
        self.system_state_byte_1, self.system_state_byte_2, self.system_state_byte_3, self.system_state_byte_4 = System_State(self.qualifier_di_8_byte1, self.qualifier_di_8_byte2, self.qualifier_do_8_byte1, self.qualifier_do_8_byte2, "false", "false", self.Sensor_Voltage, self.Actuator_Voltage)

        return True


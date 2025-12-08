import json

# Mapping from submodule "Name" to (class name, instance name)
SUBMODULE_NAME_MAP = {
    "Parameters/Diagnosis": ("Parameters", "parameters"),
    "Digital IO": ("SensorInputs", "sensor_inputs", "ActuatorOutputs", "actuator_outputs"),
    "Digital Input": ("SensorInputs", "sensor_inputs"),
    "Digital Output": ("ActuatorOutputs", "actuator_outputs"),
    "Qualifier Digital Input": ("QualifierDIs", "qualifier_dis"),
    "Qualifier Digital Output": ("QualifierDOs", "qualifier_dos"),
    "System state": ("SystemStates", "system_state")
}

HEADER_IMPORTS = '''import numpy as np
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
'''
def generate_constructor_1(json_data, di_pins, do_pins):
    VALID_MASTER_KEYS = {
        "DIO_MASTER",
        "DIO_MASTER_IOL2",
        "DIO_MASTER_IOL4",
        "DIO_MASTER_IOL2_EXT1",
        "DI_MASTER",
        "DO_MASTER",
        "DIDO_MASTER",
    }

    device_id = json_data["ModuleInfo"]["OrderNumber"]["@attributes"]["Value"]
    class_name = f"MVK{device_id}"

    lines = []
    lines.append(HEADER_IMPORTS)
    lines.append("\n\n")
    lines.append(f"class {class_name}(Fmi3Slave):")
    lines.append('    """')
    lines.append(f"    Main class for MVK device {device_id}")
    lines.append('    """\n')
    lines.append("    def __init__(self, **kwargs):")
    lines.append('        """')
    lines.append("        Constructor")
    lines.append("        :param kwargs: All keyword arguments are passed to the base class.")
    lines.append('        """')
    lines.append("        super().__init__(**kwargs)\n")

    # Add submodule-based declarations
    #submodules = json_data["ResolvedModuleItems"]["DIDO_MASTER"]["SubmoduleItems"]
    submodules = json_data.get("ResolvedModuleItems", {})

    lines.append(f"        self.PinBased = True")
    lines.append(f"        self.PortBased = False")
    lines.append(f"        self.Compact = False\n")

    if len(di_pins) != 0:
        for dis in di_pins:
            lines.append(f"        self.IN_{dis} = 1")

        lines.append(f"\n")
        lines.append(f"        self.qualifier_di_8_byte1 = 0")
        lines.append(f"        self.qualifier_di_8_byte2 = 0\n")

        lines.append(f"        self.outByte1 = 0")
        lines.append(f"        self.outByte2 = 0\n")



    if len(do_pins) != 0:
        for dos in do_pins:
            lines.append(f"        self.OUT_{dos} = 1")

        lines.append(f"\n")
        lines.append(f"        self.qualifier_do_8_byte1 = 0")
        lines.append(f"        self.qualifier_do_8_byte2 = 0\n")

        lines.append(f"        self.inByte1 = 255")
        lines.append(f"        self.inByte2 = 255\n")



    lines.append(f"        self.system_state_byte_1 = 0")
    lines.append(f"        self.system_state_byte_2 = 0")
    lines.append(f"        self.system_state_byte_3 = 0")
    lines.append(f"        self.system_state_byte_4 = 0\n")

    lines.append(f"        self.Sensor_Voltage = 24.0")
    lines.append(f"        self.Actuator_Voltage = 24.0")
    lines.append(f"        self.actuator_short_circuit_trigger_value = 0")
    lines.append(f"        self.sensor_short_circuit_trigger_value = 0\n")

    lines.append(f"        self.LED_Off = 0")
    lines.append(f"        self.LED_Red = 0")
    lines.append(f"        self.LED_Green = 0\n")

    #Register the variables

    lines.append(f"        self.register_variable(Boolean('{"PinBased"}',causality=Fmi3Causality.parameter,variability=Fmi3Variability.tunable,description='{"Pin based mapping of inputs"}',))")
    lines.append(f"        self.register_variable(Boolean('{"PortBased"}',causality=Fmi3Causality.parameter,variability=Fmi3Variability.tunable,description='{"Port based mapping of inputs"}',))")
    lines.append(f"        self.register_variable(Boolean('{"Compact"}',causality=Fmi3Causality.parameter,variability=Fmi3Variability.tunable,description='{"Compact based mapping of inputs"}',))\n")

    if len(di_pins)!= 0:
        for dis in di_pins:
            lines.append(f"        self.register_variable(Int32('IN_{dis}',causality=Fmi3Causality.input,description='{"Sensor Input"}',))")

        lines.append(f"\n")

        lines.append(f"        self.register_variable(Int32('{"qualifier_di_8_byte1"}',causality=Fmi3Causality.output,description='{"To PLC: shows location of error in the module in inputs"}',))")
        lines.append(f"        self.register_variable(Int32('{"qualifier_di_8_byte2"}',causality=Fmi3Causality.output,description='{"To PLC: shows location of error in the module in inputs"}',))\n")

        lines.append(f"        self.register_variable(Int32('{"outByte1"}',causality=Fmi3Causality.output,description='{"To PLC: Sensor bits converted to Integer"}',))")
        lines.append(f"        self.register_variable(Int32('{"outByte2"}',causality=Fmi3Causality.output,description='{"To PLC: Sensor bits converted to Integer"}',))\n")

    if len(do_pins) != 0:
        for dos in do_pins:
            lines.append(f"        self.register_variable(Int32('OUT_{dos}',causality=Fmi3Causality.output,description='{"Actuator Output"}',))")

        lines.append(f"\n")

        lines.append(f"        self.register_variable(Int32('{"qualifier_do_8_byte1"}',causality=Fmi3Causality.output,description='{"To PLC: shows location of error in the module in outputs"}',))")
        lines.append(f"        self.register_variable(Int32('{"qualifier_do_8_byte2"}',causality=Fmi3Causality.output,description='{"To PLC: shows location of error in the module in outputs"}',))\n")

        lines.append(f"        self.register_variable(Int32('{"inByte1"}',causality=Fmi3Causality.input,description='{"From PLC: Integer value to set the actuators from the module"}',))")
        lines.append(f"        self.register_variable(Int32('{"inByte2"}',causality=Fmi3Causality.input,description='{"From PLC: Integer value to set the actuators from the module"}',))\n")

    lines.append(f"        self.register_variable(Int32('{"system_state_byte_1"}',causality=Fmi3Causality.output,description='{"To PLC: shows state of the module"}',))")
    lines.append(f"        self.register_variable(Int32('{"system_state_byte_2"}',causality=Fmi3Causality.output,description='{"To PLC: shows state of the module"}',))")
    lines.append(f"        self.register_variable(Int32('{"system_state_byte_3"}',causality=Fmi3Causality.output,description='{"To PLC: shows state of the module"}',))")
    lines.append(f"        self.register_variable(Int32('{"system_state_byte_4"}',causality=Fmi3Causality.output,description='{"To PLC: shows state of the module"}',))\n")

    lines.append(f"        self.register_variable(Float64('{"Sensor_Voltage"}',causality=Fmi3Causality.input,description='{"User Interface control of sensor voltage"}',))")
    lines.append(f"        self.register_variable(Float64('{"Actuator_Voltage"}',causality=Fmi3Causality.input,description='{"User Interface control of sensor voltage"}',))")
    lines.append(f"        self.register_variable(Int32('{"actuator_short_circuit_trigger_value"}',causality=Fmi3Causality.input,description='{"Sensor Short circuit can be triggered by changing values from 255 to 0-255"}',))")
    lines.append(f"        self.register_variable(Int32('{"sensor_short_circuit_trigger_value"}',causality=Fmi3Causality.input,description='{"Actuator Short circuit can be triggered by changing values from 255 to 0-255"}',))\n")

    lines.append(f"        self.register_variable(Int32('{"LED_Green"}',causality=Fmi3Causality.output,description='{"LED behaviour of the device"}',))")
    lines.append(f"        self.register_variable(Int32('{"LED_Red"}',causality=Fmi3Causality.output,description='{"LED behaviour of the device"}',))")
    lines.append(f"        self.register_variable(Int32('{"LED_Off"}',causality=Fmi3Causality.output,description='{"LED behaviour of the device"}',))\n")


    # Time and metadata
    lines.append('        self.author = "Raj Kumar"')
    lines.append('        self.description = "A simple description of DIO 8 module from Murrelektronik catalogue"')
    lines.append("        self.time = 0.0")
    lines.append('        self.register_variable(Float64("time", causality=Fmi3Causality.independent))')
    lines.append('        ')
    lines.append('        ')


    return "\n".join(lines)

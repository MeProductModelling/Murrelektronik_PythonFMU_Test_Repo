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
def generate_constructor(json_data):
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

    # Find the first matching master key
    master_key = next(
        (key for key in submodules if key in VALID_MASTER_KEYS),
        None
    )

    if master_key is not None:
        submodules = submodules[master_key]["SubmoduleItems"]
    else:
        raise KeyError("No known master module key found in ResolvedModuleItems.")

    for sub in submodules:
        name = sub["Name"]
        class_info = SUBMODULE_NAME_MAP.get(name)
        if class_info and len(class_info) == 2:
            class_type, instance_name = class_info
            lines.append(f"        self.{instance_name} = {class_type}()")
            lines.append(f"        self.{instance_name}.register(self)\n")

        if class_info and len(class_info) == 4 :
            Sensor_class_type, Sensor_instance_name, Actuator_class_type, Actuator_instance_name = class_info
            lines.append(f"        self.{Sensor_instance_name} = {Sensor_class_type}()")
            lines.append(f"        self.{Sensor_instance_name}.register(self)\n")
            lines.append(f"        self.{Actuator_instance_name} = {Actuator_class_type}()")
            lines.append(f"        self.{Actuator_instance_name}.register(self)\n")

    lines.append(f"        self.plc_ios = PLCIOs()")
    lines.append(f"        self.plc_ios.register(self)\n")

    lines.append(f"        self.user_interface_ios = UserInterfaceIOs()")
    lines.append(f"        self.user_interface_ios.register(self)\n")

    # Time and metadata
    lines.append('        self.author = "Raj Kumar"')
    lines.append('        self.description = "A simple description of DIO 8 module from Murrelektronik catalogue"')
    lines.append("        self.time = 0.0")
    lines.append('        self.register_variable(Float64("time", causality=Fmi3Causality.independent))')
    lines.append('        ')
    lines.append('        ')


    return "\n".join(lines)

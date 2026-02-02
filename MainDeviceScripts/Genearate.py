import json

from MainDeviceScripts.Algorithm_support.Algorithm import generate_algorithm
from MainDeviceScripts.Header import generate_constructor
from MainDeviceScripts.PLCIOs import generate_plcios_class
from MainDeviceScripts.Parameters import generate_parameters_class
from MainDeviceScripts.DigitalInputs import generate_sensor_inputs_class
from MainDeviceScripts.DigitalOutputs import generate_actuator_outputs_class
from MainDeviceScripts.QualifierDI import generate_qualifier_dis_class
from MainDeviceScripts.QualifierDO import generate_qualifier_dos_class
from MainDeviceScripts.SystemState import generate_systemstate_class
from MainDeviceScripts.UserInterfacesIO import User_Interfaces_IO


def generate_code_from_json(data, data_connectors):

    output_code = ""
    #These are the Strings that shall be searched in JSON to find the data...
    VALID_MASTER_KEYS = {
        "DIO_MASTER",
        "DIO_MASTER_IOL2",
        "DIO_MASTER_IOL4",
        "DIO_MASTER_IOL2_EXT1",
        "DI_MASTER",
        "DO_MASTER",
        "DIDO_MASTER",
    }

    # Extract metadata
    dap = data.get("DeviceAccessPointItem", {})
    module_info = data.get("ModuleInfo", {})
    device_id = dap.get("ID", "UnknownDevice")
    class_name = f"MVK{device_id}"
    author = "Raj Kumar"
    description = module_info.get("InfoText", {}).get("@attributes", {}).get("TextId", "")
    if not description:
        description = "A simulation model for Murrelektronik IO device"

    #submodules = data.get("ResolvedModuleItems", {}).get("DIDO_MASTER", {}).get("SubmoduleItems", [])
    submodules = data.get("ResolvedModuleItems", {})
    module_key = next(
        (key for key in submodules if key in VALID_MASTER_KEYS),
        None
    )

    if module_key is not None:
        submodules = submodules[module_key]["SubmoduleItems"]
        # proceed with submodule_items...
    else:
        raise KeyError("No known master module key found in ResolvedModuleItems.")

    generate_parameters = any(sub.get("ID") in {"10", "20", "30", "50", "60", "70", "80", "90", "100", "82", "92", "102"} for sub in submodules)
    generate_sensor_inputs = any(sub.get("ID") in {"11", "21", "81", "83"} for sub in submodules)
    generate_actuator_outputs = any(sub.get("ID") in {"11", "21", "101", "103"} for sub in submodules)
    generate_qualifier_dis = any(sub.get("ID") == "12" for sub in submodules)
    generate_qualifier_dos = any(sub.get("ID") == "13" for sub in submodules)
    generate_systemstate = any(sub.get("ID") == "14" for sub in submodules)



    # Seperate pins and it's function from the JSON to lists
    di_pins = []
    do_pins = []
    # Loop through each connectors (X0..X7)
    for connector, pins in data_connectors.items():
        for pin, value in pins.items():
            # Normalise the value into list of capabilities
            #capabilities = [cap.strip() for cap in value.split("/")]
            capabilities = value
            # If DI is in capabilities, store connectors_pin (e.g. X0_2)
            if"DI / DO" in capabilities:
                pin_num = pin.replace("PIN ", "")
                di_pins.append(f"{connector}_{pin_num}")
                do_pins.append(f"{connector}_{pin_num}")
            elif "DI" in capabilities:
                #pin looks like "PIN2" -> extract number part
                pin_num = pin.replace("PIN ", "")
                di_pins.append(f"{connector}_{pin_num}")
            elif  "DO" in capabilities:
                # pin looks like "PIN2" -> extract number part
                pin_num = pin.replace("PIN ", "")
                do_pins.append(f"{connector}_{pin_num}")

    #The code factoring starts form this.
    #1. Header files, constructor and do_step methods come from this point.
    generated_constructor_code = generate_constructor(data)

    #Store it in output-code string
    output_code = generated_constructor_code + "\n\n"

    # Here enters the do_step algorithm that changes for every device.
    output_code += generate_algorithm(di_pins, do_pins, generate_qualifier_dis, generate_qualifier_dos) +  "\n\n"

    #The parameters are initialised here and registered in the FMI3
    if generate_parameters:
        output_code += generate_parameters_class() + "\n\n"

    # The sensor inputs are initialised here and registered in the FMI3
    if generate_sensor_inputs:
        output_code += generate_sensor_inputs_class(di_pins) + "\n"

    # The actuator outputs are initialised here and registered in the FMI3
    if generate_actuator_outputs:
        output_code += generate_actuator_outputs_class(do_pins) + "\n"

    # The qualifier_dis are initialised here and registered in the FMI3
    if generate_qualifier_dis:
        output_code += generate_qualifier_dis_class() + "\n"
#
    ## The qualifier_dos are initialised here and registered in the FMI3
    if generate_qualifier_dos:
        output_code += generate_qualifier_dos_class() + "\n"
#
    ###The System_state are initialised here and registered in the FMI3
    if generate_systemstate:
        output_code += generate_systemstate_class() + "\n"

    ##The PLCIOs are initialised here and registered in the FMI3
    output_code += generate_plcios_class() + "\n"

    #User Interface IOS
    output_code += User_Interfaces_IO() + "\n"

    #Assign the name of the python file based on the device.
    if output_code:
        with open(class_name+".py", "w") as f:
            f.write(output_code)
        print("Generated: "+ class_name+".py")
    else:
        print("No matching submodule IDs found.")


    if not (generate_parameters or generate_sensor_inputs):
        print("No matching submodule IDs found.")


    return output_code
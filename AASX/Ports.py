


def PortsVAR (data, data_connectors):

    VALID_MASTER_KEYS = {
        "DIO_MASTER",
        "DIO_MASTER_IOL2",
        "DIO_MASTER_IOL4",
        "DIO_MASTER_IOL2_EXT1",
        "DI_MASTER",
        "DO_MASTER",
        "DIDO_MASTER",
    }

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

    generate_parameters = any(
        sub.get("ID") in {"10", "20", "30", "50", "60", "70", "80", "90", "100", "82", "92", "102"} for sub in
        submodules)
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
            # capabilities = [cap.strip() for cap in value.split("/")]
            capabilities = value
            # If DI is in capabilities, store connectors_pin (e.g. X0_2)
            if "DI / DO" in capabilities:
                pin_num = pin.replace("PIN ", "")
                di_pins.append(f"{connector}_{pin_num}")
                do_pins.append(f"{connector}_{pin_num}")
            elif "DI" in capabilities:
                # pin looks like "PIN2" -> extract number part
                pin_num = pin.replace("PIN ", "")
                di_pins.append(f"{connector}_{pin_num}")
            elif "DO" in capabilities:
                # pin looks like "PIN2" -> extract number part
                pin_num = pin.replace("PIN ", "")
                do_pins.append(f"{connector}_{pin_num}")

    OutBytes = ["outByte1","outByte2"]
    InBytes = ["inByte1","inByte2"]
    SystemState = ["SystemState1","SystemState2", "SystemState3", "SystemState4"]
    QualifierDI = ["qualifier_di_Byte_1","qualifier_di_Byte_2"]
    QualifierDO = ["qualifier_do_Byte_1", "qualifier_do_Byte_2"]
    UserInterfaceI = ["Sensor_Voltage", "", "",""]


    Ports ={}
    PortConnector = []
    i = 0

    if  len(di_pins) != 0:
        # Generate Ports for Sensor Inputs
        for pins in di_pins:

            i = i+1

            Variable = {
                "VariableName": f"IN_{pins}",
                "Range": "0 to 1",
                "VariableType": "Integer",
                "VariableDescription": "Sensor Input",
                "UnitList": "TBD",
                "UnitDescription": "TBD",
                "VariableCausality": "Input",
                "VariablePrefix": "TBD"
            }

            PortsConnector = {
                "PortConnectorName": f"IN_{pins}",
                "PortConDescription": "Sensor Input",
                "Variable": Variable
            }

            PortConnector.append(PortsConnector)
            Ports.update({f"PortsConnector{i}": PortsConnector})

        for qdis in QualifierDI:
            i = i + 1

            Variable = {
                "VariableName": f"{qdis}",
                "Range": "0 to 255",
                "VariableType": "Integer",
                "VariableDescription": "qualifier value of inputs from Simulation Block to PLC",
                "UnitList": "TBD",
                "UnitDescription": "TBD",
                "VariableCausality": "Output",
                "VariablePrefix": "TBD"
            }

            PortsConnector = {
                "PortConnectorName": f"{qdis}",
                "PortConDescription": "qualifier value of inputs from Simulation Block to PLC",
                "Variable": Variable
            }

            PortConnector.append(PortsConnector)
            Ports.update({f"PortsConnector{i}": PortsConnector})

        for Byte in OutBytes:
            i = i + 1

            Variable = {
                "VariableName": f"{Byte}",
                "Range": "0 to 255",
                "VariableType": "Integer",
                "VariableDescription": "Value from Simulation Block to PLC sensors in Simulation environment are controlled by PLC",
                "UnitList": "TBD",
                "UnitDescription": "TBD",
                "VariableCausality": "Output",
                "VariablePrefix": "TBD"
            }

            PortsConnector = {
                "PortConnectorName": f"{Byte}",
                "PortConDescription": "Value from Simulation Block to PLC sensors in Simulation environment are controlled by PLC",
                "Variable": Variable
            }
            PortConnector.append(PortsConnector)
            Ports.update({f"PortsConnector{i}": PortsConnector})

    # Generate Ports for Actuator Outputs
    if len(do_pins) != 0:
        for pins in do_pins:

            i = i+1

            Variable = {
                "VariableName": f"OUT_{pins}",
                "Range": "0 to 1",
                "VariableType": "Integer",
                "VariableDescription": "Actuator Output",
                "UnitList": "TBD",
                "UnitDescription": "TBD",
                "VariableCausality": "Output",
                "VariablePrefix": "TBD"
            }

            PortsConnector = {
                "PortConnectorName": f"OUT_{pins}",
                "PortConDescription": "Actuator Output",
                "Variable": Variable
            }

            PortConnector.append(PortsConnector)
            Ports.update({f"PortsConnector{i}": PortsConnector})

        for qdos in QualifierDO:
            i = i + 1

            Variable = {
                "VariableName": f"{qdos}",
                "Range": "0 to 255",
                "VariableType": "Integer",
                "VariableDescription": "qualifier value of outputs from Simulation Block to PLC",
                "UnitList": "TBD",
                "UnitDescription": "TBD",
                "VariableCausality": "Output",
                "VariablePrefix": "TBD"
            }

            PortsConnector = {
                "PortConnectorName": f"{qdos}",
                "PortConDescription": "qualifier value of outputs from Simulation Block to PLC",
                "Variable": Variable
            }

            PortConnector.append(PortsConnector)
            Ports.update({f"PortsConnector{i}": PortsConnector})

        for Byte in InBytes:
            i = i + 1

            Variable = {
                "VariableName": f"{Byte}",
                "Range": "0 to 255",
                "VariableType": "Integer",
                "VariableDescription": "Value from PLC to Simulation Block to control actuators in Simulation environment",
                "UnitList": "TBD",
                "UnitDescription": "TBD",
                "VariableCausality": "Input",
                "VariablePrefix": "TBD"
            }

            PortsConnector = {
                "PortConnectorName": f"{Byte}",
                "PortConDescription": "Value from PLC to Simulation Block to control actuators in Simulation environment",
                "Variable": Variable
            }
            PortConnector.append(PortsConnector)
            Ports.update({f"PortsConnector{i}": PortsConnector})

    for ss in SystemState:
        i = i + 1

        Variable = {
            "VariableName": f"{ss}",
            "Range": "0 to 255",
            "VariableType": "Integer",
            "VariableDescription": "state of the device value from Simulation Block to PLC",
            "UnitList": "TBD",
            "UnitDescription": "TBD",
            "VariableCausality": "Output",
            "VariablePrefix": "TBD"
        }

        PortsConnector = {
            "PortConnectorName": f"{ss}",
            "PortConDescription": "state of the device value from Simulation Block to PLC",
            "Variable": Variable
        }
        PortConnector.append(PortsConnector)
        Ports.update({f"PortsConnector{i}": PortsConnector})

    #Sensor Voltage
    i= i+1
    Variable = {
        "VariableName": "Sensor_Voltage",
        "Range": "0 to 50",
        "VariableType": "Double",
        "VariableDescription": "User Interface Control to test the simulation block behaviour on change of voltage",
        "UnitList": "TBD",
        "UnitDescription": "TBD",
        "VariableCausality": "Input",
        "VariablePrefix": "TBD"
    }

    PortsConnector = {
        "PortConnectorName": "Sensor_Voltage",
        "PortConDescription": "User Interface Control to test the simulation block behaviour on change of voltage",
        "Variable": Variable
    }
    PortConnector.append(PortsConnector)
    Ports.update({f"PortsConnector{i}": PortsConnector})

    # Actuator Voltage
    i = i + 1
    Variable = {
        "VariableName": "Actuator_Voltage",
        "Range": "0 to 50",
        "VariableType": "Double",
        "VariableDescription": "User Interface Control to test the simulation block behaviour on change of voltage",
        "UnitList": "TBD",
        "UnitDescription": "TBD",
        "VariableCausality": "Input",
        "VariablePrefix": "TBD"
    }

    PortsConnector = {
        "PortConnectorName": "Actuator_Voltage",
        "PortConDescription": "User Interface Control to test the simulation block behaviour on change of voltage",
        "Variable": Variable
    }
    PortConnector.append(PortsConnector)
    Ports.update({f"PortsConnector{i}": PortsConnector})

    # actuator_short_circuit_trigger_value
    i = i + 1
    Variable = {
        "VariableName": "actuator_short_circuit_trigger_value",
        "Range": "0 to 255",
        "VariableType": "Double",
        "VariableDescription": "User Interface Control to test the simulation block behaviour on triggering error on actuators ",
        "UnitList": "TBD",
        "UnitDescription": "TBD",
        "VariableCausality": "Input",
        "VariablePrefix": "TBD"
    }

    PortsConnector = {
        "PortConnectorName": "actuator_short_circuit_trigger_value",
        "PortConDescription": "User Interface Control to test the simulation block behaviour on triggering error on actuators ",
        "Variable": Variable
    }
    PortConnector.append(PortsConnector)
    Ports.update({f"PortsConnector{i}": PortsConnector})

    # sensor_short_circuit_trigger_value
    i = i + 1
    Variable = {
        "VariableName": "sensor_short_circuit_trigger_value",
        "Range": "0 to 255",
        "VariableType": "Double",
        "VariableDescription": "User Interface Control to test the simulation block behaviour on change of Sensor voltage",
        "UnitList": "TBD",
        "UnitDescription": "TBD",
        "VariableCausality": "Input",
        "VariablePrefix": "TBD"
    }

    PortsConnector = {
        "PortConnectorName": "sensor_short_circuit_trigger_value",
        "PortConDescription": "User Interface Control to test the simulation block behaviour on change of Sensor voltage",
        "Variable": Variable
    }
    PortConnector.append(PortsConnector)
    Ports.update({f"PortsConnector{i}": PortsConnector})

    # LED_Green
    i = i + 1
    Variable = {
        "VariableName": "LED_Green",
        "Range": "0 to 1",
        "VariableType": "Integer",
        "VariableDescription": "LEDs of the device",
        "UnitList": "TBD",
        "UnitDescription": "TBD",
        "VariableCausality": "Output",
        "VariablePrefix": "TBD"
    }

    PortsConnector = {
        "PortConnectorName": "LED_Green",
        "PortConDescription": "LEDs of the device",
        "Variable": Variable
    }
    PortConnector.append(PortsConnector)
    Ports.update({f"PortsConnector{i}": PortsConnector})

    # LED_Red
    i = i + 1
    Variable = {
        "VariableName": "LED_Red",
        "Range": "0 to 1",
        "VariableType": "Integer",
        "VariableDescription": "LEDs of the device",
        "UnitList": "TBD",
        "UnitDescription": "TBD",
        "VariableCausality": "Output",
        "VariablePrefix": "TBD"
    }

    PortsConnector = {
        "PortConnectorName": "LED_Red",
        "PortConDescription": "LEDs of the device",
        "Variable": Variable
    }
    PortConnector.append(PortsConnector)
    Ports.update({f"PortsConnector{i}": PortsConnector})

    # LED_Off
    i = i + 1
    Variable = {
        "VariableName": "LED_Off",
        "Range": "0 to 1",
        "VariableType": "Integer",
        "VariableDescription": "LEDs of the device",
        "UnitList": "TBD",
        "UnitDescription": "TBD",
        "VariableCausality": "Output",
        "VariablePrefix": "TBD"
    }

    PortsConnector = {
        "PortConnectorName": "LED_Off",
        "PortConDescription": "LEDs of the device",
        "Variable": Variable
    }
    PortConnector.append(PortsConnector)
    Ports.update({f"PortsConnector{i}": PortsConnector})

    FinalPorts ={
        "PortsConnector": PortConnector
    }

    return FinalPorts
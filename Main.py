import tkinter as tk
from tkinter import filedialog

from AASX.AASXSubModelGenerator import AASXSimulationSubModelGenerator
from gsdml_parser import parse_component_info
import json
from MainDeviceScripts.Genearate import generate_code_from_json
from MainDeviceScripts.GeneratePythonfile import generate_code_from_json_1
from AASXSubmodelConnectorsParser import extract_pins_as_major_tags
from AASX import AASXSubModelGenerator
import AASXConnectorsData
from pathlib import Path


def main():
    # GUI to select XML file
    root = tk.Tk()
    root.withdraw()
    xml_path = filedialog.askopenfilename(
        title="Select GSDML File",
        filetypes=[("XML files", "*.xml"), ("All files", "*.*")]
    )
    if not xml_path:
        print("No file selected.")
        return

    # Ask user for component number
    component_id = input("Enter component number (e.g., 55530): ").strip()

    # Initialise Output JSON path : This JSON is the output from parsing GSDML.
    output_path = component_id+"_output.json"

    #Initialise Output path of Connectors Info.
    output_path_connectors_info = component_id + "_connectors.json"

    #Initialise Output path of Simulation Submodel for AASX
    output_path_AASXSimulationSubModel = "Simulation_data_" + component_id + ".json"

    #Search for AAS in the Database
    BASE_DIR = Path(__file__).resolve().parent
    DATA_DIR = BASE_DIR / "AASXConnectorsData"  # folder name where JSONs are stored

    json_path = DATA_DIR / ("ME_"+ component_id + "_Submodel_TechnicalData"+".json")

    # Extract pin info and save in Json as connectors info.
    extract_pins_as_major_tags(json_path,  output_path_connectors_info)

    #Read GSDML file and post if iut is success or not...
    success = parse_component_info(xml_path, component_id, output_path)

    #Print the output status on to the terminal
    if success:
        print(f"\nComponent info saved to: {output_path}")
    else:
        print(f"\nComponent {component_id} not found.")


    #Open the output data that was generated from the GSDML file. And store the data into the variable named "data"
    with open(output_path, "r") as f:
        data = json.load(f)
    #open the data connectors info and load it into the variable "data_connecotrs"
    with open(output_path_connectors_info, "r") as f:
        data_connectors = json.load(f)
    #Now use the above declared variables and their data to generate Python file of the device..
    generated_code = generate_code_from_json_1(data, data_connectors)
    #Print of the code is generated successfully.
    if generated_code:
        print("Code generation complete")
    else:
        print("No code generated.")

    # Extract simmulation data and save into AASX Simulation SubModel JSON
    AASXSimulationSubModelGenerator(data, data_connectors, component_id, output_path_AASXSimulationSubModel)

if __name__ == "__main__":
    main()

import tkinter as tk
from tkinter import filedialog
from gsdml_parser import parse_component_info
import json
from MainDeviceScripts.Genearate import generate_code_from_json
from AASXSubmodelConnectorsParser import extract_pins_as_major_tags
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

    # Parse and export
    output_path = component_id+"_output.json"
        #
    output_path_connectors_info = component_id + "_connectors.json"
        #Search for AAS in the Database
    BASE_DIR = Path(__file__).resolve().parent
    DATA_DIR = BASE_DIR / "AASXConnectorsData"  # folder name where JSONs are stored

    json_path = DATA_DIR / ("ME_"+ component_id + "_Submodel_TechnicalData"+".json")

    extract_pins_as_major_tags(json_path,  output_path_connectors_info)

    success = parse_component_info(xml_path, component_id, output_path)

    if success:
        print(f"\nComponent info saved to: {output_path}")
    else:
        print(f"\nComponent {component_id} not found.")


    with open(output_path, "r") as f:
        data = json.load(f)

    with open(output_path_connectors_info, "r") as f:
        data_connectors = json.load(f)

    generated_code = generate_code_from_json(data, data_connectors)
    if generated_code:
        print("Code generation complete")
    else:
        print("No code generated.")

if __name__ == "__main__":
    main()

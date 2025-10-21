import json


def extract_pins_as_major_tags(input_file, output_file):
    # Load JSON
    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Navigate into SubmodelElements → TechnicalPropertyAreas
    submodel_elements = data.get("submodelElements", [])
    connectors_output = {}

    for element in submodel_elements:
        if element.get("idShort") == "TechnicalPropertyAreas":
            tech_areas = element.get("value", [])

            # Look for "Connectors" inside TechnicalPropertyAreas
            for area in tech_areas:
                if area.get("idShort") == "Connectors":
                    for connector in area.get("value", []):
                        connector_name = connector.get("idShort")
                        pins_dict = {}

                        # Find "Pin assignment"
                        for prop in connector.get("value", []):
                            if prop.get("idShort") == "Installation":
                                for pin in prop.get("value", []):
                                    if pin.get("idShort") == "Pin assignment":
                                        for values in pin.get("value", []):
                                            if values.get("idShort") in {"PIN 2"}:
                                                pins_dict["PIN 2"] = values.get("value", [])
                                            if values.get("idShort") in {"PIN 4"}:
                                                pins_dict["PIN 4"] = values.get("value", [])

                        # Only include connectors with Pin 2/Pin 4
                        if pins_dict:
                            connectors_output[connector_name] = pins_dict

    # Save result
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(connectors_output, f, indent=4, ensure_ascii=False)

    print(f" Extracted Pin 2 & Pin 4 info saved to {output_file}")
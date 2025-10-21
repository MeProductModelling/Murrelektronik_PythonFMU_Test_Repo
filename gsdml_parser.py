import xml.etree.ElementTree as ET
import json

def element_to_dict(elem, ns=None):
    """Convert XML to nested dict."""
    result = {}
    if elem.attrib:
        result["@attributes"] = elem.attrib
    children = list(elem)
    if children:
        for child in children:
            tag = child.tag.split('}')[-1]
            value = element_to_dict(child, ns)
            if tag in result:
                if isinstance(result[tag], list):
                    result[tag].append(value)
                else:
                    result[tag] = [result[tag], value]
            else:
                result[tag] = value
    else:
        text = elem.text.strip() if elem.text else None
        if text and not elem.attrib:
            return text
    return result

def extract_module_info(modinfo_elem, ns):
    """Extract all contents under ModuleInfo into a dict."""
    return element_to_dict(modinfo_elem, ns)

def parse_component_info(xml_path, component_id, output_path):
    ns = {
        'ns': 'http://www.profibus.com/GSDML/2003/11/DeviceProfile'
    }

    tree = ET.parse(xml_path)
    root = tree.getroot()

    device_items = root.findall(".//ns:DeviceAccessPointItem", ns)

    for item in device_items:
        if item.attrib.get("ID") == component_id:
            result = {}

            # 1. DeviceAccessPointItem attributes
            result["DeviceAccessPointItem"] = item.attrib

            # 2. ModuleInfo section
            modinfo = item.find("ns:ModuleInfo", ns)
            if modinfo is not None:
                result["ModuleInfo"] = extract_module_info(modinfo, ns)

            # 3. UsableModules (ModuleItemRef)
            useable = item.find("ns:UseableModules", ns)
            module_refs = []
            resolved_modules = {}

            if useable is not None:
                for ref in useable.findall("ns:ModuleItemRef", ns):
                    ref_attribs = ref.attrib
                    module_refs.append(ref_attribs)

                    module_id = ref_attribs.get("ModuleItemTarget")
                    if not module_id:
                        continue

                    module_elem = root.find(f".//ns:ModuleItem[@ID='{module_id}']", ns)
                    submodule_items = []

                    if module_elem is not None:
                        for sub_ref in module_elem.findall(".//ns:SubmoduleItemRef", ns):
                            sub_id = sub_ref.attrib.get("SubmoduleItemTarget")
                            if not sub_id:
                                continue

                            # Look up the SubmoduleItem by ID
                            sub_elem = root.find(f".//ns:SubmoduleItem[@ID='{sub_id}']", ns)
                            sub_name = ""
                            sub_info = ""
                            sub_name_textid = ""
                            sub_info_textid =""

                            if sub_elem is not None:
                                module_info = sub_elem.find("ns:ModuleInfo", ns)
                                if module_info is not None:
                                    name_elem = module_info.find("ns:Name", ns)
                                    sub_name = name_elem.text if name_elem is not None else ""
                                    sub_name_textid = name_elem.attrib.get("TextId") if name_elem is not None else ""

                                    info_elem = module_info.find("ns:InfoText", ns)
                                    sub_info = info_elem.text if info_elem is not None else ""
                                    sub_info_textid = info_elem.attrib.get("TextId") if info_elem is not None else ""


                            submodule_items.append({
                                "ID": sub_id,
                                "Name": sub_name_textid,
                                "Description": sub_info_textid

                            })

                    resolved_modules[module_id] = {
                        "SubmoduleItems": submodule_items
                    }

            result["UseableModules"] = module_refs
            result["ResolvedModuleItems"] = resolved_modules

            # 4. ModuleItem entries (used via Target refs - optional enhancement)

            # 5. ParameterRecordDataItem (if any exist)
            params = root.findall(f".//ns:ParameterRecordDataItem", ns)
            related_params = []
            for p in params:
                if p.attrib.get("SubmoduleIdentValue") == component_id:
                    related_params.append(p.attrib)
            result["ParameterRecordDataItem"] = related_params

            # Write to JSON
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(result, f, indent=4)

            return True

    return False

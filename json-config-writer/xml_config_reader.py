import xml.etree.ElementTree as ET

from elements import (TextElement, BooleanElement, ChoiceElement, EditableElement,
                       IntegerElement, FloatElement, ColorElement,
                       FilePathElement, DirectoryPathElement)



def read_config(file_path: str) -> list[EditableElement]:
    tree = ET.parse(file_path)
    root = tree.getroot()
    elements : list[EditableElement] = []
    for elem in root:
        if elem.tag == "TextElement":
            key = elem.attrib["name"]
            default = elem.attrib.get("default", "")
            min_length = int(elem.attrib["min_length"]) if "min_length" in elem.attrib else 0
            max_length = int(elem.attrib["max_length"]) if "max_length" in elem.attrib else -1
            allowed_chars = elem.attrib.get("allowed_chars", r"a-zA-Z0-9_.-")
            elements.append(TextElement(key, default, min_length, max_length, allowed_chars))
        elif elem.tag == "BooleanElement":
            key = elem.attrib["name"]
            default = elem.attrib.get("default", "false").lower() == "true"
            elements.append(BooleanElement(key, default))
        elif elem.tag == "ChoiceElement":
            key = elem.attrib["name"]
            default = elem.attrib.get("default")
            choices = [choice.attrib["value"] for choice in elem.findall("Choice")]
            if default is None and choices:
                default = choices[0]
            elements.append(ChoiceElement(key, choices, default))
        elif elem.tag == "IntegerElement":
            key = elem.attrib["name"]
            default = int(elem.attrib.get("default", "0"))
            min_ = int(elem.attrib["min"]) if "min" in elem.attrib else None
            max_ = int(elem.attrib["max"]) if "max" in elem.attrib else None
            elements.append(IntegerElement(key, default, min_, max_))
        elif elem.tag == "FloatElement":
            key = elem.attrib["name"]
            default = float(elem.attrib.get("default", "0.0"))
            min_ = float(elem.attrib["min"]) if "min" in elem.attrib else None
            max_ = float(elem.attrib["max"]) if "max" in elem.attrib else None
            elements.append(FloatElement(key, default, min_, max_))
        elif elem.tag == "ColorElement":
            key = elem.attrib["name"]
            default = elem.attrib.get("default", "#000000")
            elements.append(ColorElement(key, default))
        elif elem.tag == "FilePathElement":
            key = elem.attrib["name"]
            default = elem.attrib.get("default", "")
            elements.append(FilePathElement(key, default))
        elif elem.tag == "DirectoryPathElement":
            key = elem.attrib["name"]
            default = elem.attrib.get("default", "")
            elements.append(DirectoryPathElement(key, default))
        else:
            print(f"Unknown element type: {elem.tag}")
    return elements
        
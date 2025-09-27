import xml.etree.ElementTree as ET
import re
from elements import (TextElement, BooleanElement, ChoiceElement, EditableElement,
                       IntegerElement, FloatElement, ColorElement,
                       FilePathElement, DirectoryPathElement)


def get_element_tag(tag: str) -> str:
    # Remove namespace if present
    match = re.match(r'\{.*\}(.*)', tag)
    return match[1] if match else tag


def read_config(file_path: str) -> list[EditableElement]:
    tree = ET.parse(file_path)
    root = tree.getroot()
    elements : list[EditableElement] = []
    for elem in root:
        key = elem.attrib["key"]
        name = elem.attrib["name"]
        if get_element_tag(elem.tag) == "TextElement":
            default = elem.attrib.get("default", "")
            min_length = int(elem.attrib["min_length"]) if "min_length" in elem.attrib else 0
            max_length = int(elem.attrib["max_length"]) if "max_length" in elem.attrib else -1
            allowed_chars = elem.attrib.get("allowed_chars", r"a-zA-Z0-9_.-")
            elements.append(TextElement(key, name, default, min_length, max_length, allowed_chars))

        elif get_element_tag(elem.tag) == "BooleanElement":
            default = elem.attrib.get("default", "false").lower() == "true"
            elements.append(BooleanElement(key, name, default))

        elif get_element_tag(elem.tag) == "ChoiceElement":
            default = elem.attrib.get("default")
            choices = [choice.attrib["value"] for choice in elem.findall("{http://json-config-writer/schema}Choice")]
            if default is None and choices:
                default = choices[0]
            elements.append(ChoiceElement(key, name, choices, default))

        elif get_element_tag(elem.tag) == "IntegerElement":
            default = int(elem.attrib.get("default", "0"))
            min_ = int(elem.attrib["min"]) if "min" in elem.attrib else None
            max_ = int(elem.attrib["max"]) if "max" in elem.attrib else None
            elements.append(IntegerElement(key, name, default, min_, max_))

        elif get_element_tag(elem.tag) == "FloatElement":
            default = float(elem.attrib.get("default", "0.0"))
            min_ = float(elem.attrib["min"]) if "min" in elem.attrib else None
            max_ = float(elem.attrib["max"]) if "max" in elem.attrib else None
            elements.append(FloatElement(key, name, default, min_, max_))

        elif get_element_tag(elem.tag) == "ColorElement":
            default = elem.attrib.get("default", "#000000")
            elements.append(ColorElement(key, name, default))

        elif get_element_tag(elem.tag) == "FilePathElement":
            default = elem.attrib.get("default", "")
            elements.append(FilePathElement(key, name, default))

        elif get_element_tag(elem.tag) == "DirectoryPathElement":
            default = elem.attrib.get("default", "")
            elements.append(DirectoryPathElement(key, name, default))

        else:
            print(f"Unknown element type: {get_element_tag(elem.tag)}")
    return elements

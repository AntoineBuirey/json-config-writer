import xml.etree.ElementTree as ET
import re
from elements import (TextElement, BooleanElement, ChoiceElement, EditableElement,
                       IntegerElement, FloatElement, ColorElement, SubCategoryElement,
                       FilePathElement, DirectoryPathElement, ListElement)

def get_element_tag(tag: str) -> str:
    # Remove namespace if present
    match = re.match(r'\{.*\}(.*)', tag)
    return match[1] if match else tag


def _parse_text_element(elem : ET.Element):
    tag = elem.attrib["tag"]
    name = elem.attrib["name"]
    default = elem.attrib.get("default", "")
    min_length = int(elem.attrib["min_length"]) if "min_length" in elem.attrib else 0
    max_length = int(elem.attrib["max_length"]) if "max_length" in elem.attrib else -1
    allowed_chars = elem.attrib.get("allowed_chars", r"a-zA-Z0-9_.-")
    return TextElement(tag, name, default, min_length, max_length, allowed_chars)

def _parse_boolean_element(elem : ET.Element):
    tag = elem.attrib["tag"]
    name = elem.attrib["name"]
    default = elem.attrib.get("default", "false").lower() == "true"
    return BooleanElement(tag, name, default)

def _parse_choice_element(elem : ET.Element):
    tag = elem.attrib["tag"]
    name = elem.attrib["name"]
    default = elem.attrib.get("default")
    choices = [choice.attrib["value"] for choice in elem.findall("{http://json-config-writer/schema}Choice")]
    if default is None and choices:
        default = choices[0]
    return ChoiceElement(tag, name, choices, default)

def _parse_integer_element(elem : ET.Element):
    tag = elem.attrib["tag"]
    name = elem.attrib["name"]
    default = int(elem.attrib.get("default", "0"))
    min_ = int(elem.attrib["min"]) if "min" in elem.attrib else None
    max_ = int(elem.attrib["max"]) if "max" in elem.attrib else None
    return IntegerElement(tag, name, default, min_, max_)

def _parse_float_element(elem : ET.Element):
    tag = elem.attrib["tag"]
    name = elem.attrib["name"]
    default = float(elem.attrib.get("default", "0.0"))
    min_ = float(elem.attrib["min"]) if "min" in elem.attrib else None
    max_ = float(elem.attrib["max"]) if "max" in elem.attrib else None
    return FloatElement(tag, name, default, min_, max_)

def _parse_color_element(elem : ET.Element):
    tag = elem.attrib["tag"]
    name = elem.attrib["name"]
    default = elem.attrib.get("default", "#000000")
    return ColorElement(tag, name, default)

def _parse_file_path_element(elem : ET.Element):
    tag = elem.attrib["tag"]
    name = elem.attrib["name"]
    default = elem.attrib.get("default", "")
    return FilePathElement(tag, name, default)

def _parse_directory_path_element(elem : ET.Element):
    tag = elem.attrib["tag"]
    name = elem.attrib["name"]
    default = elem.attrib.get("default", "")
    return DirectoryPathElement(tag, name, default)

def _parse_list_element(elem : ET.Element):
    tag = elem.attrib["tag"]
    name = elem.attrib["name"]
    defaults = [default.attrib["value"] for default in elem.findall("{http://json-config-writer/schema}Default")]
    return ListElement(tag, name, defaults)

def _parse_subcategory_element(elem : ET.Element):
    tag = elem.attrib["tag"]
    name = elem.attrib["name"]
    sub_elements = []
    for sub_elem in elem:
        tag_name = get_element_tag(sub_elem.tag)
        if tag_name in _PARSERS:
            parser = _PARSERS[tag_name]
            element = parser(sub_elem)
            sub_elements.append(element)
        else:
            print(f"Unknown sub-element type: {tag_name}")
    return SubCategoryElement(tag, name, sub_elements)

_PARSERS = {
    "TextElement": _parse_text_element,
    "BooleanElement": _parse_boolean_element,
    "ChoiceElement": _parse_choice_element,
    "IntegerElement": _parse_integer_element,
    "FloatElement": _parse_float_element,
    "ColorElement": _parse_color_element,
    "FilePathElement": _parse_file_path_element,
    "DirectoryPathElement": _parse_directory_path_element,
    "ListElement": _parse_list_element,
    "SubCategoryElement": _parse_subcategory_element,
}

def read_config(file_path: str) -> list[EditableElement]:
    tree = ET.parse(file_path)
    root = tree.getroot()
    elements : list[EditableElement] = []
    for elem in root:
        tag_name = get_element_tag(elem.tag)
        if tag_name in _PARSERS:
            parser = _PARSERS[tag_name]
            element = parser(elem)
            elements.append(element)
        else:
            print(f"Unknown element type: {tag_name}")
    return elements
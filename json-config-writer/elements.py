import re
from typing import TypeVar, Sequence, Any
from abc import ABC, abstractmethod

class BaseElement(ABC):
    """
    An abstract base class for all configuration elements.
    """
    def __init__(self, tag: str, name: str):
        self.__tag = tag
        self.__name = name

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(tag={self.__tag})"

    @property
    def tag(self) -> str:
        return self.__tag
    
    @property
    def name(self) -> str:
        return self.__name

class EditableElement(BaseElement, ABC):
    """
    An abstract base class for elements that allow a input from a free text field.
    """
    @abstractmethod
    def from_string(self, value: str): ...

    def get(self) -> Any: ...


    def set(self, value: Any): ...



# text-based elements
class TextElement(EditableElement):
    """
    An abstract base class for text-based configuration elements.
    """
    def __init__(self, tag: str, name: str, default: str = "", min_length : int = 0, max_length: int = -1, allowed_chars: str = r"a-zA-Z0-9_.-"):
        super().__init__(tag, name)
        self.__value = default
        self.__min_length = min_length
        self.__max_length = max_length # -1 means no limit
        self.__allowed_chars = re.compile(f"^[{allowed_chars}]*$")
        
        self.__validate(default)

    def __validate(self, value: str) -> None:
        if not isinstance(value, str):
            raise ValueError("Value must be a string")
        if len(value) < self.__min_length:
            raise ValueError(f"Value must be at least {self.__min_length} characters long")
        if self.__max_length != -1 and len(value) > self.__max_length:
            raise ValueError(f"Value must be at most {self.__max_length} characters long")
        if not self.__allowed_chars.match(value):
            raise ValueError("Value contains invalid characters")

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(tag={self.__tag}, value={self.__value})"

    def set(self, value: str) -> None:
        self.__validate(value)
        self.__value = value

    def get(self) -> str:
        return self.__value
    
    def from_string(self, value: str) -> None:
        self.set(value)

class ColorElement(TextElement):
    def __init__(self, tag: str, name: str, default: str = "#000000"):
        super().__init__(tag, name, default, min_length=4, max_length=7, allowed_chars=r"#0-9a-fA-F")

class PathElement(TextElement):
    def __init__(self, tag: str, name: str, default: str = ""):
        # Allow / and \ in paths
        super().__init__(tag, name, default, min_length=1, max_length=-1, allowed_chars=r"a-zA-Z0-9_.\-\\/")

class FilePathElement(PathElement): ...
class DirectoryPathElement(PathElement): ...




T = TypeVar('T')
class ChoiceElement(EditableElement):
    """
    A class for choice configuration elements.
    """
    def __init__(self, tag: str, name: str, choices: Sequence[T], default: T):
        super().__init__(tag, name)
        if not choices:
            raise ValueError("Choices list cannot be empty")
        if default not in choices:
            raise ValueError("Default value must be one of the choices")
        self.__choices = choices
        self.__value = default

    def from_string(self, value: str) -> None:
        self.set(value)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(tag={self.__tag}, value={self.__value}, choices={self.__choices})"

    def set(self, value: object) -> None:
        if value not in self.__choices:
            raise ValueError(f"Value must be one of the choices: {self.__choices}")
        self.__value = value

    def get(self) -> object:
        return self.__value
    
    @property
    def choices(self) -> Sequence[object]:
        return self.__choices




# number-based elements
class IntegerElement(EditableElement):
    """
    A class for integer configuration elements.
    """
    def __init__(self, tag: str, name: str, default: int = 0, min_ : None|int = None, max_ : None|int = None):
        super().__init__(tag, name)
        self.__value = default
        self.__min = min_
        self.__max = max_
        self.__validate(default)

    def __validate(self, value: int) -> None:
        if not isinstance(value, int):
            raise ValueError("Value must be an integer")
        if self.__min is not None and value < self.__min:
            raise ValueError(f"Value must be at least {self.__min}")
        if self.__max is not None and value > self.__max:
            raise ValueError(f"Value must be at most {self.__max}")

    def from_string(self, value: str) -> None:
        try:
            int_value = int(value)
        except ValueError:
            raise ValueError("Value must be an integer")
        self.set(int_value)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(tag={self.__tag}, value={self.__value})"

    def set(self, value: int) -> None:
        self.__validate(value)
        self.__value = value

    def get(self) -> int:
        return self.__value

class FloatElement(EditableElement):
    """
    A class for float configuration elements.
    """
    def __init__(self, tag: str, name: str, default: float = 0.0, min_ : None|float = None, max_ : None|float = None):
        super().__init__(tag, name)
        self.__value = default
        self.__min = min_
        self.__max = max_
        self.__validate(default)

    def __validate(self, value: float) -> None:
        if not isinstance(value, float):
            raise ValueError("Value must be a float")
        if self.__min is not None and value < self.__min:
            raise ValueError(f"Value must be at least {self.__min}")
        if self.__max is not None and value > self.__max:
            raise ValueError(f"Value must be at most {self.__max}")

    def from_string(self, value: str) -> None:
        try:
            float_value = float(value)
        except ValueError:
            raise ValueError("Value must be a float")
        self.set(float_value)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(tag={self.__tag}, value={self.__value})"

    def set(self, value: float) -> None:
        self.__validate(value)
        self.__value = value

    def get(self) -> float:
        return self.__value




# other elements
class BooleanElement(EditableElement):
    """
    A class for boolean configuration elements.
    """
    def __init__(self, tag: str, name: str, default: bool = False):
        super().__init__(tag, name)
        self.__value = default

    def from_string(self, value: str) -> None:
        if value.lower() in ("true", "1", "yes", "on"):
            self.set(True)
        elif value.lower() in ("false", "0", "no", "off"):
            self.set(False)
        else:
            raise ValueError("Value must be a boolean (true/false)")

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(tag={self.__tag}, value={self.__value})"

    def set(self, value: bool) -> None:
        if not isinstance(value, bool):
            raise ValueError("Value must be a boolean")
        self.__value = value

    def get(self) -> bool:
        return self.__value

class FixedElement(BaseElement):
    """
    A class for fixed configuration elements that cannot be edited.
    """
    def __init__(self, tag: str, name: str, value):
        super().__init__(tag, name)
        self.__value = value

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(tag={self.__tag}, value={self.__value})"

    def get(self):
        return self.__value



class ListElement(EditableElement):
    """
    A class for list configuration elements.
    """
    def __init__(self, tag: str, name: str, default: Sequence[str] = ()):
        super().__init__(tag, name)
        self.__value = list(default)
    
    def from_string(self, value: str) -> None:
        # Expecting a comma-separated list
        items = [item.strip() for item in value.split(",")]
        self.set(items)
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(tag={self.__tag}, value={self.__value})"
    
    def set(self, value: Sequence[str]) -> None:
        if not all(isinstance(item, str) for item in value):
            raise ValueError("All items in the list must be strings")
        self.__value = list(value)
    
    def get(self) -> Sequence[str]:
        return self.__value

    def append(self, item: str) -> None:
        if not isinstance(item, str):
            raise ValueError("Item must be a string")
        self.__value.append(item)
    
    def remove(self, item: str) -> None:
        self.__value.remove(item)

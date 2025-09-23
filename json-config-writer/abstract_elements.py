from abc import ABC, abstractmethod

class BaseElement(ABC):
    """
    An abstract base class for all configuration elements.
    """
    def __init__(self, key: str):
        self.__key = key

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(key={self.__key})"

    @property
    def key(self) -> str:
        return self.__key


class EditableElement(BaseElement, ABC):
    """
    An abstract base class for elements that allow a input from a free text field.
    """
    @abstractmethod
    def from_string(self, value: str): ...

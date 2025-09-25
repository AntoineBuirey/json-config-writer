import tkinter as tk
import tkinter.ttk as ttk
from tkinter import colorchooser, filedialog
from abc import ABC, abstractmethod

from elements import (TextElement, BooleanElement, ChoiceElement, EditableElement,
                       IntegerElement, FloatElement, ColorElement, PathElement,
                       FilePathElement, DirectoryPathElement)


class ElementWidget(ttk.Frame):
    def __init__(self, parent: tk.Misc, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

    def confirm(self) -> bool:
        """
        Confirm the value in the widget and update the associated element.
        Returns True if the value is valid, False otherwise.
        """
        raise NotImplementedError("Subclasses must implement this method")


class TextElementWidget(ElementWidget):
    def __init__(self, parent: tk.Misc, element: TextElement):
        super().__init__(parent)
        self.element = element

        self.label = ttk.Label(self, text=element.key)
        self.label.pack(side=tk.LEFT, padx=5, pady=5)

        self.var = tk.StringVar(value=element.get())
        self.entry = ttk.Entry(self, textvariable=self.var)
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, pady=5)

    
    def confirm(self) -> bool:
        try:
            self.element.set(self.var.get())
            self.entry.config(foreground="black")
            return True
        except ValueError as e:
            print(f"Invalid input for {self.element.key}: {e}")
            self.entry.config(foreground="red")
            return False

class BooleanElementWidget(ElementWidget):
    def __init__(self, parent: tk.Misc, element: BooleanElement):
        super().__init__(parent)
        self.element = element

        self.var = tk.BooleanVar(value=element.get())
        self.checkbutton = ttk.Checkbutton(self, text=element.key, variable=self.var)
        self.checkbutton.pack(side=tk.LEFT, padx=5, pady=5)

    
    def confirm(self) -> bool:
        try:
            self.element.set(self.var.get())
            return True
        except ValueError as e:
            print(f"Invalid input for {self.element.key}: {e}")
            return False

class ChoiceElementWidget(ElementWidget):
    def __init__(self, parent: tk.Misc, element: ChoiceElement):
        super().__init__(parent)
        self.element = element

        self.label = ttk.Label(self, text=element.key)
        self.label.pack(side=tk.LEFT, padx=5, pady=5)

        self.var = tk.StringVar(value=str(element.get()))
        self.combobox = ttk.Combobox(self, textvariable=self.var, values=[str(e) for e in element.choices], state="readonly")
        self.combobox.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, pady=5)

    
    def confirm(self) -> bool:
        try:
            self.element.set(self.var.get())
            self.combobox.config(foreground="black")
            return True
        except ValueError as e:
            print(f"Invalid input for {self.element.key}: {e}")
            self.combobox.config(foreground="red")
            return False

class IntegerElementWidget(ElementWidget):
    def __init__(self, parent: tk.Misc, element: IntegerElement):
        super().__init__(parent)
        self.element = element

        self.label = ttk.Label(self, text=element.key)
        self.label.pack(side=tk.LEFT, padx=5, pady=5)

        self.var = tk.StringVar(value=str(element.get()))
        self.entry = ttk.Entry(self, textvariable=self.var)
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, pady=5)
        vcmd = (self.register(self.validate_input), '%P')
        self.entry.config(validate="key", validatecommand=vcmd)

    def validate_input(self, P: str) -> bool:
        if P == "":
            return True
        try:
            int(P)
            return True
        except ValueError:
            return False
    
    def confirm(self) -> bool:
        try:
            self.element.from_string(self.var.get())
            self.entry.config(foreground="black")
            return True
        except ValueError as e:
            print(f"Invalid input for {self.element.key}: {e}")
            self.entry.config(foreground="red")
            return False

class FloatElementWidget(ElementWidget):
    def __init__(self, parent: tk.Misc, element: FloatElement):
        super().__init__(parent)
        self.element = element

        self.label = ttk.Label(self, text=element.key)
        self.label.pack(side=tk.LEFT, padx=5, pady=5)

        self.var = tk.StringVar(value=str(element.get()))
        self.entry = ttk.Entry(self, textvariable=self.var)
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, pady=5)
        vcmd = (self.register(self.validate_input), '%P')
        self.entry.config(validate="key", validatecommand=vcmd)
        
    
    def validate_input(self, P: str) -> bool:
        if P == "" or P == "." or P == "-":
            return True
        try:
            float(P)
            return True
        except ValueError:
            return False

    
    def confirm(self) -> bool:
        try:
            self.element.from_string(self.var.get())
            self.entry.config(foreground="black")
            return True
        except ValueError as e:
            print(f"Invalid input for {self.element.key}: {e}")
            self.entry.config(foreground="red")
            return False

class ColorElementWidget(ElementWidget):
    def __init__(self, parent: tk.Misc, element: ColorElement):
        super().__init__(parent)
        self.element = element

        self.label = ttk.Label(self, text=element.key)
        self.label.pack(side=tk.LEFT, padx=5, pady=5)

        self.var = tk.StringVar(value=element.get())
        self.entry = ttk.Entry(self, textvariable=self.var, state="readonly")
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, pady=5)

        self.button = ttk.Button(self, text="Choose...", command=self.choose_color)
        self.button.pack(side=tk.LEFT, padx=5, pady=5)

    def choose_color(self):
        color_code = colorchooser.askcolor(title ="Choose color", initialcolor=self.var.get())
        if color_code and color_code[1]:
            self.var.set(color_code[1])
            self.entry.config(foreground="black")

    def confirm(self) -> bool:
        try:
            self.element.set(self.var.get())
            self.entry.config(foreground="black")
            return True
        except ValueError as e:
            print(f"Invalid input for {self.element.key}: {e}")
            self.entry.config(foreground="red")
            return False

class PathElementWidget(ABC, ElementWidget):
    def __init__(self, parent: tk.Misc, element: PathElement):
        super().__init__(parent)
        self.element = element

        self.label = ttk.Label(self, text=element.key)
        self.label.pack(side=tk.LEFT, padx=5, pady=5)

        self.var = tk.StringVar(value=element.get())
        self.entry = ttk.Entry(self, textvariable=self.var, state="readonly")
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, pady=5)
        
        self.button = ttk.Button(self, text="Browse...", command=self.browse_path)
        self.button.pack(side=tk.LEFT, padx=5, pady=5)
    
    @abstractmethod
    def browse_path(self): ...

    def confirm(self) -> bool:
        try:
            self.element.set(self.var.get())
            self.entry.config(foreground="black")
            return True
        except ValueError as e:
            print(f"Invalid input for {self.element.key}: {e}")
            self.entry.config(foreground="red")
            return False

class FilePathElementWidget(PathElementWidget):
    def browse_path(self):
        file_path = filedialog.askopenfilename(title="Select File", initialfile=self.var.get())
        if file_path:
            self.var.set(file_path)
            self.entry.config(foreground="black")

class DirectoryPathElementWidget(PathElementWidget):
    def browse_path(self):
        dir_path = filedialog.askdirectory(title="Select Directory", initialdir=self.var.get())
        if dir_path:
            self.var.set(dir_path)
            self.entry.config(foreground="black")


def get_all_subclasses(cls : type) -> list[type]:
    subclasses = []
    for subclass in cls.__subclasses__():
        subclasses.append(subclass)
        subclasses.extend(get_all_subclasses(subclass))
    return subclasses

def get_widget_for_element(element : EditableElement) -> type[ElementWidget]|None:
    for cls in get_all_subclasses(ElementWidget):
        if cls.__name__ == f"{element.__class__.__name__}Widget":
            return cls
    return None


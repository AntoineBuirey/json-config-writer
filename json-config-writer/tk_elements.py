import tkinter as tk
import tkinter.ttk as ttk
from tkinter import colorchooser, filedialog
from abc import ABC, abstractmethod

from elements import (TextElement, BooleanElement, ChoiceElement, EditableElement,
                       IntegerElement, FloatElement, ColorElement, PathElement,
                       ListElement, EditableElement, BaseElement, SubCategoryElement)


class ElementWidget(ttk.Frame, ABC):
    def __init__(self, parent: tk.Misc, element: BaseElement, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.__element = element
    
    @property
    def element(self) -> BaseElement:
        return self.__element

    @abstractmethod
    def confirm(self) -> bool: ...

class EditableElementWidget(ElementWidget, ABC):
    def __init__(self, parent: tk.Misc, element: EditableElement, *args, **kwargs):
        super().__init__(parent, element, *args, **kwargs)
        self.__element = element

    @property
    def element(self) -> EditableElement:
        return self.__element


class TextElementWidget(EditableElementWidget):
    def __init__(self, parent: tk.Misc, element: TextElement):
        super().__init__(parent, element)

        self.label = ttk.Label(self, text=element.name)
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
            print(f"Invalid input for {self.element.tag}: {e}")
            self.entry.config(foreground="red")
            return False

class BooleanElementWidget(EditableElementWidget):
    def __init__(self, parent: tk.Misc, element: BooleanElement):
        super().__init__(parent, element)

        self.var = tk.BooleanVar(value=element.get())
        self.checkbutton = ttk.Checkbutton(self, text=element.name, variable=self.var)
        self.checkbutton.pack(side=tk.LEFT, padx=5, pady=5)

    
    def confirm(self) -> bool:
        try:
            self.element.set(self.var.get())
            return True
        except ValueError as e:
            print(f"Invalid input for {self.element.tag}: {e}")
            return False

class ChoiceElementWidget(EditableElementWidget):
    def __init__(self, parent: tk.Misc, element: ChoiceElement):
        super().__init__(parent, element)

        self.label = ttk.Label(self, text=element.name)
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
            print(f"Invalid input for {self.element.tag}: {e}")
            self.combobox.config(foreground="red")
            return False

class IntegerElementWidget(EditableElementWidget):
    def __init__(self, parent: tk.Misc, element: IntegerElement):
        super().__init__(parent, element)

        self.label = ttk.Label(self, text=element.name)
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
            print(f"Invalid input for {self.element.tag}: {e}")
            self.entry.config(foreground="red")
            return False

class FloatElementWidget(EditableElementWidget):
    def __init__(self, parent: tk.Misc, element: FloatElement):
        super().__init__(parent, element)

        self.label = ttk.Label(self, text=element.name)
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
            print(f"Invalid input for {self.element.tag}: {e}")
            self.entry.config(foreground="red")
            return False

class ColorElementWidget(EditableElementWidget):
    def __init__(self, parent: tk.Misc, element: ColorElement):
        super().__init__(parent, element)

        self.label = ttk.Label(self, text=element.name)
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
            print(f"Invalid input for {self.element.tag}: {e}")
            self.entry.config(foreground="red")
            return False

class PathElementWidget(EditableElementWidget, ABC):
    def __init__(self, parent: tk.Misc, element: PathElement):
        super().__init__(parent, element)

        self.label = ttk.Label(self, text=element.name)
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
            print(f"Invalid input for {self.element.tag}: {e}")
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

class ListElementWidget(EditableElementWidget):
    """
    name of the list, then a entry field to add a new item, then a button to add it to the list
    below a listbox showing the current items, with a button next to each item to remove it
    """
    def __init__(self, parent: tk.Misc, element: ListElement):
        super().__init__(parent, element)

        self.label = ttk.Label(self, text=element.name)
        self.label.pack(side=tk.TOP, anchor="w", padx=5, pady=5)
        
        self.frame = ttk.Frame(self)
        self.frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        self.var = tk.StringVar()
        self.entry = ttk.Entry(self.frame, textvariable=self.var)
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, pady=5)
        self.add_button = ttk.Button(self.frame, text="Add", command=self.add_item)
        self.add_button.pack(side=tk.LEFT, padx=5, pady=5)
        
        self.listbox = tk.Listbox(self, height=5)
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.listbox.yview)
        self.scrollbar.pack(side=tk.LEFT, fill=tk.Y)
        self.listbox.config(yscrollcommand=self.scrollbar.set)
        for item in element.get():
            self.listbox.insert(tk.END, str(item))
        self.remove_button = ttk.Button(self, text="Remove Selected", command=self.remove_selected)
        self.remove_button.pack(side=tk.LEFT, padx=5, pady=5)
        
    def add_item(self):
        item = self.var.get().strip()
        if item and item not in self.listbox.get(0, tk.END):
            self.listbox.insert(tk.END, item)
            self.var.set("")
            self.entry.config(foreground="black")
        elif item in self.listbox.get(0, tk.END):
            print(f"Item '{item}' already in the list.")
            self.entry.config(foreground="red")
        else:
            self.entry.config(foreground="red")
    
    def remove_selected(self):
        selected_indices = self.listbox.curselection()
        for index in reversed(selected_indices):
            self.listbox.delete(index)
    
    def confirm(self) -> bool:
        try:
            items = list(self.listbox.get(0, tk.END))
            self.element.set(items)
            self.listbox.config(foreground="black")
            return True
        except ValueError as e:
            print(f"Invalid input for {self.element.tag}: {e}")
            self.listbox.config(foreground="red")
            return False


class SubCategoryElementWidget(ElementWidget):
    def __init__(self, parent: tk.Misc, element: SubCategoryElement):
        super().__init__(parent, element)
        self.label = ttk.Label(self, text=element.name, font=("TkDefaultFont", 10, "bold"))
        self.label.pack(side=tk.TOP, anchor="w", padx=5, pady=5)
        self.frame = ttk.Frame(self)
        self.frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.sub_widgets: list[ElementWidget] = []
        for sub_element in element.get_elements():
            widget_class = get_widget_for_element(sub_element)
            widget = widget_class(self.frame, sub_element)
            widget.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
            self.sub_widgets.append(widget)

    def confirm(self) -> bool:
        all_valid = True
        for widget in self.sub_widgets:
            if hasattr(widget, "confirm") and not widget.confirm():
                all_valid = False
        return all_valid


def get_all_subclasses(cls : type) -> list[type]:
    subclasses = []
    for subclass in cls.__subclasses__():
        subclasses.append(subclass)
        subclasses.extend(get_all_subclasses(subclass))
    return subclasses

def get_widget_for_element(element : BaseElement) -> type[ElementWidget]:
    for cls in get_all_subclasses(ElementWidget):
        if cls.__name__ == f"{element.__class__.__name__}Widget":
            return cls
    raise ValueError(f"No widget found for element type {element.__class__.__name__}")

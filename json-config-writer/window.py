import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog
import sv_ttk
from enum import StrEnum
from typing import Literal
import sys
import darkdetect
if sys.platform == "win32":
    import pywinstyles
from xml_config_reader import read_config
from tk_elements import ElementWidget, get_widget_for_element

class COLORS(StrEnum):
    LIGHT_BACKGROUND = "#fafafa"
    DARK_BACKGROUND = "#2b2b2b"
    LIGHT_FOREGROUND = "#000000"
    DARK_FOREGROUND = "#ffffff"

def apply_theme_to_titlebar(root, theme : Literal["Light", "Dark"]):
    if sys.platform != "win32":
        return
    version = sys.getwindowsversion()

    if version.major == 11:
        # Set the title bar color to the background color on Windows 11 for better appearance
        pywinstyles.change_header_color(root, COLORS.DARK_BACKGROUND if theme == "Dark" else COLORS.LIGHT_BACKGROUND)
    elif version.major == 10:
        pywinstyles.apply_style(root, "dark" if theme == "Dark" else "normal")

        # A hacky way to update the title bar's color on Windows 10 (it doesn't update instantly like on Windows 11)
        root.wm_attributes("-alpha", 0.99)
        root.wm_attributes("-alpha", 1)

def apply_theme_to_background(root, theme : Literal["Light", "Dark"]):
    bg_color = COLORS.DARK_BACKGROUND if theme == "Dark" else COLORS.LIGHT_BACKGROUND
    fg_color = COLORS.DARK_FOREGROUND if theme == "Dark" else COLORS.LIGHT_FOREGROUND
    root.configure(bg=bg_color)
    
    # Configure ttk styles for better theme consistency
    style = ttk.Style()
    style.configure('TFrame', background=bg_color)
    style.configure('TLabel', background=bg_color, foreground=fg_color)

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Configuration Editor")
        theme : Literal['Light', "Dark"] = darkdetect.theme()
        print(f"Detected theme: {theme}")
        sv_ttk.set_theme(theme.lower(), self)
        apply_theme_to_titlebar(self, theme)
        apply_theme_to_background(self, theme)
        elements = read_config(self.select_config_xml())

        self.widgets : list[ElementWidget] = []
        for elem in elements:
            WidgetClass = get_widget_for_element(elem)
            if WidgetClass is None:
                print(f"No widget found for element type: {elem.__class__.__name__}")
                continue
            widget = WidgetClass(self, elem)
            widget.pack(fill=tk.X, padx=10, pady=5)
            self.widgets.append(widget)

        confirm_button = ttk.Button(self, text="Confirm", command=self.on_confirm)
        confirm_button.pack(pady=10)

    def select_config_xml(self):
        file_path = filedialog.askopenfilename(title="Select config.xml", filetypes=[("XML files", "*.xml")])
        return file_path or None

    def on_confirm(self):
        all_valid = all(widget.confirm() for widget in self.widgets)
        if all_valid:
            print("All values are valid:")
            for widget in self.widgets:
                elem = widget.element
                print(f"  {elem.key}: {elem.get()}")
        else:
            print("Some values are invalid. Please correct them.")

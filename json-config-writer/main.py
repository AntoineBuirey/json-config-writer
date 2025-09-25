import tkinter as tk
import tkinter.ttk as ttk

from xml_config_reader import read_config
from tk_elements import ElementWidget, get_widget_for_element


root = tk.Tk()
root.title("Configuration Editor")

elements = read_config("json-config-writer/config.xml")

widgets : list[ElementWidget] = []
for elem in elements:
    WidgetClass = get_widget_for_element(elem)
    if WidgetClass is None:
        print(f"No widget found for element type: {elem.__class__.__name__}")
        continue
    widget = WidgetClass(root, elem)
    widget.pack(fill=tk.X, padx=10, pady=5)
    widgets.append(widget)

def on_confirm():
    all_valid = all(widget.confirm() for widget in widgets)
    if all_valid:
        print("All values are valid:")
        for elem in elements:
            print(f"  {elem.key}: {elem.get()}")
    else:
        print("Some values are invalid. Please correct them.")

confirm_button = ttk.Button(root, text="Confirm", command=on_confirm)
confirm_button.pack(pady=10)

root.mainloop()
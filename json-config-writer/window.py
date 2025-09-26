import tkinter as tk
import tkinter.ttk as ttk
import sv_ttk
import sys
import darkdetect
if sys.platform == "win32":
    import pywinstyles
from xml_config_reader import read_config
from tk_elements import ElementWidget, get_widget_for_element


def apply_theme_to_titlebar(root):
    if sys.platform != "win32":
        return
    version = sys.getwindowsversion()

    if version.major == 10 and version.build >= 22000:
        # Set the title bar color to the background color on Windows 11 for better appearance
        pywinstyles.change_header_color(root, "#1c1c1c" if sv_ttk.get_theme() == "dark" else "#fafafa")
    elif version.major == 10:
        pywinstyles.apply_style(root, "dark" if sv_ttk.get_theme() == "dark" else "normal")

        # A hacky way to update the title bar's color on Windows 10 (it doesn't update instantly like on Windows 11)
        root.wm_attributes("-alpha", 0.99)
        root.wm_attributes("-alpha", 1)

# Example usage (replace `root` with the reference to your main/Toplevel window)

def main():
    root = tk.Tk()
    root.title("Configuration Editor")

    sv_ttk.set_theme(darkdetect.theme())
    apply_theme_to_titlebar(root)

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

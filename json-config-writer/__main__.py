from window import MainWindow
import traceback

if __name__ == "__main__":
    try:
        app = MainWindow()
        app.mainloop()
    except Exception as e:
        print(f"Error: {e}")
        traceback.print_exc()

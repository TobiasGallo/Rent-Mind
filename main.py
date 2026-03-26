import sys
from ui.main_window import MainWindow

def main():
    try:
        app = MainWindow()
        app.run()
    except Exception as e:
        print(f"Error fatal: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
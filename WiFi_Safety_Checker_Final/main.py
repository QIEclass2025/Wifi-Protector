# main.py
import sys
import platform
from PyQt6.QtWidgets import QApplication
from data.database import init_db

def main():
    """
    Initializes the database and runs the platform-specific application.
    """
    # Initialize the database
    init_db()

    # Create the PyQt6 application
    pyqt_app = QApplication(sys.argv)

    # Import and run the appropriate app version based on the OS
    os_name = platform.system()
    
    if os_name == "Windows":
        from gui.app_windows import App
        print("Running Windows version")
    elif os_name == "Darwin":
        from gui.app import App
        print("Running macOS version")
    else:
        print(f"Unsupported OS: {os_name}", file=sys.stderr)
        # Fallback to the default app, might not be fully functional
        from gui.app import App
        print("Falling back to default version", file=sys.stderr)

    window = App()
    window.show()
    sys.exit(pyqt_app.exec())

if __name__ == "__main__":
    main()

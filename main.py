import sys
from main_application import create_application
from main_window import MainWindow
from config import Version


app_title = f"Binance现货交易系统_new {Version}"

if __name__ == "__main__":
    app = create_application(app_title)
    main_window = MainWindow(app_title)
    main_window.show()
    sys.exit(app.exec())
    
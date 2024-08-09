import sys
from main_application import create_application
from main_window import MainWindow
from app_engine import AppEngine
from config import Version


_app_title = f"Binance现货交易系统 {Version}"

if __name__ == "__main__":
    app = create_application(_app_title)
    app_engine = AppEngine()
    main_window = MainWindow(_app_title, app_engine)
    main_window.show()
    sys.exit(app.exec())

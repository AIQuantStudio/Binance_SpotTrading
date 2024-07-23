import sys
import asyncio
from main_application import create_application
from main_window import MainWindow

VERSION = "v1.0"


if __name__ == '__main__':
    app_title = f"Binance现货交易系统 {VERSION}"
    app = create_application(app_title)
    main_window = MainWindow(app_title)
    main_window.show()
    sys.exit(app.exec())

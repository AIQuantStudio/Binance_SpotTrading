from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *

from exchange.binance_canvas import BinanceCanvas
from exchange.binance_market import BinanceMarket
from model import ModelFactory
from event import EVENT_TIMER, EVENT_PREDICT


class ModelPanel(QFrame):

    def __init__(self, parent_widget, top_dock, app_engine):
        super().__init__(parent_widget)

        self.top_dock = top_dock
        self.app_engine = app_engine
        
        self.setup_ui()
        self.bind_event()
        
        self.show_symbol()
        self.show_config_info()
        self.show_kline()
        
        self.app_engine.event_engine.register_timer(self.refresh_kline, 1)

    def setup_ui(self):
        main_hbox_layout = QHBoxLayout()
        self.setLayout(main_hbox_layout)

        main_left_widget = QWidget()
        main_hbox_layout.addWidget(main_left_widget, stretch=3)

        main_right_widget = QWidget()
        main_hbox_layout.addWidget(main_right_widget, stretch=10)

        self.setup_left_area_ui(main_left_widget)
        self.setup_right_area_ui(main_right_widget)

    def setup_left_area_ui(self, left_widget):
        vbox_layout = QVBoxLayout()

        self.symbol_label = QLabel("")
        vbox_layout.addWidget(self.symbol_label)

        config_info_label = QLabel("配置信息：")
        vbox_layout.addWidget(config_info_label)

        self.config_info_textbrowser = QTextBrowser()
        self.config_info_textbrowser.setFont(QFont("Courier New"))
        vbox_layout.addWidget(self.config_info_textbrowser)

        self.gpu_checkbox = QCheckBox()
        self.gpu_checkbox.setText("GPU")
        self.gpu_checkbox.setCheckState(Qt.CheckState.Checked)
        if not ModelFactory().cuda_is_available():
            self.gpu_checkbox.setCheckState(Qt.CheckState.Unchecked)
            self.gpu_checkbox.setDisabled(True)
        vbox_layout.addWidget(self.gpu_checkbox)
        
        hbox_layout = QHBoxLayout()
        self.start_prediction_btn = QPushButton()
        self.start_prediction_btn.setText("启动预测")
        hbox_layout.addWidget(self.start_prediction_btn)
        self.stop_prediction_btn = QPushButton()
        self.stop_prediction_btn.setText("停止预测")
        self.stop_prediction_btn.setDisabled(True)
        hbox_layout.addWidget(self.stop_prediction_btn)
        vbox_layout.addLayout(hbox_layout)
        
        left_widget.setLayout(vbox_layout)

    def setup_right_area_ui(self, right_widget):
        vbox_layout = QVBoxLayout()
        right_widget.setLayout(vbox_layout)

        self.binance_kline_penal = QFrame(right_widget)
        self.binance_kline_penal.setLineWidth(1)
        self.binance_kline_penal.setMidLineWidth(1)
        self.binance_kline_penal.setFrameStyle(QFrame.Shape.Panel | QFrame.Shadow.Raised)
        
        vbox_layout.addWidget(self.binance_kline_penal)
    
    def bind_event(self):
        self.gpu_checkbox.stateChanged.connect(self.gpu_changed)
        self.start_prediction_btn.clicked.connect(self.start_predict)
        self.stop_prediction_btn.clicked.connect(self.stop_predict)
        
    def start_predict(self):
        self.start_prediction_btn.setDisabled(True)
        self.stop_prediction_btn.setEnabled(True)

        self.app_engine.event_engine.register_timer(self.predict, once = True)
        
        
    def stop_predict(self):
        self.start_prediction_btn.setEnabled(True)
        self.stop_prediction_btn.setDisabled(True)

        
    def show_symbol(self):
        model = ModelFactory().get_model(self.top_dock.id)
        self.symbol_label.setText(model.symbol)
        title = self.top_dock.windowTitle()
        title += " " + model.symbol
        self.top_dock.setWindowTitle(title)
    
    def show_config_info(self):
        model = ModelFactory().get_model(self.top_dock.id)
        config = model.get_config()
        if config is not None:
            s = ""
            max_len = 0
            for key in config.keys():
                if len(key) > max_len:
                    max_len = len(key)
            for key, value in config.items():
                s = s + f"{key:<{max_len+1}}: {value}\n"

            self.config_info_textbrowser.setText(s)
    
    def show_kline(self):
        layout = QVBoxLayout()
        self.binance_kline_penal.setLayout(layout)
        
        self.figure_canvas = BinanceCanvas()
        layout.addWidget(self.figure_canvas)
        
    def gpu_changed(self):
        model = ModelFactory().get_model(self.top_dock.id)
        model
    def refresh_kline(self):
        model = ModelFactory().get_model(self.top_dock.id)
        data = BinanceMarket().get_klines(f"{model.base_currency}{model.quote_currency}")
        self.figure_canvas.plot_data(data)
        
    def predict(self):
        model = ModelFactory().get_model(self.top_dock.id)
        data = BinanceMarket().get_klines(f"{model.base_currency}{model.quote_currency}")
        dataloader = ModelFactory().create_dataloader(self.top_dock.id, data)
        price = model.predict(dataloader)
        print(price)
        
    def close(self):
        self.app_engine.event_engine.unregister_timer(self.refresh_kline)
        return super().close()
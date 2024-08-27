from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *

from config import Config
from main_engine import MainEngine
from model import ModelFactory
from event import Event, EVENT_PREDICT

from widget.log_monitor import LogMonitor
from widget.market_canvas import MarketCanvas
from exchange.binance_market import BinanceMarket


class ModelPanel(QFrame):

    def __init__(self, parent_widget, top_dock):
        super().__init__(parent_widget)

        self.top_dock = top_dock

        self.setup_ui()
        self.bind_event()

        self.show_model_info()
        self.show_market()

        # self.app_engine.event_engine.register_timer(self.refresh_kline, 1)

    def setup_ui(self):
        main_hbox_layout = QHBoxLayout()
        main_hbox_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(main_hbox_layout)

        main_left_widget = QWidget()
        main_hbox_layout.addWidget(main_left_widget, stretch=3)

        main_right_widget = QWidget()
        main_hbox_layout.addWidget(main_right_widget, stretch=10)

        self.setup_left_area_ui(main_left_widget)
        self.setup_right_area_ui(main_right_widget)

    def setup_left_area_ui(self, left_widget: QWidget):
        vbox_layout = QVBoxLayout()

        config_info_label = QLabel("配置信息")
        vbox_layout.addWidget(config_info_label)

        self.config_info_textbrowser = QTextBrowser()
        self.config_info_textbrowser.setFont(QFont("Courier New", 11))
        self.config_info_textbrowser.setMaximumHeight(200)
        vbox_layout.addWidget(self.config_info_textbrowser)

        vertical_sep_line = QFrame(left_widget)
        vertical_sep_line.setLineWidth(8)
        vertical_sep_line.setFrameShape(QFrame.Shape.HLine)
        vertical_sep_line.setFrameShadow(QFrame.Shadow.Sunken)
        vbox_layout.addWidget(vertical_sep_line)

        # prediction_record_label = QLabel("预测记录")
        # vbox_layout.addWidget(prediction_record_label)

        # self.predict_price_table = PredictPriceTable(self, self.top_dock, self.app_engine)
        # vbox_layout.addWidget(self.predict_price_table)

        # log_monitor_label = QLabel("日志")
        # vbox_layout.addWidget(log_monitor_label)

        self.log_monitor = LogMonitor(self, self.top_dock)
        vbox_layout.addWidget(self.log_monitor)

        # hbox_layout = QHBoxLayout()
        # hbox_layout.setContentsMargins(0, 0, 0, 0)

        # self.gpu_checkbox = QCheckBox()
        # self.gpu_checkbox.setText("GPU")
        # self.gpu_checkbox.setCheckState(Qt.CheckState.Checked)
        # if not ModelFactory().cuda_is_available():
        #     self.gpu_checkbox.setCheckState(Qt.CheckState.Unchecked)
        #     self.gpu_checkbox.setDisabled(True)
        # hbox_layout.addWidget(self.gpu_checkbox)

        # label1 = QLabel()
        # label1.setText("预测间隔时间")
        # self.predict_interval_edit = QLineEdit()
        # self.predict_interval_edit.setValidator(QIntValidator())
        # self.predict_interval_edit.setText(str(Config.get("model.predict_interval", 60)))
        # label2 = QLabel()
        # label2.setText("秒")

        # hbox_layout.addSpacing(80)
        # hbox_layout.addWidget(label1)
        # hbox_layout.addWidget(self.predict_interval_edit)
        # hbox_layout.addWidget(label2)
        # vbox_layout.addLayout(hbox_layout)

        # hbox_layout = QHBoxLayout()
        # self.start_prediction_btn = QPushButton()
        # self.start_prediction_btn.setText("启动预测")
        # hbox_layout.addWidget(self.start_prediction_btn)
        # self.stop_prediction_btn = QPushButton()
        # self.stop_prediction_btn.setText("停止预测")
        # self.stop_prediction_btn.setDisabled(True)
        # hbox_layout.addWidget(self.stop_prediction_btn)
        # vbox_layout.addLayout(hbox_layout)

        left_widget.setLayout(vbox_layout)

    def setup_right_area_ui(self, right_widget):
        vbox_layout = QVBoxLayout()
        right_widget.setLayout(vbox_layout)

        self.market_canvas = MarketCanvas(self, self.top_dock)
        vbox_layout.addWidget(self.market_canvas)

    def bind_event(self):
        pass
        # self.start_prediction_btn.clicked.connect(self.on_start_predict)
        # self.stop_prediction_btn.clicked.connect(self.on_stop_predict)

    def show_model_info(self):
        config = ModelFactory().get_config_dict(self.top_dock.id)
        if config is not None:
            s = ""
            max_len = 0
            for key in config.keys():
                if len(key) > max_len:
                    max_len = len(key)
            for key, value in config.items():
                s = s + f"{key:<{max_len+1}}: {value}\n"

            self.config_info_textbrowser.setText(s)

    def show_market(self):
        self.market_canvas.start_market()

    # def refresh_kline(self):
    #     model = ModelFactory().get_model(self.top_dock.id)
    #     data = BinanceMarket().get_klines(f"{model.base_currency}{model.quote_currency}")
    #     self.figure_canvas.plot_data(data)

    # def on_gpu_changed(self):
    #     model = ModelFactory().get_model(self.top_dock.id)

    def on_start_predict(self):
        self.start_prediction_btn.setDisabled(True)
        self.stop_prediction_btn.setEnabled(True)

        interval = int(self.predict_interval_edit.text())
        MainEngine.event_engine.register_timer(self.predict, interval=interval)

    def on_stop_predict(self):
        pass
        # self.start_prediction_btn.setEnabled(True)
        # self.stop_prediction_btn.setDisabled(True)

        MainEngine.event_engine.unregister_timer(self.predict)

    def predict(self):
        predict_price = ModelFactory().predict(self.top_dock.id, gpu=self.gpu_checkbox.checkState() == Qt.CheckState.Checked)

        print(predict_price[0][0])
        self.market_canvas.set_predict_price(predict_price[0][0])
        # self.app_engine.event_engine.put(Event(EVENT_PREDICT, price, self.top_dock.id))
        # self.figure_canvas.set_predict_price(price[0][0])
        # self.refresh_kline()

    def close(self):
        # self.app_engine.event_engine.unregister_timer(self.refresh_kline)
        # self.on_stop_predict()
        self.market_canvas.stop_market()
        self.log_monitor.close()
        return super().close()

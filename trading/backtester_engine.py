

class BacktesterEngine:
    
    def __init__(self):
        self._history_data = []
    
    def clear_data(self):
        self._result_df = None
        self._result_statistics = None
        self._result_values = None

        self.strategy = None
        self.tick = None
        self.bar = None
        self.datetime = None

        self.stop_order_count = 0
        self.stop_orders.clear()
        self.active_stop_orders.clear()

        self.limit_order_count = 0
        self.limit_orders.clear()
        self.active_limit_orders.clear()

        self.trade_count = 0
        self.trades.clear()

        self.logs.clear()
        self.daily_results.clear()

    def load_history_data(self):
        # self.write_log("开始加载历史数据")

        if not self._end:
            self._end = datetime.now()

        if self._start >= self._end:
            self.write_log("起始日期必须小于结束日期")
            return

        self._history_data.clear()

        progress_delta = None
        interval_delta = None
        if self._interval == Interval.MINUTE:
            progress_delta = timedelta(hours=4)
            interval_delta = timedelta(minutes=1)
        elif self._interval == Interval.HOUR:
            progress_delta = timedelta(days=4)
            interval_delta = timedelta(hours=1)
        elif self._interval == Interval.DAILY:
            progress_delta = timedelta(days=60)
            interval_delta = timedelta(days=1)

        if progress_delta is None or interval_delta is None:
            self.write_log(f"K线周期设定错误 interval({self._interval})")
            return

        total_delta = self._end - self._start
        start = self._start
        end = self._start + progress_delta
        progress = 0

        while start < self._end:
            end = min(end, self._end)  # 确保结束时间在设定的范围内


            data = load_bar_data(self.symbol, self.exchange, self._interval, start, end)


            self._history_data.extend(data)

            progress += progress_delta / total_delta
            progress = min(progress, 1)
            progress_bar = "#" * int(progress * 10)
            self.write_log(f"加载进度：{progress_bar} [{progress:.0%}]")

            start = end + interval_delta
            end += (progress_delta + interval_delta)

        self.write_log(f"历史数据加载完成，数据量：{len(self._history_data)}")
        
    
    def run_backtesting(self):
        self.strategy.on_init()

        count = 0
        ix = 0
        # 用历史数据预加载
        for ix, data in enumerate(self._history_data):
            if count >= self._preload_count:
                break

            count += 1
            self.datetime = data.datetime

            try:
                self._preload_callback(data)
            except Exception:
                self.write_log("触发异常，回测终止")
                self.write_log(traceback.format_exc())
                return

        self.strategy.inited = True
        self.write_log("策略初始化完成")

        self.strategy.on_start()
        self.strategy.trading = True
        self.write_log("开始回放历史数据")

        # 使用剩余的历史数据来运行回测
        for data in self._history_data[ix:]:
            try:
                self._new_bar(data)
            except Exception:
                self.write_log("触发异常，回测终止")
                self.write_log(traceback.format_exc())
                return

        self.write_log("历史数据回放结束")

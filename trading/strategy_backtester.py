from collections import defaultdict
from datetime import date, datetime, timedelta
from typing import Callable, Type
from itertools import product
from functools import lru_cache
from time import time
import multiprocessing
import random
import traceback
from PyQt5 import QtCore, QtWidgets

import numpy as np
from pandas import DataFrame
import plotly.graph_objects as go
from plotly.subplots import make_subplots
# from deap import creator, base, tools, algorithms

from harvester.strategies import BaseStrategy, StrategyEngine
from harvester.constant import INTERVAL_DELTA_MAP, STOPORDER_PREFIX
from harvester.enumeration import Direction, Offset, Exchange, Interval, Status, AppEngineMode, BacktestingMode, StopOrderStatus
from harvester.database import database_manager
from harvester.structure import OrderData, TradeData, BarData, TickData, StoporderData
from harvester.common import Utils


from .optimization_setting import OptimizationSetting


# Set deap algo
# creator.create("FitnessMax", base.Fitness, weights=(1.0,))
# creator.create("Individual", list, fitness=creator.FitnessMax)


class StrategyBacktester(StrategyInterface):

    engine_mode = AppEngineMode.BACKTESTING
    gateway_name = "BACKTESTING"

    def __init__(self, class_name: str, strategy_class: Type[BaseStrategy], setting: dict, signal_log: QtCore.pyqtSignal = None):
        """"""
        self._signal_log: QtCore.pyqtSignal = signal_log

        self._strategy_class_name: str = class_name
        self._strategy_class: Type[BaseStrategy] = strategy_class
        self._strategy_name: str = strategy_class.name
        self._strategy_parameter: dict = None

        self._vt_symbol = setting.get("vt_symbol")
        self._interval = setting.get("interval")
        self._start = setting.get("start")
        self._end = setting.get("end")
        self._rate = setting.get("rate")
        self._slippage = setting.get("slippage")
        self._size = setting.get("size")
        self._pricetick = setting.get("pricetick")
        self._capital = setting.get("capital")
        self._inverse = setting.get("inverse")
        self._type = BacktestingMode.BAR

        self._history_data = []

        self.strategy_class = None
        self.strategy = None
        self.tick: TickData
        self.bar: BarData
        self.datetime = None

        self._preload_count = 0
        self._preload_interval = None
        self._preload_callback = None
        
        self.stop_order_count = 0
        self.stop_orders = {}
        self.active_stop_orders = {}

        self.limit_order_count = 0
        self.limit_orders = {}
        self.active_limit_orders = {}

        self.trade_count = 0
        self.trades = {}

        self.logs = []

        self.daily_results = {}
        self.daily_df = None

        self._result_df = None
        self._result_statistics = None
        self._result_values = None
        
    def preload_bar(self, count: int, callback: Callable[[BarData], None], interval: Interval):
        """ 实现 StrategyInterface::preload_bar """
        self._preload_count = count
        self._pre_interval = interval
        self._preload_callback = callback

    @property
    def mode(self):
        return self.engine_mode

    def clear_data(self):
        """"""
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
        """"""
        self.write_log("开始加载历史数据")

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

            if self._type == BacktestingMode.BAR:
                data = load_bar_data(self.symbol, self.exchange, self._interval, start, end)
            else:
                data = load_tick_data(self.symbol, self.exchange, start, end)

            self._history_data.extend(data)

            progress += progress_delta / total_delta
            progress = min(progress, 1)
            progress_bar = "#" * int(progress * 10)
            self.write_log(f"加载进度：{progress_bar} [{progress:.0%}]")

            start = end + interval_delta
            end += (progress_delta + interval_delta)

        self.write_log(f"历史数据加载完成，数据量：{len(self._history_data)}")

    def write_log(self, msg: str):
        """ 实现 StrategyEngine::write_log """
        if self._signal_log:
            self._signal_log.emit(f"{self.datetime}\t{msg}")

    def set_parameters(
        self,
        vt_symbol: str,
        interval: Interval,
        start: datetime,
        rate: float,
        slippage: float,
        size: float,
        pricetick: float,
        capital: int = 0,
        end: datetime = None,
        mode: BacktestingMode = BacktestingMode.BAR,
        inverse: bool = False
    ):
        """"""
        self._type = mode
        self._vt_symbol = vt_symbol
        self._interval = Interval(interval)
        self._rate = rate
        self._slippage = slippage
        self._size = size
        self._pricetick = pricetick
        self._start = start

        self.symbol, self.exchange = Utils.extract_vt_symbol(self._vt_symbol)

        self._capital = capital
        self._end = end
        self._type = mode
        self._inverse = inverse

    def add_strategy(self, strategy_class: type, setting: dict):
        """"""
        self.strategy_class = strategy_class
        self.strategy = strategy_class(self, self._vt_symbol, setting)

    
    def run_backtesting(self):
        """"""
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

    def calculate_result(self):
        """"""
        self.write_log("开始计算逐日盯市盈亏")

        if not self.trades:
            self.write_log("成交记录为空，无法计算")
            return

        # 将交易数据添加到daily_result中
        for trade in self.trades.values():
            d = trade.datetime.date()
            daily_result = self.daily_results[d]
            daily_result.add_trade(trade)

        # 通过迭代计算每日结果
        pre_close = 0
        start_pos = 0
        for daily_result in self.daily_results.values():
            daily_result.calculate_pnl(pre_close, start_pos, self._size, self._rate, self._slippage, self._inverse)

            pre_close = daily_result.close_price
            start_pos = daily_result.end_pos

        # 生成Dataframe
        results = defaultdict(list)
        for daily_result in self.daily_results.values():
            for key, value in daily_result.__dict__.items():
                results[key].append(value)

        self.daily_df = DataFrame.from_dict(results).set_index("date")

        self.write_log("逐日盯市盈亏计算完成")
        return self.daily_df

    def calculate_statistics(self, df: DataFrame = None, output=True):
        """"""
        self.write_log("开始计算策略统计指标")

        if df is None:
            df = self.daily_df

        if df is None:
            # 如果没有交易，则将所有统计设置为0
            start_date = ""
            end_date = ""
            total_days = 0
            profit_days = 0
            loss_days = 0
            end_balance = 0
            max_drawdown = 0
            max_ddpercent = 0
            max_drawdown_duration = 0
            total_net_pnl = 0
            daily_net_pnl = 0
            total_commission = 0
            daily_commission = 0
            total_slippage = 0
            daily_slippage = 0
            total_turnover = 0
            daily_turnover = 0
            total_trade_count = 0
            daily_trade_count = 0
            total_return = 0
            annual_return = 0
            daily_return = 0
            return_std = 0
            sharpe_ratio = 0
            return_drawdown_ratio = 0
        else:
            # 计算与余额相关的时间序列数据
            df["balance"] = df["net_pnl"].cumsum() + self._capital
            df["return"] = np.log(df["balance"] / df["balance"].shift(1))
            df["return"].fillna(0)
            df["highlevel"] = (df["balance"].rolling(min_periods=1, window=len(df), center=False).max())
            df["drawdown"] = df["balance"] - df["highlevel"]
            df["ddpercent"] = df["drawdown"] / df["highlevel"] * 100

            # 计算统计值
            start_date = df.index[0]
            end_date = df.index[-1]

            total_days = len(df)
            profit_days = len(df[df["net_pnl"] > 0])
            loss_days = len(df[df["net_pnl"] < 0])

            end_balance = df["balance"].iloc[-1]
            max_drawdown = df["drawdown"].min()
            max_ddpercent = df["ddpercent"].min()
            max_drawdown_end = df["drawdown"].idxmin()

            if isinstance(max_drawdown_end, date):
                max_drawdown_start = df["balance"][:max_drawdown_end].idxmax()
                max_drawdown_duration = (max_drawdown_end - max_drawdown_start).days
            else:
                max_drawdown_duration = 0

            total_net_pnl = df["net_pnl"].sum()
            daily_net_pnl = total_net_pnl / total_days

            total_commission = df["commission"].sum()
            daily_commission = total_commission / total_days

            total_slippage = df["slippage"].sum()
            daily_slippage = total_slippage / total_days

            total_turnover = df["turnover"].sum()
            daily_turnover = total_turnover / total_days

            total_trade_count = df["trade_count"].sum()
            daily_trade_count = total_trade_count / total_days

            total_return = (end_balance / self._capital - 1) * 100
            annual_return = total_return / total_days * 240
            daily_return = df["return"].mean() * 100
            return_std = df["return"].std() * 100

            if return_std:
                sharpe_ratio = daily_return / return_std * np.sqrt(240)
            else:
                sharpe_ratio = 0

            return_drawdown_ratio = -total_return / max_ddpercent

        if output:
            self.write_log("-" * 30)
            self.write_log(f"首个交易日：\t{start_date}")
            self.write_log(f"最后交易日：\t{end_date}")

            self.write_log(f"总交易日：\t{total_days}")
            self.write_log(f"盈利交易日：\t{profit_days}")
            self.write_log(f"亏损交易日：\t{loss_days}")

            self.write_log(f"起始资金：\t{self._capital:,.2f}")
            self.write_log(f"结束资金：\t{end_balance:,.2f}")

            self.write_log(f"总收益率：\t{total_return:,.2f}%")
            self.write_log(f"年化收益：\t{annual_return:,.2f}%")
            self.write_log(f"最大回撤: \t{max_drawdown:,.2f}")
            self.write_log(f"百分比最大回撤: {max_ddpercent:,.2f}%")
            self.write_log(f"最长回撤天数: \t{max_drawdown_duration}")

            self.write_log(f"总盈亏：\t{total_net_pnl:,.2f}")
            self.write_log(f"总手续费：\t{total_commission:,.2f}")
            self.write_log(f"总滑点：\t{total_slippage:,.2f}")
            self.write_log(f"总成交金额：\t{total_turnover:,.2f}")
            self.write_log(f"总成交笔数：\t{total_trade_count}")

            self.write_log(f"日均盈亏：\t{daily_net_pnl:,.2f}")
            self.write_log(f"日均手续费：\t{daily_commission:,.2f}")
            self.write_log(f"日均滑点：\t{daily_slippage:,.2f}")
            self.write_log(f"日均成交金额：\t{daily_turnover:,.2f}")
            self.write_log(f"日均成交笔数：\t{daily_trade_count}")

            self.write_log(f"日均收益率：\t{daily_return:,.2f}%")
            self.write_log(f"收益标准差：\t{return_std:,.2f}%")
            self.write_log(f"Sharpe Ratio：\t{sharpe_ratio:,.2f}")
            self.write_log(f"收益回撤比：\t{return_drawdown_ratio:,.2f}")

        statistics = {
            "start_date": start_date,
            "end_date": end_date,
            "total_days": total_days,
            "profit_days": profit_days,
            "loss_days": loss_days,
            "capital": self._capital,
            "end_balance": end_balance,
            "max_drawdown": max_drawdown,
            "max_ddpercent": max_ddpercent,
            "max_drawdown_duration": max_drawdown_duration,
            "total_net_pnl": total_net_pnl,
            "daily_net_pnl": daily_net_pnl,
            "total_commission": total_commission,
            "daily_commission": daily_commission,
            "total_slippage": total_slippage,
            "daily_slippage": daily_slippage,
            "total_turnover": total_turnover,
            "daily_turnover": daily_turnover,
            "total_trade_count": total_trade_count,
            "daily_trade_count": daily_trade_count,
            "total_return": total_return,
            "annual_return": annual_return,
            "daily_return": daily_return,
            "return_std": return_std,
            "sharpe_ratio": sharpe_ratio,
            "return_drawdown_ratio": return_drawdown_ratio,
        }

        for key, value in statistics.items():
            if value in (np.inf, -np.inf):
                value = 0
            statistics[key] = np.nan_to_num(value)

        self.write_log("策略统计指标计算完成")
        return statistics

    def show_chart(self, df: DataFrame = None):
        """"""
        if df is None:
            df = self.daily_df

        if df is None:
            return

        fig = make_subplots(rows=4, cols=1, subplot_titles=["Balance", "Drawdown", "Daily Pnl", "Pnl Distribution"], vertical_spacing=0.06)

        balance_line = go.Scatter(x=df.index, y=df["balance"], mode="lines", name="Balance")
        drawdown_scatter = go.Scatter(x=df.index, y=df["drawdown"], fillcolor="red", fill='tozeroy', mode="lines", name="Drawdown")
        pnl_bar = go.Bar(y=df["net_pnl"], name="Daily Pnl")
        pnl_histogram = go.Histogram(x=df["net_pnl"], nbinsx=100, name="Days")

        fig.add_trace(balance_line, row=1, col=1)
        fig.add_trace(drawdown_scatter, row=2, col=1)
        fig.add_trace(pnl_bar, row=3, col=1)
        fig.add_trace(pnl_histogram, row=4, col=1)

        fig.update_layout(height=1000, width=1000)
        fig.show()

    def run_optimization(self, optimization_setting: OptimizationSetting, output=True):
        """"""
        settings = optimization_setting.generate_setting()
        target_name = optimization_setting.target_name

        if not settings:
            self.write_log("优化参数组合为空，请检查")
            return

        if not target_name:
            self.write_log("优化目标未设置，请检查")
            return

        # 使用多进程以不同的设置运行回测
        # 强制使用spawn方法创建新进程（而不是Linux上的fork）
        ctx = multiprocessing.get_context("spawn")
        pool = ctx.Pool(multiprocessing.cpu_count())

        results = []
        for setting in settings:
            result = (pool.apply_async(optimize, (
                target_name,
                self.strategy_class,
                setting,
                self._vt_symbol,
                self._interval,
                self._start,
                self._rate,
                self._slippage,
                self._size,
                self._pricetick,
                self._capital,
                self._end,
                self._type,
                self._inverse
            )))
            results.append(result)

        pool.close()
        pool.join()

        result_values = [result.get() for result in results]
        result_values.sort(reverse=True, key=lambda result: result[1])

        if output:
            for value in result_values:
                self.write_log(f"参数：{value[0]}, 目标：{value[1]}")

        return result_values

    # def run_ga_optimization(self, optimization_setting: OptimizationSetting, population_size=100, ngen_size=30, output=True):
    #     """"""
    #     settings = optimization_setting.generate_setting_ga()
    #     target_name = optimization_setting.target_name

    #     if not settings:
    #         self.write_log("优化参数组合为空，请检查")
    #         return

    #     if not target_name:
    #         self.write_log("优化目标未设置，请检查")
    #         return

    #     def generate_parameter():
    #         """"""
    #         return random.choice(settings)

    #     def mutate_individual(individual, indpb):
    #         """"""
    #         size = len(individual)
    #         paramlist = generate_parameter()
    #         for i in range(size):
    #             if random.random() < indpb:
    #                 individual[i] = paramlist[i]
    #         return individual,

    #     global ga_target_name
    #     global ga_strategy_class
    #     global ga_setting
    #     global ga_vt_symbol
    #     global ga_interval
    #     global ga_start
    #     global ga_rate
    #     global ga_slippage
    #     global ga_size
    #     global ga_pricetick
    #     global ga_capital
    #     global ga_end
    #     global ga_mode
    #     global ga_inverse

    #     ga_target_name = target_name
    #     ga_strategy_class = self.strategy_class
    #     ga_setting = settings[0]
    #     ga_vt_symbol = self._vt_symbol
    #     ga_interval = self._interval
    #     ga_start = self._start
    #     ga_rate = self._rate
    #     ga_slippage = self._slippage
    #     ga_size = self._size
    #     ga_pricetick = self._pricetick
    #     ga_capital = self._capital
    #     ga_end = self._end
    #     ga_mode = self._type
    #     ga_inverse = self._inverse

    #     toolbox = base.Toolbox()
    #     toolbox.register("individual", tools.initIterate, creator.Individual, generate_parameter)
    #     toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    #     toolbox.register("mate", tools.cxTwoPoint)
    #     toolbox.register("mutate", mutate_individual, indpb=1)
    #     toolbox.register("evaluate", ga_optimize)
    #     toolbox.register("select", tools.selNSGA2)

    #     total_size = len(settings)
    #     pop_size = population_size                      # number of individuals in each generation
    #     lambda_ = pop_size                              # number of children to produce at each generation
    #     mu = int(pop_size * 0.8)                        # number of individuals to select for the next generation

    #     cxpb = 0.95         # probability that an offspring is produced by crossover
    #     mutpb = 1 - cxpb    # probability that an offspring is produced by mutation
    #     ngen = ngen_size    # number of generation

    #     pop = toolbox.population(pop_size)
    #     hof = tools.ParetoFront()               # end result of pareto front

    #     stats = tools.Statistics(lambda ind: ind.fitness.values)
    #     np.set_printoptions(suppress=True)
    #     stats.register("mean", np.mean, axis=0)
    #     stats.register("std", np.std, axis=0)
    #     stats.register("min", np.min, axis=0)
    #     stats.register("max", np.max, axis=0)

    #     # Multiprocessing is not supported yet.
    #     # pool = multiprocessing.Pool(multiprocessing.cpu_count())
    #     # toolbox.register("map", pool.map)

    #     # Run ga optimization
    #     self.write_log(f"参数优化空间：{total_size}")
    #     self.write_log(f"每代族群总数：{pop_size}")
    #     self.write_log(f"优良筛选个数：{mu}")
    #     self.write_log(f"迭代次数：{ngen}")
    #     self.write_log(f"交叉概率：{cxpb:.0%}")
    #     self.write_log(f"突变概率：{mutpb:.0%}")

    #     start = time()

    #     algorithms.eaMuPlusLambda(pop, toolbox, mu, lambda_, cxpb, mutpb, ngen, stats, halloffame=hof)

    #     end = time()
    #     cost = int((end - start))

    #     self.write_log(f"遗传算法优化完成，耗时{cost}秒")

    #     # Return result list
    #     results = []

    #     for parameter_values in hof:
    #         setting = dict(parameter_values)
    #         target_value = ga_optimize(parameter_values)[0]
    #         results.append((setting, target_value, {}))

    #     return results

    def update_daily_close(self, price: float):
        """"""
        d = self.datetime.date()

        daily_result = self.daily_results.get(d, None)
        if daily_result:
            daily_result.close_price = price
        else:
            self.daily_results[d] = DailyResult(d, price)

    def _new_bar(self, bar: BarData):
        """"""
        self.bar = bar
        self.datetime = bar.datetime

        self.cross_limit_order()
        self.cross_stop_order()
        self.strategy.on_bar(bar)

        self.update_daily_close(bar.close_price)

    def new_tick(self, tick: TickData):
        """"""
        self.tick = tick
        self.datetime = tick.datetime

        self.cross_limit_order()
        self.cross_stop_order()
        self.strategy.on_tick(tick)

        self.update_daily_close(tick.last_price)

    def cross_limit_order(self):
        """
        Cross limit order with last bar/tick data.
        """
        if self._type == BacktestingMode.BAR:
            long_cross_price = self.bar.low_price
            short_cross_price = self.bar.high_price
            long_best_price = self.bar.open_price
            short_best_price = self.bar.open_price
        else:
            long_cross_price = self.tick.ask_price_1
            short_cross_price = self.tick.bid_price_1
            long_best_price = long_cross_price
            short_best_price = short_cross_price

        for order in list(self.active_limit_orders.values()):
            # Push order update with status "not traded" (pending).
            if order.status == Status.SUBMITTING:
                order.status = Status.NOTTRADED
                self.strategy.on_order(order)

            # Check whether limit orders can be filled.
            long_cross = (
                order.direction == Direction.BUY
                and order.price >= long_cross_price
                and long_cross_price > 0
            )

            short_cross = (
                order.direction == Direction.SELL
                and order.price <= short_cross_price
                and short_cross_price > 0
            )

            if not long_cross and not short_cross:
                continue

            # Push order udpate with status "all traded" (filled).
            order.traded = order.volume
            order.status = Status.ALLTRADED
            self.strategy.on_order(order)

            self.active_limit_orders.pop(order.vt_order_id)

            # Push trade update
            self.trade_count += 1

            if long_cross:
                trade_price = min(order.price, long_best_price)
                pos_change = order.volume
            else:
                trade_price = max(order.price, short_best_price)
                pos_change = -order.volume

            trade = TradeData(
                symbol=order.symbol,
                exchange=order.exchange,
                order_id=order.order_id,
                trade_id=str(self.trade_count),
                direction=order.direction,
                offset=order.offset,
                price=trade_price,
                volume=order.volume,
                datetime=self.datetime,
                gateway_name=self.gateway_name,
            )

            self.strategy.pos += pos_change
            self.strategy.on_trade(trade)

            self.trades[trade.vt_trade_id] = trade

    def cross_stop_order(self):
        """
        Cross stop order with last bar/tick data.
        """
        if self._type == BacktestingMode.BAR:
            long_cross_price = self.bar.high_price
            short_cross_price = self.bar.low_price
            long_best_price = self.bar.open_price
            short_best_price = self.bar.open_price
        else:
            long_cross_price = self.tick.last_price
            short_cross_price = self.tick.last_price
            long_best_price = long_cross_price
            short_best_price = short_cross_price

        for stop_order in list(self.active_stop_orders.values()):
            # Check whether stop order can be triggered.
            long_cross = (
                stop_order.direction == Direction.BUY
                and stop_order.price <= long_cross_price
            )

            short_cross = (
                stop_order.direction == Direction.SELL
                and stop_order.price >= short_cross_price
            )

            if not long_cross and not short_cross:
                continue

            # Create order data.
            self.limit_order_count += 1

            order = OrderData(
                symbol=self.symbol,
                exchange=self.exchange,
                order_id=str(self.limit_order_count),
                direction=stop_order.direction,
                offset=stop_order.offset,
                price=stop_order.price,
                volume=stop_order.volume,
                status=Status.ALLTRADED,
                gateway_name=self.gateway_name,
                datetime=self.datetime
            )

            self.limit_orders[order.vt_order_id] = order

            # Create trade data.
            if long_cross:
                trade_price = max(stop_order.price, long_best_price)
                pos_change = order.volume
            else:
                trade_price = min(stop_order.price, short_best_price)
                pos_change = -order.volume

            self.trade_count += 1

            trade = TradeData(
                symbol=order.symbol,
                exchange=order.exchange,
                order_id=order.order_id,
                trade_id=str(self.trade_count),
                direction=order.direction,
                offset=order.offset,
                price=trade_price,
                volume=order.volume,
                datetime=self.datetime,
                gateway_name=self.gateway_name,
            )

            self.trades[trade.vt_trade_id] = trade

            # Update stop order.
            stop_order.vt_order_ids.append(order.vt_order_id)
            stop_order.status = StopOrderStatus.TRIGGERED

            if stop_order.stoporder_id in self.active_stop_orders:
                self.active_stop_orders.pop(stop_order.stoporder_id)

            # Push update to strategy.
            self.strategy.on_stop_order(stop_order)
            self.strategy.on_order(order)

            self.strategy.pos += pos_change
            self.strategy.on_trade(trade)

    

    # def load_bar(self, vt_symbol: str, days: int, interval: Interval, callback: Callable, use_database: bool):
    #     """ 实现 StrategyEngine::load_bar """
    #     self.days = days
    #     self.callback = callback

    # def load_tick(self, vt_symbol: str, days: int, callback: Callable):
    #     """ 实现 StrategyEngine::load_tick """
    #     self.days = days
    #     self.callback = callback

    def send_order(self, strategy: BaseStrategy, direction: Direction, offset: Offset, price: float, volume: float, stop: bool, lock: bool):
        """"""
        price = Utils.round_to(price, self._pricetick)
        if stop:
            vt_order_id = self.send_stop_order(direction, offset, price, volume)
        else:
            vt_order_id = self.send_limit_order(direction, offset, price, volume)
        return [vt_order_id]

    def send_stop_order(self, direction: Direction, offset: Offset, price: float, volume: float):
        """"""
        self.stop_order_count += 1

        stoporder_data = StoporderData(
            vt_symbol=self._vt_symbol,
            direction=direction,
            offset=offset,
            price=price,
            volume=volume,
            stoporder_id=f"{STOPORDER_PREFIX}.{self.stop_order_count}",
            strategy_name=self.strategy.strategy_name,
        )

        self.active_stop_orders[stoporder_data.stoporder_id] = stoporder_data
        self.stop_orders[stoporder_data.stoporder_id] = stoporder_data

        return stoporder_data.stoporder_id

    def send_limit_order(self, direction: Direction, offset: Offset, price: float, volume: float):
        """"""
        self.limit_order_count += 1

        order = OrderData(
            symbol=self.symbol,
            exchange=self.exchange,
            order_id=str(self.limit_order_count),
            direction=direction,
            offset=offset,
            price=price,
            volume=volume,
            status=Status.SUBMITTING,
            gateway_name=self.gateway_name,
            datetime=self.datetime
        )

        self.active_limit_orders[order.vt_order_id] = order
        self.limit_orders[order.vt_order_id] = order

        return order.vt_order_id

    def cancel_order(self, strategy: BaseStrategy, vt_order_id: str):
        """
        Cancel order by vt_order_id.
        """
        if vt_order_id.startswith(STOPORDER_PREFIX):
            self.cancel_stop_order(strategy, vt_order_id)
        else:
            self.cancel_limit_order(strategy, vt_order_id)

    def cancel_stop_order(self, strategy: BaseStrategy, vt_order_id: str):
        """"""
        if vt_order_id not in self.active_stop_orders:
            return
        stop_order = self.active_stop_orders.pop(vt_order_id)

        stop_order.status = StopOrderStatus.CANCELLED
        self.strategy.on_stop_order(stop_order)

    def cancel_limit_order(self, strategy: BaseStrategy, vt_order_id: str):
        """"""
        if vt_order_id not in self.active_limit_orders:
            return
        order = self.active_limit_orders.pop(vt_order_id)

        order.status = Status.CANCELLED
        self.strategy.on_order(order)

    def cancel_all(self, strategy: BaseStrategy):
        """"""
        limit_orderids = list(self.active_limit_orders.keys())
        for vt_order_id in limit_orderids:
            self.cancel_limit_order(strategy, vt_order_id)

        stop_orderids = list(self.active_stop_orders.keys())
        for vt_order_id in stop_orderids:
            self.cancel_stop_order(strategy, vt_order_id)


    def send_email(self, msg: str, strategy: BaseStrategy = None):
        """
        Send email to default receiver.
        """
        pass

    def sync_strategy_data(self, strategy: BaseStrategy):
        """
        Sync strategy data into json file.
        """
        pass

    # def get_engine_type(self):
    #     """
    #     Return engine type.
    #     """
    #     return self.engine_type

    def get_pricetick(self, strategy: BaseStrategy):
        """
        Return contract pricetick data.
        """
        return self._pricetick

    def put_strategy_event(self, strategy: BaseStrategy):
        """
        生成更新策略状态的事件
        """
        pass

    def write_log(self, msg: str):
        """"""
        if self._signal_log:
            self._signal_log.emit(msg)
        else:
            print(f"{datetime.now()}\t{msg}")

    def get_all_trade_result(self):
        """
        获取成交记录数据
        """
        return list(self.trades.values())

    def get_all_order_result(self):
        """
        获取限价委托订单数据
        """
        return list(self.limit_orders.values())

    def get_all_daily_result(self):
        """
        获取日盈亏数据
        """
        return list(self.daily_results.values())

    # @property
    # def engine_type(self):
    #     return self.engine_type

    def get_strategy_parameter(self):
        """"""
        if self._strategy_parameter is None:
            self._strategy_parameter = self._strategy_class.get_class_parameters()

        return self._strategy_parameter

    def set_strategy_parameter(self, parameter: dict):
        """"""
        self._strategy_parameter = parameter

    def reload_strategy_parameter(self):
        """"""
        self._strategy_parameter = self._strategy_class.get_class_parameters()

    @property
    def strategy_class_name(self):
        """"""
        return self._strategy_class_name

    def save_setting(self, setting: dict):
        """"""
        self._vt_symbol = setting["vt_symbol"]
        self._interval = setting["interval"]
        self._rate = setting["rate"]
        self._slippage = setting["slippage"]
        self._size = setting["size"]
        self._pricetick = setting["pricetick"]
        self._capital = setting["capital"]
        self._inverse = setting["inverse"]

    @property
    def rate(self):
        return self._rate

    @rate.setter
    def rate(self, val: float):
        self._rate = val

    @property
    def slippage(self):
        return self._slippage

    @slippage.setter
    def slippage(self, val: float):
        self._slippage = val

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, val: int):
        self._size = val

    @property
    def pricetick(self):
        return self._pricetick

    @pricetick.setter
    def pricetick(self, val: float):
        self._pricetick = val

    @property
    def capital(self):
        return self._capital

    @capital.setter
    def capital(self, val: int):
        self._capital = val

    @property
    def inverse(self):
        return self._inverse

    @inverse.setter
    def inverse(self, val: bool):
        self._inverse = val


class DailyResult:
    """"""

    def __init__(self, date: date, close_price: float):
        """"""
        self.date = date
        self.close_price = close_price
        self.pre_close = 0

        self.trades = []
        self.trade_count = 0

        self.start_pos = 0
        self.end_pos = 0

        self.turnover = 0
        self.commission = 0
        self._slippage = 0

        self.trading_pnl = 0
        self.holding_pnl = 0
        self.total_pnl = 0
        self.net_pnl = 0

    def add_trade(self, trade: TradeData):
        """"""
        self.trades.append(trade)

    def calculate_pnl(self, pre_close: float, start_pos: float, size: int, rate: float, slippage: float, inverse: bool):
        """"""
        # 如果第一天没有提供预结算
        # 使用值1可避免零除错误
        if pre_close:
            self.pre_close = pre_close
        else:
            self.pre_close = 1

        # 持仓pnl是指从当日开始持仓的pnl
        self.start_pos = start_pos
        self.end_pos = start_pos

        if not inverse:     # 常规合约
            self.holding_pnl = self.start_pos * (self.close_price - self.pre_close) * size
        else:               # 加密货币反向合约
            self.holding_pnl = self.start_pos * (1 / self.pre_close - 1 / self.close_price) * size

        # 交易pnl是当日新交易的pnl
        self.trade_count = len(self.trades)

        for trade in self.trades:
            if trade.direction == Direction.BUY:
                pos_change = trade.volume
            else:
                pos_change = -trade.volume

            self.end_pos += pos_change

            if not inverse:     # 常规合约
                turnover = trade.volume * size * trade.price
                self.trading_pnl += pos_change * (self.close_price - trade.price) * size
                self._slippage += trade.volume * size * slippage
            else:               # 加密货币反向合约
                turnover = trade.volume * size / trade.price
                self.trading_pnl += pos_change * (1 / trade.price - 1 / self.close_price) * size
                self._slippage += trade.volume * size * slippage / (trade.price ** 2)

            self.turnover += turnover
            self.commission += turnover * rate

        # 净pnl考虑了佣金和滑差成本
        self.total_pnl = self.trading_pnl + self.holding_pnl
        self.net_pnl = self.total_pnl - self.commission - self._slippage


def optimize(
    target_name: str,
    strategy_class: BaseStrategy,
    setting: dict,
    vt_symbol: str,
    interval: Interval,
    start: datetime,
    rate: float,
    slippage: float,
    size: float,
    pricetick: float,
    capital: int,
    end: datetime,
    mode: BacktestingMode,
    inverse: bool
):
    """"""
    engine = BacktesterEngine()

    engine.set_parameters(vt_symbol=vt_symbol, interval=interval, start=start, rate=rate, slippage=slippage, size=size, pricetick=pricetick, capital=capital, end=end, mode=mode, inverse=inverse)
    engine.add_strategy(strategy_class, setting)
    engine.load_data()
    engine.run_backtesting()
    engine.calculate_result()
    statistics = engine.calculate_statistics(output=False)

    target_value = statistics[target_name]
    return (str(setting), target_value, statistics)


# @lru_cache(maxsize=1000000)
# def _ga_optimize(parameter_values: tuple):
#     """"""
#     setting = dict(parameter_values)
#     result = optimize(ga_target_name, ga_strategy_class, setting, ga_vt_symbol, ga_interval, ga_start, ga_rate, ga_slippage, ga_size, ga_pricetick, ga_capital, ga_end, ga_mode, ga_inverse)
#     return (result[1],)


# def ga_optimize(parameter_values: list):
#     """"""
#     return _ga_optimize(tuple(parameter_values))


@lru_cache(maxsize=999)
def load_bar_data(symbol: str, exchange: Exchange, interval: Interval, start: datetime, end: datetime):
    """"""
    return database_manager.load_bar_data(symbol, exchange, interval, start, end)


@lru_cache(maxsize=999)
def load_tick_data(symbol: str, exchange: Exchange, start: datetime, end: datetime):
    """"""
    return database_manager.load_tick_data(symbol, exchange, start, end)


# GA相关全局值
# ga_end = None
# ga_mode = None
# ga_target_name = None
# ga_strategy_class = None
# ga_setting = None
# ga_vt_symbol = None
# ga_interval = None
# ga_start = None
# ga_rate = None
# ga_slippage = None
# ga_size = None
# ga_pricetick = None
# ga_capital = None

import pandas as pd
import mplfinance as mpf

# 创建一个空的数据框
data = pd.DataFrame(columns=['Open', 'High', 'Low', 'Close', 'Volume'])

# 设置数据框的索引为日期范围（可以设置一个虚拟的日期范围）
data.index = pd.date_range(start='2024-07-01', end='2024-07-10', freq='D')

# 绘制 K 线图
mpf.plot(data, type='candle', style='charles', title='Empty K-line Chart', ylabel='Price')
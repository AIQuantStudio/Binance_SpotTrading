# #需要用到 wxPython 库

# import wx

# from wx import FontEnumerator

# import matplotlib
# print(matplotlib.matplotlib_fname())

# aaa = wx.App(False)

# # FontEnumerator 枚举系统上所有可用的字体
# e = wx.FontEnumerator()


# # fontlist=e.GetFacenames()

# # print("可用字体数：", len(fontlist))

# # for i in fontlist:
# #     print(i)
    
# from matplotlib.font_manager import FontManager
# fm = FontManager()

# print(fm.ttflist)
# for i in fm.ttflist:
#     print(i.name)



import numpy as np
 
# 假设matrix是你的输入矩阵
matrix = np.array([[1, 2, 3],
                   [4, 5, 6],
                   [7, 8, 9]])
 
# 保留最后一行
last_row = matrix[-1:]
 
print(last_row)
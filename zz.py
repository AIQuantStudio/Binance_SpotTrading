#需要用到 wxPython 库

import wx

from wx import FontEnumerator

import matplotlib
print(matplotlib.matplotlib_fname())

aaa = wx.App(False)

# FontEnumerator 枚举系统上所有可用的字体
e = wx.FontEnumerator()

fontlist=e.GetFacenames()

print("可用字体数：", len(fontlist))

for i in fontlist[:20]:
    print(i)

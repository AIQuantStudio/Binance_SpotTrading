Config_Data = {
    "FontFamily": "Arial",
    "FontSize": 12,
    'Url':'https://www.3356g3356.com:8990/',
    'LowerLimit': 5,
    'UpperLimit': 1000,
    'Ratio': 1,
    'MailAddrs':['376844229@qq.com']
}

def init_cfg(data):
    for key, value in data.items():
        Config_Data[key] = value

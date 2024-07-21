from dataclasses import dataclass


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


@dataclass
class ModelConfig:
    Models = {
        "LSTM_V1": {
            "class": "LstmV1"
        },
        "LSTM_V2": {
            "class": "LstmV2"
        }
    }
        
    ModelValues =["lstmv1", "lstmv2"]

    
    
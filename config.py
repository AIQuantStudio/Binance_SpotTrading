from dataclasses import dataclass
from logging import CRITICAL

Config_Data = {
    "FontFamily": "Arial",
    "FontSize": 12,
    "model.path": "./data",

    "BinanceAccount":[
        {
            "Name": "ZhuZheng",
            "Account": "23194749@qq.com",
            "ApiKey": "tPMBEjZCnFiAszSuXMzk1r8ASdd20dUwlaVFsOv4LvnfVW5xEPPZYK5JqlrOTnSU",
            "SecertKey": "R2rh9FwjRCWRxm5I8muCmErmFeSyKMsjx8ecg5kqXYcqEbPWzfEFq7VZBOb1xdnY"
        },
        {
            "Name": "Test",
            "Account": "13812665650",
            "ApiKey": "111",
            "SecertKey": "222"
        },
    ],
    
    "log.active": True,
    "log.level": CRITICAL,
    "log.console": True,
    "log.file": True,
    "log.formatter": "%(asctime)s  %(levelname)s: %(message)s",

    "email.server": "smtp.qq.com",
    "email.port": 465,
    "email.username": "",
    "email.password": "",
    "email.sender": "",
    "email.receiver": "",
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
        },
        
    }
        
    ModelValues =["lstmv1", "lstmv2"]
    
@dataclass
class Accounts:
    data = [
        {
            "Name": "ZhuZheng",
            "Account": "23194749@qq.com",
            "ApiKey": "tPMBEjZCnFiAszSuXMzk1r8ASdd20dUwlaVFsOv4LvnfVW5xEPPZYK5JqlrOTnSU",
            "SecertKey": "R2rh9FwjRCWRxm5I8muCmErmFeSyKMsjx8ecg5kqXYcqEbPWzfEFq7VZBOb1xdnY"
        },
        {
            "Name": "Test",
            "Account": "13812665650",
            "ApiKey": "111",
            "SecertKey": "222"
        },
    ]
        

    
    
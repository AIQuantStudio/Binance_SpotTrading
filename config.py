from dataclasses import dataclass
# from logging import CRITICAL

# _Version = "v1.0"


# Config_Data = {
#     "FontFamily": "Arial",
#     "FontSize": 12,
#     "model.path": "./data",

#     "BinanceAccount":[
#         {
#             "Name": "ZhuZheng",
#             "Account": "23194749@qq.com",
#             "ApiKey": "tPMBEjZCnFiAszSuXMzk1r8ASdd20dUwlaVFsOv4LvnfVW5xEPPZYK5JqlrOTnSU",
#             "SecertKey": "R2rh9FwjRCWRxm5I8muCmErmFeSyKMsjx8ecg5kqXYcqEbPWzfEFq7VZBOb1xdnY"
#         },
#         {
#             "Name": "Test",
#             "Account": "13812665650",
#             "ApiKey": "111",
#             "SecertKey": "222"
#         },
#     ],
    
#     "log.active": True,
#     "log.level": CRITICAL,
#     "log.console": True,
#     "log.file": True,
#     "log.formatter": "%(asctime)s  %(levelname)s: %(message)s",

#     "email.server": "smtp.qq.com",
#     "email.port": 465,
#     "email.username": "",
#     "email.password": "",
#     "email.sender": "",
#     "email.receiver": "",
# }

# def init_cfg(data):
#     for key, value in data.items():
#         Config_Data[key] = value


    
    
import json
import os
from logging import CRITICAL
from copy import copy
from pathlib import Path


Version = "v1.0"

_config_folder: str = ".config"
_congfig_filename: str = "config.json"
_custom_config_filepath = Path(".").joinpath(_congfig_filename)
_saved_config_filepath = Path(".").joinpath(_config_folder, _congfig_filename)

_global_config_data = {
    "model.default_path": "./data",
    
    "main_window.width": 1600,
    "main_window.height": 900,
    "font.family": "Arial",
    "font.size": 12,

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



def _get_config(name, default = None):
    if name in _global_config_data:
        return _global_config_data[name]
    else:
        return default


def _get_global_config(clone: bool = False):
    if clone:
        return copy(_global_config_data)

    return _global_config_data


def _save_global_config(data, refresh = True):
    setting_path = os.path.split(os.path.realpath(_saved_config_filepath))[0]
    if not os.path.exists(setting_path):
        os.mkdir(setting_path)

    with open(_saved_config_filepath, mode="w+", encoding="UTF-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    if refresh:
        _global_config_data.update(data)


def _init_config():
    # 加载自定义配置文件(config.json)
    if _custom_config_filepath.exists():
        with open(_custom_config_filepath, mode="r", encoding="UTF-8") as f:
            _global_config_data.update(json.load(f))

    # 加载保存的配置文件(./config/config.json)
    if _saved_config_filepath.exists():
        with open(_saved_config_filepath, mode="r", encoding="UTF-8") as f:
            _global_config_data.update(json.load(f))



class Config:
    init_config = _init_config
    
    get = _get_config
    get_global_config = _get_global_config
    save_global_config = _save_global_config



# @dataclass
# class ModelConfig:
#     Models = {
#         "LSTM_V1": {
#             "class": "LstmV1"
#         },
#         "LSTM_V2": {
#             "class": "LstmV2"
#         },
        
#     }
        
#     ModelValues =["lstmv1", "lstmv2"]
    
# @dataclass
# class Accounts:
#     data = [
#         {
#             "Name": "ZhuZheng",
#             "Account": "23194749@qq.com",
#             "ApiKey": "tPMBEjZCnFiAszSuXMzk1r8ASdd20dUwlaVFsOv4LvnfVW5xEPPZYK5JqlrOTnSU",
#             "SecertKey": "R2rh9FwjRCWRxm5I8muCmErmFeSyKMsjx8ecg5kqXYcqEbPWzfEFq7VZBOb1xdnY"
#         },
#         {
#             "Name": "Test",
#             "Account": "13812665650",
#             "ApiKey": "111",
#             "SecertKey": "222"
#         },
#     ]
        

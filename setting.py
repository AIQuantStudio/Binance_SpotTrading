from dataclasses import dataclass


@dataclass
class ModelSetting:
    Models = [
        {
            "name": "LSTM_V1",
            "class": "LstmV1"
        },
        {
            "name": "LSTM_V2",
            "class": "LstmV2"
        }
    ]
      

@dataclass
class AccountSetting:
    Accounts = [
        {
            "Name": "ZhuZheng",
            "Account": "23194749@qq.com",
            "ApiKey": "tPMBEjZCnFiAszSuXMzk1r8ASdd20dUwlaVFsOv4LvnfVW5xEPPZYK5JqlrOTnSU",
            "SecertKey": "R2rh9FwjRCWRxm5I8muCmErmFeSyKMsjx8ecg5kqXYcqEbPWzfEFq7VZBOb1xdnY"
        },
        {
            "Name": "[TEST] ADA_USDT",
            "Account": "13812665650",
            "DB": "./test.db"
        },
    ]
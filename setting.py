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
      
        
    # ModelValues =["lstmv1", "lstmv2"]
    
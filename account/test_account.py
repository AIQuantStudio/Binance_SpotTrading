import sqlite3

from account.base_account import BaseAccount


class TestAccount(BaseAccount):

    def __init__(self, model_id, account_data):
        super().__init__(model_id, account_data["Name"], account_data["Account"])
 
        self.db = account_data["DB"]

    def connect(self):
        try:
            self.conn = sqlite3.connect(self.db)
        except:
            self.conn = None
            return False

        return True
    
    def close(self):
        self.conn.close()

    def get_asset_balance(self):
        cursor = self.conn.cursor().execute("SELECT * from asset")
        balances = []
        for row in cursor:
            balance = {"asset": row[0], "free": row[1], "locked": row[2]}
            balances.append(balance)

        return balances

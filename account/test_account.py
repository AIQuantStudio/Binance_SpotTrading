import sqlite3

class TestAccount:

    def __init__(self, account_data):
        self.name = account_data.name
        self.id = account_data.id
        self.db = account_data.db

    def connect(self):
        try:
            self.conn = sqlite3.connect(self.db)
        except:
            self.conn = None
            return False

        return True

    def get_all_asset_balance(self):
        c = self.conn.cursor()
        print ("数据库打开成功")

        cursor = c.execute("SELECT *  from asset")
        for row in cursor:
            print ("ID = ", row[0])
            print ("NAME = ", row[1])
            print ("ADDRESS = ", row[2])

            print ("数据操作成功")
        
        return []

        # data = self.client.get_account()
        # balances = data["balances"]
        # return [balance for balance in balances if float(balance["free"]) > 0 or float(balance["locked"]) > 0]

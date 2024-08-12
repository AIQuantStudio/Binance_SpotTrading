import sqlite3


class TestAccount:

    def __init__(self, account_data):
        print(account_data)
        self.name = account_data["Name"]
        self.id = account_data["Account"]
        self.db = account_data["DB"]

    def connect(self):
        try:
            self.conn = sqlite3.connect(self.db)
        except:
            self.conn = None
            return False

        return True

    def get_all_asset_balance(self):
        cursor = self.conn.cursor().execute("SELECT * from asset")
        balances = []
        for row in cursor:
            balance = {"asset": row[0], "free": row[1], "locked": row[2]}
            balances.append(balance)

        return balances

import pandas


class Users:
    def __init__(self):
        self.credentials_path = "login_credentials.CSV"
        self.users_data = pandas.read_csv(self.credentials_path)

    def add_user(self, username, password):
        data_to_add = [username, password]
        self.users_data.loc[len(self.users_data)] = data_to_add
        self.users_data.to_csv(self.credentials_path, index=False)

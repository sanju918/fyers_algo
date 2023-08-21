import json


class Settings:
    def __init__(self, path="db.json"):
        self.path = path
        self.app_id = ''
        self.app_secret = ''
        self.access_token = ''
        self.old_time_stamp = 0
        self.new_time_stamp = 0
        self.delta_settings = {}
        self.load_settings()

    def load_settings(self):
        with open(self.path, 'r') as json_object:
            settings = json.load(json_object)
        self.delta_settings = settings
        self.app_id = settings["fixed_settings"]["FYERS_CLIENT_ID"]
        self.app_secret = settings["fixed_settings"]["FYERS_SECRET_ID"]
        self.access_token = settings["dynamic_settings"]["access_token"]
        self.old_time_stamp = settings["dynamic_settings"]["time_generated"]

    def write_settings(self, access_token, time_stamp):
        self.delta_settings["dynamic_settings"]["access_token"] = access_token
        self.delta_settings["dynamic_settings"]["time_generated"] = time_stamp

        with open(self.path, 'w') as out_file:
            out_file.write(json.dumps(self.delta_settings, indent=4))


st = Settings()
print(st.delta_settings)
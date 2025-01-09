import pandas as pd
import os

class Logging_Tools:
    def __init__(self):
        print("Utils class created.")
        pass

    def create_log(self, log_name, additional_info=""):
        log_name = "log/" + log_name

        if not os.path.exists(log_name):
            os.makedirs(os.path.dirname(log_name), exist_ok=True)

        with open(log_name, 'w') as f:
            f.write(f"Log file created. ({log_name})\nAdditional Info: {additional_info}\n")

    def append_to_log(self, log_name, message):
        log_name = "log/" + log_name
        with open(log_name, 'a') as f:
            f.write("\n" + message)

    def create_excel_file(self, file_name, sheet_name, data):    
        file_name = "log/" + file_name
        # if exist, remove the file
        try:
            os.remove(file_name)
        except OSError:
            pass
        
        df = pd.DataFrame(data)
        df.to_excel(file_name, sheet_name=sheet_name, index=False)

    def append_to_excel(self, file_name, sheet_name, data):
        file_name = "log/" + file_name
        # Data is one row
        excel_df = pd.read_excel(file_name, sheet_name=sheet_name)
        excel_df = pd.concat([excel_df, pd.DataFrame([data])], ignore_index=True)
        excel_df.to_excel(file_name, sheet_name=sheet_name, index=False)
        
    def excel_to_df(self, file_name, sheet_name):
        file_name = "log/" + file_name
        excel_df = pd.read_excel(file_name, sheet_name=sheet_name)
        return excel_df

            
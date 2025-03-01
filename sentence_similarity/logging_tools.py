import pandas as pd
import os

class Logging_Tools:
    def __init__(self):
        print("Utils class created.")
        pass
    
    def create_csv_file(self, file_name, data):
        file_name = "log/" + file_name
        # if exist, remove the file
        try:
            os.remove(file_name)
        except OSError:
            pass
        
        df = pd.DataFrame(data)
        df.to_csv(file_name, index=False)

    def append_to_csv(self, file_name, data):
        file_name = "log/" + file_name
        # Data is one row
        csv_df = pd.read_csv(file_name)
        csv_df = pd.concat([csv_df, pd.DataFrame([data])], ignore_index=True)
        csv_df.to_csv(file_name, index=False)

    def csv_to_df(self, file_name):
        file_name = "log/" + file_name
        csv_df = pd.read_csv(file_name)
        return csv_df
    


            
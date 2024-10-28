import pandas as pd

#
# load_data
#   input:
#       - file_path: file path of csv file
#
#   output:
#       - raw data (DataFrame)
#
def load_data(file_path):
    try:
        data = pd.read_csv(file_path, delimiter=';')
        return data
    except Exception as e:
        print("Error loading data:", e)
        return None
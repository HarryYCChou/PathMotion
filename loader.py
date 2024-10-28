import pandas as pd

#
# load_data
#   input:
#       - file_path: file path of csv file
#       - chunksize: data chunk(lines) read each time
#
#   output:
#       - raw data (DataFrame)
#
def load_data(file_path, chunksize=10000):
    try:
        # Count total lines in the file
        total_lines = sum(1 for _ in open(file_path, 'r', encoding='cp950', errors='replace'))
        # lines_processed is for progress calculation
        lines_processed = 0

        # Create DataFrame for data
        data = pd.DataFrame()

        for chunk in pd.read_csv(file_path, delimiter=';', chunksize=chunksize):
            # concat data
            data = pd.concat([data, chunk], ignore_index=True)
            # progress
            lines_processed += len(chunk)
            percentage = lines_processed / total_lines * 100
            print(f"Load data processing: {percentage:.2f}%...", end='\r')
        
        return data
    except Exception as e:
        print("Error loading data:", e)
        return None
#
#   Note: The analyzer gets data from a fixed position (hard code)
#

#
#   get_description
#       input:
#          - data: raw data (DataFrame)
#
#      output:
#           data description:
#               - test date
#               - test time
#               - sample rate
#
def get_description(data):
    if data is not None:
        return dict(test_date=data.iloc[1,1],
                    test_time=data.iloc[2,1],
                    sample_rate=data.iloc[4,1])

#
#   get_sensor_data
#       input:
#          - data: raw data (DataFrame)
#
#       output:
#           - time_data
#           - accel_data_low
#           - accel_data_high
#           - gyro_data
#
def get_sensor_data(data):
    return data.iloc[28:,0], data.iloc[28:, 1:4], data.iloc[28:, 4:7], data.iloc[28:, 7:10]
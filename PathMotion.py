from loader import load_data
from analyzer import get_description, get_sensor_data
from simulator import simulate
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

#
#   plot_result
#       input:
#           - result: simulate result (numpy shape of (n, 3))
#           - reduce: slicing to take every reduce_th row
#
#       output:
#           - 3D path motion figure
#
def plot_result(result, reduce):
    # Create a new figure
    fig = plt.figure()

    # Create a 3D axis
    ax = fig.add_subplot(111, projection='3d')

    # slicing to take every reduce_th row
    reduced_result = result[::reduce]
    x = reduced_result[:, 0]  # First column
    y = reduced_result[:, 1]  # Second column
    z = reduced_result[:, 2]  # Third column

    # Scatter plot
    ax.scatter(x, y, z, c='r', marker='o')  # 'c' is for color and 'marker' specifies the point shape

    # Set labels
    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    ax.set_zlabel('Z Label')

    # Set title
    ax.set_title('3D Path Motion')

    # Show the plot
    plt.show()

#
#   main
#       input:
#           - file_path: file path
#
#       output:
#           - 3D path motion figure
# 
#       load_data->get_description->simulate->plot_result
#
def main():
    file_path = input("Please enter a file name(.csv): ")
    print("Load file...")
    raw_data = load_data(file_path)
    if raw_data is not None:
        print("Data loaded successfully!")
        print("Load data description...")
        description = get_description(raw_data)
        time_data, accel_data_low, accel_data_high, gyro_data = get_sensor_data(raw_data)
        print("Run simulation...")
        result = simulate(accel_data_high.to_numpy().astype(float),
                          gyro_data.to_numpy().astype(float),
                          1/int(description['sample_rate']))
        print("Plot result...")
        plot_result(result, 5000)
    else:
        print("Invalid file path or format")

if __name__ == "__main__":
    main()
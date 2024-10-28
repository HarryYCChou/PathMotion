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
def plot_result(result, reduce=5000):
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
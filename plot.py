import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

# Wing half-span (distance from center to wing tip)
WING_HALF_SPAN = 2000.0

def rotation_matrix(angles):
    """Create rotation matrix from roll, pitch, yaw angles (in radians)"""
    roll, pitch, yaw = angles

    # Rotation matrix for roll (X-axis)
    R_roll = np.array([
        [1, 0, 0],
        [0, np.cos(roll), -np.sin(roll)],
        [0, np.sin(roll), np.cos(roll)]
    ])

    # Rotation matrix for pitch (Y-axis)
    R_pitch = np.array([
        [np.cos(pitch), 0, np.sin(pitch)],
        [0, 1, 0],
        [-np.sin(pitch), 0, np.cos(pitch)]
    ])

    # Rotation matrix for yaw (Z-axis)
    R_yaw = np.array([
        [np.cos(yaw), -np.sin(yaw), 0],
        [np.sin(yaw), np.cos(yaw), 0],
        [0, 0, 1]
    ])

    # Combine the rotation matrices
    R = R_yaw @ R_pitch @ R_roll
    return R

def draw_wing(ax, position, prev_position, next_position, angles_deg):
    """Draw bird wing at given position, perpendicular to flight path (wings extend sideways)"""
    # Calculate flight direction (tangent to path)
    if prev_position is not None and next_position is not None:
        flight_dir = next_position - prev_position
    elif next_position is not None:
        flight_dir = next_position - position
    elif prev_position is not None:
        flight_dir = position - prev_position
    else:
        flight_dir = np.array([1, 0, 0])  # Default: moving along X

    # Normalize flight direction
    flight_len = np.linalg.norm(flight_dir)
    if flight_len > 0:
        flight_dir = flight_dir / flight_len
    else:
        flight_dir = np.array([1, 0, 0])

    # Find a perpendicular direction for the wing
    # Wing extends sideways, perpendicular to flight direction
    # Use cross product with world up (Z) to get wing direction
    world_up = np.array([0, 0, 1])

    # If flight is along Z, use Y as reference
    if np.abs(np.dot(flight_dir, world_up)) > 0.95:
        world_up = np.array([0, 1, 0])

    # Wing direction = cross(flight_dir, world_up) - gives sideways direction
    wing_dir = np.cross(flight_dir, world_up)
    wing_len = np.linalg.norm(wing_dir)
    if wing_len > 0:
        wing_dir = wing_dir / wing_len
    else:
        wing_dir = np.array([0, 1, 0])

    # Wing endpoints (left wing tip to right wing tip)
    wing_start = position - wing_dir * WING_HALF_SPAN
    wing_end = position + wing_dir * WING_HALF_SPAN

    # Draw the wing as a blue line (perpendicular to flight path)
    ax.plot([wing_start[0], wing_end[0]],
            [wing_start[1], wing_end[1]],
            [wing_start[2], wing_end[2]],
            'b-', linewidth=3, label='Wing' if np.allclose(position, [0, 0, 0], atol=0.01) else "")

#
#   plot_result
#       input:
#           - result: simulate result (numpy shape of (n, 3))
#           - angles: gyro angles (numpy shape of (n, 3)) in degrees
#           - reduce: slicing to take every reduce_th row
#
#       output:
#           - 3D path motion figure with wing visualization and slider
#
def plot_result(result, angles, reduce=5000):
    # Create a new figure
    fig = plt.figure(figsize=(12, 8))

    # Create a 3D axis
    ax = fig.add_subplot(111, projection='3d')

    # slicing to take every reduce_th row
    reduced_result = result[::reduce]
    x = reduced_result[:, 0]  # First column
    y = reduced_result[:, 1]  # Second column
    z = reduced_result[:, 2]  # Third column

    # Scatter plot
    ax.scatter(x, y, z, c='r', marker='o', s=10, alpha=0.5, label='Path')

    # Set labels
    ax.set_xlabel('X (m)')
    ax.set_ylabel('Y (m)')
    ax.set_zlabel('Z (m)')

    # Set title
    ax.set_title('3D Path Motion with Wing Visualization')

    # Calculate total frames
    total_frames = len(result)
    current_index = [0]  # Use list to allow modification in closure
    wing_path = [result[0]]  # Track wing center path

    # Initial draw of wing at first position
    prev_pos = None
    next_pos = result[1] if len(result) > 1 else None
    draw_wing(ax, result[0], prev_pos, next_pos, angles[0])
    ax.legend()

    # Create slider axis at the bottom
    from matplotlib.widgets import Slider
    ax_slider = plt.axes([0.125, 0.05, 0.75, 0.03])
    slider = Slider(
        ax=ax_slider,
        label='Time',
        valmin=0,
        valmax=total_frames - 1,
        valinit=0,
        valstep=1
    )

    def update(val):
        """Update the wing position based on slider value"""
        # Clear the axis
        ax.cla()

        # Re-setup the axis
        ax.set_xlabel('X (m)')
        ax.set_ylabel('Y (m)')
        ax.set_zlabel('Z (m)')

        # Get current index from slider
        current_index[0] = int(slider.val)

        # Calculate reduced current index for matching the scatter plot
        reduced_current = current_index[0] // reduce

        # Redraw path
        ax.scatter(x, y, z, c='r', marker='o', s=10, alpha=0.5, label='Path')

        # Draw wing motion trail (blue line showing where wing has been) - match reduced path
        wing_trail = reduced_result[:reduced_current+1]
        if len(wing_trail) > 1:
            ax.plot(wing_trail[:, 0], wing_trail[:, 1], wing_trail[:, 2], 'b-', linewidth=1, alpha=0.6, label='Wing Motion')

        # Draw wing at current position (perpendicular to path)
        idx = current_index[0]
        prev_pos = result[idx - 1] if idx > 0 else None
        next_pos = result[idx + 1] if idx < len(result) - 1 else None
        draw_wing(ax, result[idx], prev_pos, next_pos, angles[idx])

        ax.legend()

        # Update title with current time info
        ax.set_title(f'3D Path Motion with Wing Visualization (Frame: {current_index[0]}/{total_frames - 1})')

        fig.canvas.draw_idle()

    # Connect slider update function
    slider.on_changed(update)

    # Store slider reference to prevent garbage collection
    fig.slider = slider

    # Show the plot
    plt.show()
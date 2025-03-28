import numpy as np

#
#   rotation_matrix
#       input:
#           - angles: [roll, pitch, yaw] numpy arrays of shape(n, 3)
#
#       output:
#           - R: rotation matrix (numpy array of shape(n, 3))
#
def rotation_matrix(angles):
    # Convert to radians
    angle_roll = np.radians(angles[0])
    angle_pitch = np.radians(angles[1])
    angle_yaw = np.radians(angles[2])

    # Rotation matrix for roll (X-axis)
    R_roll = np.array([
        [1, 0, 0],
        [0, np.cos(angle_roll), -np.sin(angle_roll)],
        [0, np.sin(angle_roll), np.cos(angle_roll)]
    ])

    # Rotation matrix for pitch (Y-axis)
    R_pitch = np.array([
        [np.cos(angle_pitch), 0, np.sin(angle_pitch)],
        [0, 1, 0],
        [-np.sin(angle_pitch), 0, np.cos(angle_pitch)]
    ])

    # Rotation matrix for yaw (Z-axis)
    R_yaw = np.array([
        [np.cos(angle_yaw), -np.sin(angle_yaw), 0],
        [np.sin(angle_yaw), np.cos(angle_yaw), 0],
        [0, 0, 1]
    ])
    
    # Combine the rotation matrices
    R = R_yaw @ R_pitch @ R_roll  # Using @ for matrix multiplication

    return R

#
#   integrate_gyro
#       input:
#           - gyro_data: numpy arrays of shape(n, 3)
#           - dt: delta time(float)
#
#       output:
#           - angles: rotation angle [roll, pitch, yaw] (numpy array of shape(n, 3))
#
def integrate_gyro(gyro_data, dt, update_progress):
    # Count total lines in the data
    total_lines = gyro_data.shape[0]
    # lines_processed is for progress calculation
    lines_processed = 0

    angles = []
    angle = np.zeros(3)  # [roll, pitch, yaw]
    for gyro in gyro_data:
        # FIXME: R*gyro*dt
        R = rotation_matrix(angle)  # Create rotation matrix from angles
        angle += R @ gyro * dt
        angles.append(angle.copy())
        # progress
        lines_processed += 1
        percentage = lines_processed / total_lines * 100
        update_progress(percentage, "Calculate rotation angle...")
        #print(f"Calculate rotation angle: {percentage:.2f}%...", end='\r')

    return np.array(angles)

#
#   rotate_accel
#       input:
#           - accel_data: numpy arrays of shape(n, 3)
#           - angles: rotation angle [roll, pitch, yaw] (numpy array of shape(n, 3)) 
#
#       output:
#           - rotated_accel: rotated angle [roll, pitch, yaw] (numpy array of shape(n, 3))
#
def rotate_accel(accel_data, angles, update_progress):
    # Count total lines in the data
    total_lines = accel_data.shape[0]
    # lines_processed is for progress calculation
    lines_processed = 0

    rotated_accel = []

    for i, angle in enumerate(angles):
        # Assuming angle = [roll, pitch, yaw]
        R = rotation_matrix(angle)  # Create rotation matrix from angles
        rotated = R @ accel_data[i]
        rotated_accel.append(rotated)
        # progress
        lines_processed += 1
        percentage = lines_processed / total_lines * 100
        update_progress(percentage, "Calculate rotated acceleration...")
        #print(f"Calculate rotated acceleration: {percentage:.2f}%...", end='\r')
    return np.array(rotated_accel)

#
#   integrate_accel
#       input:
#           - accel_data: numpy arrays of shape(n, 3)
#           - dt: delta time(float)
#
#       output:
#           - positions: pisition [x, y, z] (numpy array of shape(n, 3))
#
def integrate_accel(accel_data, dt, update_progress):
    # Count total lines in the data
    total_lines = accel_data.shape[0]
    # lines_processed is for progress calculation
    lines_processed = 0

    velocity = np.zeros(3)  # Initial velocity
    position = np.zeros(3)  # Initial position
    positions = []

    for accel in accel_data:
        velocity += accel * dt
        position += velocity * dt
        positions.append(position.copy())
        # progress
        lines_processed += 1
        percentage = lines_processed / total_lines * 100
        update_progress(percentage, "Calculate position...")
        #print(f"Calculate position: {percentage:.2f}%...", end='\r')
    return np.array(positions)

#
# simulate
#   input:
#       - accel_data: numpy arrays of shape(n, 3)
#       - gyro_data: numpy array of shape(n, 3)
#
#   output:
#       - positions: numpy array of shape(n, 3)
#
def simulate(accel_data, gyro_data, dt, update_progress):
    angles = integrate_gyro(gyro_data, dt, update_progress)
    rotated_accel = rotate_accel(accel_data, angles, update_progress)
    positions = integrate_accel(rotated_accel, dt, update_progress)

    return positions
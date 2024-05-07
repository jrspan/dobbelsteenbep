import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

# Define location of data file (CSV)
def get_filepath(filename: str):
    # Returns full filepath of input filename
    # Used in combination with "load_datafile" function
    directory_path = os.path.dirname((os.path.abspath(__file__)))
    return os.path.join(directory_path, filename)

# Retrieve pandas dataframe from filename
def load_datafile(filename: str):
    # Returns pd.dataFrame
    # Retrieve relative directory path
    filepath = get_filepath(filename)
    # Attempt to load data
    try:
        data = pd.read_csv(filepath, header=None, skiprows=1)
        times = np.array(data[1].tolist()) * 0.001
        return data, times
    except FileNotFoundError:
        raise FileNotFoundError(f"Data file not found in directory {filepath}")
        
def integrate_acceleration(velocity, acceleration, dt):
    return velocity + acceleration * dt

def integrate_velocity(position, velocity, dt):
    return position + velocity * dt

def create_acceleration_tables(data):
    acceleration_list = data.iloc[:, 2:5].values.tolist()
    
    return np.array(acceleration_list) * 9.81
        
def create_velocity_tables(accel_data, times):
    # Returns a list of predicted velocities for every timestep
    velocity_list = np.zeros((len(accel_data), 3))
    if len(velocity_list) != len(times):
        raise IndexError('Length of acceleration data and times do not match!')
    for i in range(1, len(times)):
        dt = times[i] - times[i-1]
        vel_x = integrate_acceleration(velocity_list[i-1][0], accel_data[i-1][0], dt)
        vel_y = integrate_acceleration(velocity_list[i-1][1], accel_data[i-1][1], dt)
        vel_z = integrate_acceleration(velocity_list[i-1][2], accel_data[i-1][2], dt)
        velocity_list[i] = [vel_x, vel_y, vel_z]
    return velocity_list

def create_position_tables(velocity_list, times):
    if len(times) != len(velocity_list):
        raise IndexError('Length of time list and velocity list do not match!')
    position_list = np.zeros((len(times), 3))
    for i in range(1, len(times)):
        dt = times[i] - times[i-1]
        pos_xyz = integrate_velocity(position_list[i-1], velocity_list[i-1], dt)
        position_list[i] = pos_xyz
    return position_list

def create_gyroscope_tables(data):
    # Returns gyroscope velocities as table
    gyroscope_velocity_list = data.iloc[:, 5:8].values.tolist()
    return gyroscope_velocity_list

# QUATERNIONS (1/4)    
def expq(vector, multiplier=1):
    x, y, z = vector[0] * multiplier, vector[1] * multiplier, vector[2]  * multiplier
    absq = (x ** 2 + y ** 2 + z ** 2) ** 1/2
    w = np.cos(absq)
    if absq == 0:
        return np.array([w, 0, 0, 0])
    else:
        sinabs = np.sin(absq)
        xq = x * sinabs / absq
        yq = y * sinabs / absq
        zq = z * sinabs / absq
        return np.array([w, xq, yq, zq])

# QUATERNIONS (2/4)
def quat_mul(p, q):
    p0 = p[0]
    q0 = q[0]
    pv = p[1:]
    qv = q[1:]
    out0 = p0 * q0 - np.dot(pv, qv)
    outv = p0 * qv + q0 * pv + np.cross(pv, qv)
    out = np.array([out0, *outv])
    return out

# QUATERNIONS (3/4)
def quaternion_conjugate(q):
    w, x, y, z = q
    return np.array([w, -x, -y, -z])

# QUATERNIONS (4/4)
# Actual Rotation Fuction - Input = Acceleration vector = 1x3 , rotation_quaternion = 1*4
def rotate_vector(vector, rotation_quaternion):
    # Convert the vector to a quaternion
    vector_quaternion = np.concatenate(([0], vector))

    # Calculate the rotated quaternion
    rotated_quaternion = quat_mul(rotation_quaternion, quat_mul(vector_quaternion, quaternion_conjugate(rotation_quaternion)))

    # Extract the rotated vector from the quaternion
    rotated_vector = rotated_quaternion[1:]

    return np.array(rotated_vector)

def create_rotational_quaternion_tables(gyroscope_data):
    rotation_quaternion_list = np.zeros((len(gyroscope_data), 4))
    for i in range(len(rotation_quaternion_list)):
        rotation_quaternion_list[i] = expq(gyroscope_data[i])
    return rotation_quaternion_list

def create_rotated_accel_vector_tables(acceleration_data, rotation_quaternion_data):
    if len(acceleration_data) != len(rotation_quaternion_data):
        raise IndexError(f"Lengtes van input datas komen niet overeen! ({len(acceleration_data)} != {len(rotation_quaternion_data)}")
    rotated_vectors = np.zeros((len(acceleration_data), 3))
    for i in range(len(acceleration_data)):
        rotated_vectors[i] = rotate_vector(acceleration_data[i], rotation_quaternion_data[i])
    return rotated_vectors


#filename = "merged_testfile.csv"
#filename = "dobbeldata.csv"
filename = "Out_8.csv"
dataframe, times = load_datafile(filename)
sensor_acceleration_table = create_acceleration_tables(dataframe)
sensor_velocity_table = create_velocity_tables(sensor_acceleration_table, times)
sensor_position_table = create_position_tables(sensor_velocity_table, times)
sensor_gyroscope_table = create_gyroscope_tables(dataframe)
rotational_quaternion_tables = create_rotational_quaternion_tables(sensor_gyroscope_table)
rotated_accel_vector_tables = create_rotated_accel_vector_tables(sensor_acceleration_table, rotational_quaternion_tables)

test_positions = create_position_tables(create_velocity_tables(rotated_accel_vector_tables, times), times)

def get_total_accel(accel_table):
    total_accel_list = np.zeros((len(accel_table), 1))
    for i in range(len(accel_table)):
        x = accel_table[i][0]
        y = accel_table[i][1]
        z = accel_table[i][2]
        total_accel_list[i] = np.sqrt(x**2 + y**2 + z**2)
    return total_accel_list

print(get_total_accel(sensor_acceleration_table))

# Plot Velocity
plt.figure(figsize=(10, 4))
plt.plot(times, sensor_velocity_table[:, 1], label='Velocity Y-sensor')
plt.plot(times, sensor_velocity_table[:, 2], label='Velocity Z-sensor')
plt.xlabel('Time')
plt.ylabel('Velocity')
plt.title('Sensor velocity vs Time')
plt.legend()

# Plot Position
plt.figure(figsize=(10, 4))
plt.plot(times, sensor_position_table[:, 0], label='Position X-sensor')
plt.plot(times, sensor_position_table[:, 1], label='Position Y-sensor')
plt.plot(times, sensor_position_table[:, 2], label='Position Z-sensor')
plt.xlabel('Time')
plt.ylabel('Position')
plt.title('Sensor position vs Time')
plt.legend()

# Plot Acceleration
plt.figure(figsize=(10, 4))
plt.plot(times, [a[0] for a in sensor_acceleration_table], label='Acceleration X-sensor', color='r', linestyle='-')
plt.plot(times, [a[1] for a in sensor_acceleration_table], label='Acceleration Y-sensor', color='g', linestyle='--')
plt.plot(times, [a[2] for a in sensor_acceleration_table], label='Acceleration Z-sensor', color='b', linestyle='-.')
plt.xlabel('Time')
plt.ylabel('Acceleration')
plt.title('Sensor acceleration vs Time')
plt.legend()
plt.grid(True)

# Plot Gyroscope Velocity
plt.figure(figsize=(10, 4))
plt.plot(times, [a[0] for a in sensor_gyroscope_table], label='Gyroscope X-sensor', color='r', linestyle='-')
plt.plot(times, [a[1] for a in sensor_gyroscope_table], label='Gyroscope Y-sensor', color='g', linestyle='--')
plt.plot(times, [a[2] for a in sensor_gyroscope_table], label='Gyroscope Z-sensor', color='b', linestyle='-.')
plt.xlabel('Time')
plt.ylabel('Gyro Velocity')
plt.title('Gyroscope Velocity vs Time')
plt.legend()
plt.grid(True)

# Plot REAL Position (TEST)
plt.figure(figsize=(10, 4))
plt.plot(times, test_positions[:, 0], label='Position X')
plt.plot(times, test_positions[:, 1], label='Position Y')
plt.plot(times, test_positions[:, 2], label='Position Z')
plt.xlabel('Time')
plt.ylabel('Position')
plt.title('Real position vs Time')
plt.legend()

def plot_path(positions):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    
    # Extract X, Y, Z coordinates from positions list
    X = [pos[0] for pos in positions]
    Y = [pos[1] for pos in positions]
    Z = [pos[2] for pos in positions]
    
    # Plot path
    ax.plot(X, Y, Z)
    
    # Label axes
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    
    plt.show()
    
plot_path(test_positions)


print("SUCCESFULLY RAN CELL CODE!")

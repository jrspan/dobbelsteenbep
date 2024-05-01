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
        times = data[0].tolist()
        return data, times
    except FileNotFoundError:
        raise FileNotFoundError(f"Data file not found in directory {filepath}")
        
def integrate_acceleration(velocity, acceleration, dt):
    return velocity + acceleration * dt

def integrate_velocity(position, velocity, dt):
    return position + velocity * dt

def create_acceleration_tables(data):
    acceleration_list = data.iloc[:, 1:4].values.tolist()
    return np.array(acceleration_list)
        
def create_velocity_tables(data):
    # Returns a list of predicted velocities for every timestep
    columns = [data[col].tolist() for col in data.columns]
    velocity_list = np.zeros((len(columns[1]), 3))
    if len(velocity_list) != len(columns[0]):
        raise IndexError('Length of times and accelerations do not match!')
    for i in range(1, len(columns[1])):
        dt = columns[0][i] - columns[0][i-1]
        vel_x = integrate_acceleration(velocity_list[i-1][0], columns[1][i-1], dt)
        vel_y = integrate_acceleration(velocity_list[i-1][1], columns[2][i-1], dt)
        vel_z = integrate_acceleration(velocity_list[i-1][2], columns[3][i-1], dt)
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
    

filename = "merged_testfile.csv"
dataframe, times = load_datafile(filename)
sensor_acceleration_table = create_acceleration_tables(dataframe)
sensor_velocity_table = create_velocity_tables(dataframe)
sensor_position_table = create_position_tables(sensor_velocity_table, times)

print(sensor_acceleration_table)

# Plot Velocity
plt.subplot(2, 1, 1)  # 2 rows, 1 column, plot 1
plt.plot(times, sensor_velocity_table[:, 0], label='Velocity X-sensor')
plt.plot(times, sensor_velocity_table[:, 1], label='Velocity Y-sensor')
plt.plot(times, sensor_velocity_table[:, 2], label='Velocity Z-sensor')
plt.xlabel('Time')
plt.ylabel('Velocity')
plt.title('Sensor velocity vs Time')
plt.legend()

# Plot Position
plt.subplot(2, 1, 2)  # 2 rows, 1 column, plot 2
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


plt.tight_layout()  # Adjust layout to prevent overlap
plt.show()

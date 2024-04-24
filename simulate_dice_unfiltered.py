import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

def get_filepath(filename: str):
    filepath = os.path.dirname((os.path.abspath(__file__)))
    return os.path.join(filepath, filename)

def load_data(acceleration_file, angular_velocity_file):
    try:
        acceleration_data = pd.read_csv(acceleration_file, header=None, skiprows=1)
        acceleration_xyz = [row.tolist() for _, row in acceleration_data.iterrows()]
    except FileNotFoundError:
        raise FileNotFoundError("Accelerometer Data File Not found")
        
    try:
        angular_velocity_data = pd.read_csv(angular_velocity_file, header=None, skiprows=1)
        angular_velocity_xyz = [row.tolist() for _, row in angular_velocity_data.iterrows()]
    except FileNotFoundError:
        raise FileNotFoundError("Gyroscope Data File Not found")
    
    try:
        t1 = acceleration_data.iloc[0, 0]
        t2 = acceleration_data.iloc[1, 0]
        dt = t2 - t1
    except:
        raise IndexError("Only one row with data exists!")    
    
    return acceleration_xyz, angular_velocity_xyz, dt


def integrate_acceleration(velocity, acceleration, dt):
    return velocity + acceleration * dt

def integrate_angular_velocity(orientation, angular_velocity, dt):
    return orientation + angular_velocity * dt

def detect_throw_end(acceleration_data, gyroscope_data):
    min_length = min(len(acceleration_data), len(gyroscope_data))
    return min_length

def roll_dice(accelerometer_data, gyroscope_data, dt):
    num_steps = detect_throw_end(accelerometer_data, gyroscope_data)

    position = np.zeros((num_steps, 3))
    orientation = np.zeros((num_steps, 3))
    measured_acceleration = np.zeros((num_steps, 3))
    measured_angular_velocity = np.zeros((num_steps, 3))

    for i in range(1, num_steps):
        _, x_accel, y_accel, z_accel = accelerometer_data[i]
        _, x_gyro, y_gyro, z_gyro = gyroscope_data[i]

        acceleration = np.array([x_accel, y_accel, z_accel])
        measured_acceleration[i] = integrate_acceleration(measured_acceleration[i-1], acceleration, dt)

        angular_velocity = np.array([x_gyro, y_gyro, z_gyro])
        measured_angular_velocity[i] = angular_velocity

        position[i] = integrate_acceleration(position[i-1], measured_acceleration[i], dt)
        orientation[i] = integrate_angular_velocity(orientation[i-1], measured_angular_velocity[i], dt)

    return position, orientation, measured_acceleration, measured_angular_velocity


filepath_accelerometer = get_filepath("acceleration_data.csv")
filepath_gyroscope = get_filepath("gyroscope_data.csv")

acceleration_xyz, angular_velocity_xyz, dt = load_data(filepath_accelerometer, filepath_gyroscope)

print("Data loaded successfully!")

position, orientation, measured_acceleration, measured_angular_velocity = roll_dice(acceleration_xyz, angular_velocity_xyz, dt)

fig, axs = plt.subplots(3, 1, figsize=(10, 12))
axs[0].plot(position[:, 0], label='X position')
axs[0].plot(position[:, 1], label='Y position')
axs[0].plot(position[:, 2], label='Z position')
axs[0].set_xlabel('Time step')
axs[0].set_ylabel('Position (m)')
axs[0].legend()
axs[0].grid(True)

axs[1].plot(np.degrees(orientation[:, 0]), label='Roll')
axs[1].plot(np.degrees(orientation[:, 1]), label='Pitch')
axs[1].plot(np.degrees(orientation[:, 2]), label='Yaw')
axs[1].set_xlabel('Time step')
axs[1].set_ylabel('Orientation (degrees)')
axs[1].legend()
axs[1].grid(True)

axs[2].plot(measured_acceleration[:, 0], label='X acceleration')
axs[2].plot(measured_acceleration[:, 1], label='Y acceleration')
axs[2].plot(measured_acceleration[:, 2], label='Z acceleration')
axs[2].set_xlabel('Time step')
axs[2].set_ylabel('Acceleration (m/s^2)')
axs[2].legend()
axs[2].grid(True)

plt.tight_layout()
plt.show()

# Basic import modules
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

# Define path location
# This command ensure that it can open all files if they are stored in the same directory as this code.
os.chdir((os.path.dirname(os.path.abspath(__file__))))

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

def parse_row(row):
    # Split the row by commas and convert to floats
    values = [float(x) for x in row.split(",")]
    return values

def load_data(acceleration_file, angular_velocity_file):
    try:
        # Load accelerometer data
        acceleration_data = pd.read_csv(acceleration_file, header=0)
        # Skip the header row and parse the data
        acceleration_xyz = np.array([parse_row(row) for row in acceleration_data[0]])
    except FileNotFoundError:
        raise FileNotFoundError("Accelerometer Data File Not found")
        
    try:
        # Load gyroscope data
        angular_velocity_data = pd.read_csv(angular_velocity_file, header=0)
        # Skip the header row and parse the data
        angular_velocity_xyz = np.array([parse_row(row) for row in angular_velocity_data[0]])
    except FileNotFoundError:
        raise FileNotFoundError("Gyroscope Data File Not found")
    
    return acceleration_xyz, angular_velocity_xyz


def integrate_acceleration(acceleration, dt):
    return acceleration * dt

def integrate_velocity(velocity, acceleration, dt):
    return velocity + acceleration * dt

def integrate_angular_velocity(angular_velocity, dt):
    return angular_velocity * dt

def detect_throw_start(acceleration):
    # Calculate total acceleration magnitude
    total_acceleration = np.linalg.norm(acceleration, axis=1)
    
    # Find the index where total acceleration starts decreasing
    start_index = 0
    for i in range(1, len(total_acceleration)):
        if total_acceleration[i] < total_acceleration[i-1] and total_acceleration[i] < total_acceleration[i-2]:
            start_index = i
            break
    return start_index

def roll_dice(acceleration_xyz, angular_velocity_xyz, dt):
    # Detect the start of the throw
    start_index = detect_throw_start(acceleration_xyz)
    
    # Trim acceleration and angular velocity arrays from the detected start index
    acceleration_xyz = acceleration_xyz[start_index:]
    angular_velocity_xyz = angular_velocity_xyz[start_index:]
    
    num_steps = len(acceleration_xyz)

    # Initial conditions
    position = np.zeros((num_steps, 3))
    velocity = np.zeros((num_steps, 3))
    orientation = np.zeros((num_steps, 3))  # Euler angles (roll, pitch, yaw)
    angular_displacement = np.zeros((num_steps, 3))

    # Placeholder for measured accelerations and angular velocities
    measured_acceleration = acceleration_xyz
    measured_angular_velocity = angular_velocity_xyz

    for i in range(1, num_steps):
        # Integrate linear motion
        acceleration = integrate_acceleration(measured_acceleration[i], dt)
        velocity[i] = integrate_velocity(velocity[i-1], acceleration, dt)
        position[i] = integrate_velocity(position[i-1], velocity[i], dt)

        # Integrate angular motion
        angular_velocity = integrate_angular_velocity(measured_angular_velocity[i], dt)
        angular_displacement[i] = integrate_angular_velocity(angular_velocity, dt)
        orientation[i] = orientation[i-1] + angular_displacement[i]

    return position, orientation, measured_acceleration, measured_angular_velocity

# Specify file paths
current_directory = os.getcwd()
acceleration_file = os.path.join(current_directory, "accelerometer_data.csv")
angular_velocity_file = os.path.join(current_directory, "gyroscope_data.csv")

# Time step size (seconds)
dt = 0.01

# Load data from CSV files
acceleration_xyz, angular_velocity_xyz = load_data(acceleration_file, angular_velocity_file)

# Simulate dice trajectory
position, orientation, measured_acceleration, measured_angular_velocity = roll_dice(acceleration_xyz, angular_velocity_xyz, dt)

# Plot trajectory
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

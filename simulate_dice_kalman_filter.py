import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

class KalmanFilter:
    def __init__(self, initial_state, initial_covariance, process_noise, measurement_noise):
        # Initialize the state vector
        self.x = initial_state
        
        # Initialize the state covariance matrix
        self.P = initial_covariance
        
        # Initialize the process noise covariance matrix
        self.Q = process_noise
        
        # Initialize the measurement noise covariance matrix
        self.R = measurement_noise
        
    def predict(self, F, B, u):
        # Prediction step
        # F: State transition matrix
        # B: Control input matrix
        # u: Control input vector
        
        # Predicted state estimate
        self.x = np.dot(F, self.x) + np.dot(B, u)
        
        # Predicted state covariance
        self.P = np.dot(np.dot(F, self.P), F.T) + self.Q
        
    def update(self, z, H):
        # Update step
        # z: Measurement vector
        # H: Measurement matrix
        
        # Innovation or measurement residual
        y = z - np.dot(H, self.x)
        
        # Innovation covariance
        S = np.dot(np.dot(H, self.P), H.T) + self.R
        
        # Kalman gain
        K = np.dot(np.dot(self.P, H.T), np.linalg.inv(S))
        
        # Update state estimate
        self.x = self.x + np.dot(K, y)
        
        # Update state covariance
        self.P = self.P - np.dot(np.dot(K, H), self.P)
        
        return self.x


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

def detect_throw_end(acceleration_data, gyroscope_data):
    min_length = min(len(acceleration_data), len(gyroscope_data))
    return min_length

def roll_dice_with_kalman_filter(accelerometer_data, gyroscope_data, dt, initial_orientation):
    num_steps = detect_throw_end(accelerometer_data, gyroscope_data)

    position = np.zeros((num_steps, 3))
    orientation = np.zeros((num_steps, 4))  # Represented as quaternions
    measured_acceleration = np.zeros((num_steps, 3))
    measured_angular_velocity = np.zeros((num_steps, 3))

    # Define the Kalman filter parameters
    initial_state = np.zeros(4)  # Initial orientation (quaternion)
    initial_covariance = np.eye(4) * 0.1  # Initial covariance matrix
    process_noise = np.eye(4) * 1e-5  # Process noise covariance matrix
    measurement_noise = np.eye(3) * 1e-2  # Measurement noise covariance matrix
    filter = KalmanFilter(initial_state, initial_covariance, process_noise, measurement_noise)

    orientation[0] = initial_orientation

    for i in range(1, num_steps):
        _, x_accel, y_accel, z_accel = accelerometer_data[i]
        _, x_gyro, y_gyro, z_gyro = gyroscope_data[i]

        acceleration = np.array([x_accel, y_accel, z_accel])
        measured_acceleration[i] = integrate_acceleration(measured_acceleration[i-1], acceleration, dt)

        angular_velocity = np.array([x_gyro, y_gyro, z_gyro])

        # Predict the next state with the Kalman filter
        filter.predict(np.eye(4), np.zeros((4, 3)), np.zeros(3))
        
        # Update the Kalman filter with the gyroscope data
        filter.update(angular_velocity, np.eye(4)[:3])

        # Get the filtered orientation estimate
        filtered_orientation = filter.x

        # Update the orientation with the filtered estimate
        orientation[i] = filtered_orientation

        position[i] = integrate_acceleration(position[i-1], measured_acceleration[i], dt)

    return position, orientation, measured_acceleration, measured_angular_velocity

# Define the initial orientation (quaternion representing no rotation)
initial_orientation = np.array([1.0, 0.0, 0.0, 0.0])

# Load data from CSV files
filepath_accelerometer = get_filepath("acceleration_data.csv")
filepath_gyroscope = get_filepath("gyroscope_data.csv")
acceleration_xyz, angular_velocity_xyz, dt = load_data(filepath_accelerometer, filepath_gyroscope)

# Perform the simulation with the Kalman filter
position_filtered, orientation_filtered, measured_acceleration_filtered, measured_angular_velocity_filtered = roll_dice_with_kalman_filter(
    acceleration_xyz, angular_velocity_xyz, dt, initial_orientation
)

# Plot the results
fig, axs = plt.subplots(3, 1, figsize=(10, 12))
axs[0].plot(position_filtered[:, 0], label='X position (filtered)')
axs[0].plot(position_filtered[:, 1], label='Y position (filtered)')
axs[0].plot(position_filtered[:, 2], label='Z position (filtered)')
axs[0].set_xlabel('Time step')
axs[0].set_ylabel('Position (m)')
axs[0].legend()
axs[0].grid(True)

axs[1].plot(orientation_filtered[:, 0], label='Quaternion W (filtered)')
axs[1].plot(orientation_filtered[:, 1], label='Quaternion X (filtered)')
axs[1].plot(orientation_filtered[:, 2], label='Quaternion Y (filtered)')
axs[1].plot(orientation_filtered[:, 3], label='Quaternion Z (filtered)')
axs[1].set_xlabel('Time step')
axs[1].set_ylabel('Quaternion')
axs[1].legend()
axs[1].grid(True)

axs[2].plot(measured_acceleration_filtered[:, 0], label='X acceleration (measured)')
axs[2].plot(measured_acceleration_filtered[:, 1], label='Y acceleration (measured)')
axs[2].plot(measured_acceleration_filtered[:, 2], label='Z acceleration (measured)')
axs[2].set_xlabel('Time step')
axs[2].set_ylabel('Acceleration (m/s^2)')
axs[2].legend()
axs[2].grid(True)

plt.tight_layout()
plt.show()

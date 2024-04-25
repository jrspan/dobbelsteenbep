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

def get_dice_number_from_orientation(orientation):
    # Define the orientations of each dice number (assuming a standard dice)
    orientations = {
        1: [1, 0, 0, 0],  # Number 1 is facing in line with the X-axis
        2: [0, 1, 0, 0],  # Number 2 is facing in line with the Y-axis
        3: [0, 0, 1, 0],  # Number 3 is facing in line with the Z-axis
        4: [0, 0, -1, 0], # Number 4 is facing opposite to the Z-axis
        5: [0, -1, 0, 0], # Number 5 is facing opposite to the Y-axis
        6: [-1, 0, 0, 0]  # Number 6 is facing opposite to the X-axis
    }
    
    # Calculate the dot product of the current orientation with each number orientation
    dot_products = {number: np.dot(orientation, orientations[number]) for number in orientations}
    
    # Determine the number with the highest dot product (indicating closest alignment)
    top_number = max(dot_products, key=dot_products.get)
    
    return top_number

def get_filepath(filename: str):
    filepath = os.path.dirname((os.path.abspath(__file__)))
    return os.path.join(filepath, filename)

def load_data(data_file):
    try:
        data = pd.read_csv(data_file, header=None, skiprows=1)
        combined_data = data.iloc[:, 1:].values.tolist()
        t1 = data.iloc[0, 0]
        t2 = data.iloc[1, 0]
        dt = t2 - t1
    except FileNotFoundError:
        raise FileNotFoundError("Data File Not found")
    except:
        raise IndexError("Only one row with data exists!")    
    
    return combined_data, dt

def integrate_acceleration(velocity, acceleration, dt):
    return velocity + acceleration * dt

def detect_throw_end(acceleration_data, gyroscope_data):
    min_length = min(len(acceleration_data), len(gyroscope_data))
    return min_length

def rotate_quaternion(quaternion, axis, angle):
    # Normalize the axis
    axis = (axis / np.linalg.norm(axis)).astype(np.float64)

    # Compute the quaternion representing the rotation
    rotation_quaternion = np.concatenate([[np.cos(angle / 2)], np.sin(angle / 2) * axis])
    
    # Perform quaternion multiplication
    result_quaternion = quaternion_multiply(rotation_quaternion, quaternion)
    
    # Convert to integers
    result_quaternion = np.round(result_quaternion).astype(int)
    
    return result_quaternion

def roll_dice_with_kalman_filter(combined_data, dt, initial_orientation):
    num_steps = len(combined_data)

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
        x_accel, y_accel, z_accel, x_gyro, y_gyro, z_gyro = combined_data[i]

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

# Function to compute quaternion multiplication
def quaternion_multiply(q1, q2):
    w1, x1, y1, z1 = q1
    w2, x2, y2, z2 = q2
    w = w1 * w2 - x1 * x2 - y1 * y2 - z1 * z2
    x = w1 * x2 + x1 * w2 + y1 * z2 - z1 * y2
    y = w1 * y2 - x1 * z2 + y1 * w2 + z1 * x2
    z = w1 * z2 + x1 * y2 - y1 * x2 + z1 * w2
    return np.array([w, x, y, z])

# Define the initial orientation based on the specifications
initial_orientation = np.array([1.0, 0.0, 0.0, 0.0])  # Identity quaternion

# Rotate the Z-axis by 50 degrees around the Y-axis
z_axis = np.array([0, 0, 1])
y_axis = np.array([0, 1, 0])
angle_degrees = 50
angle_radians = np.radians(angle_degrees)
initial_orientation = rotate_quaternion(initial_orientation, y_axis, angle_radians)

# Rotate the Y-axis by 90 degrees around the resulting Z-axis
initial_orientation = rotate_quaternion(initial_orientation, z_axis, np.radians(90))

# Load data from CSV file
filepath_data = get_filepath("merged_data_file_testv1.csv")
combined_data, dt = load_data(filepath_data)

# Perform the simulation with the Kalman filter
position_filtered, orientation_filtered, measured_acceleration_filtered, measured_angular_velocity_filtered = roll_dice_with_kalman_filter(
    combined_data, dt, initial_orientation
)

# Determine the number on the top side of the dice for each time step
dice_numbers = [get_dice_number_from_orientation(orientation) for orientation in orientation_filtered]

# Plot the results
fig, axs = plt.subplots(5, 1, figsize=(10, 20))
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

# Calculate total distance traveled
total_distance = np.linalg.norm(position_filtered, axis=1)
axs[3].plot(total_distance, label='Total Distance Traveled')
axs[3].set_xlabel('Time step')
axs[3].set_ylabel('Total Distance (m)')
axs[3].legend()
axs[3].grid(True)

# Plot the number on the top side of the dice
axs[4].plot(dice_numbers, label='Top Side Dice Number')
axs[4].set_xlabel('Time step')
axs[4].set_ylabel('Dice Number')
axs[4].legend()
axs[4].grid(True)

plt.tight_layout()
plt.show()

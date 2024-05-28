import time
import warnings
from help_functies import *
import pandas as pd
warnings.simplefilter(action='ignore', category=FutureWarning)

# Create rotated accelerometer lists
xr_acc_list = []
yr_acc_list = []
zr_acc_list = []
xr_acc_stds_list = []
yr_acc_stds_list = []
zr_acc_stds_list = []

# Create rotated gyroscope lists
xr_gyro_list = []
yr_gyro_list = []
zr_gyro_list = []
xr_gyro_stds_list = []
yr_gyro_stds_list = []
zr_gyro_stds_list = []


def calibrate(dob):
    for i in range(1, 4):
        print("Leg de dobbelsteen met nummer ", i, " boven")
        print("wacht 3 secondes")
        time.sleep(3)
        dob.connect()

        #Log the data of the dice
        dob.log(2, 200, 8, 125)

        # Download the logged data from the dice
        dob.download()
        data = dob.datadf
        data = remove_nan(data)
        q1 = np.array([-0.94614393, 0.00757503, 0.32350718, -0.00986897])
        for i, row in data.iterrows():
            data.loc[i, 'x_acc'], data.loc[i, 'y_acc'], data.loc[i, 'z_acc'] = rotate_vector(np.array([row['x_acc'], row['y_acc'], row['z_acc']]), q1)
            data.loc[i, 'x_gyro'], data.loc[i, 'y_gyro'], data.loc[i, 'z_gyro'] = rotate_vector(np.array([row['x_gyro'], row['y_gyro'], row['z_gyro']]), q1)

        # Calculate the means of the accelerometer output
        x_acc = np.mean(data['x_acc'])
        y_acc = np.mean(data['y_acc'])
        z_acc = np.mean(data['z_acc'])
        acc_means = np.array([x_acc,y_acc,z_acc])

        #Calculate the standard deviations of the accelerometer output
        x_std = np.std(data['x_acc'])
        y_std = np.std(data['y_acc'])
        z_std = np.std(data['z_acc'])
        acc_stds = np.array([x_std, y_std, z_std])

        #Append the rotated means of the accelerometer to the list
        xr_acc_list.append(acc_means[0])
        yr_acc_list.append(acc_means[1])
        zr_acc_list.append(acc_means[2])

        #Append the rotated standard deviations of the accelerometer to the list
        xr_acc_stds_list.append(acc_stds[0])
        yr_acc_stds_list.append(acc_stds[1])
        zr_acc_stds_list.append(acc_stds[2])

        # Calculate the means of the gyroscope output
        x_gyro = np.mean(data['x_gyro'])
        y_gyro = np.mean(data['y_gyro'])
        z_gyro = np.mean(data['z_gyro'])
        gyro_means = np.array([x_gyro, y_gyro, z_gyro])

        # Calculate the standard deviations of the gyroscope output
        x_gyro_std = np.std(data['x_gyro'])
        y_gyro_std = np.std(data['y_gyro'])
        z_gyro_std = np.std(data['z_gyro'])
        gyro_stds = np.array([x_gyro_std, y_gyro_std, z_gyro_std])

        # Append the rotated means of the gyroscope output to the list
        xr_gyro_list.append(gyro_means[0])
        yr_gyro_list.append(gyro_means[1])
        zr_gyro_list.append(gyro_means[2])

        # Append the rotated standard deviations of the gyroscope output to the list
        xr_gyro_stds_list.append(gyro_stds[0])
        yr_gyro_stds_list.append(gyro_stds[1])
        zr_gyro_stds_list.append(gyro_stds[2])

    #Create DataFrames from the list of rotated accelerometer means and standard deviations
    acc_means_init_df = pd.DataFrame({"xr_acc": xr_acc_list, "yr_acc": yr_acc_list, "zr_acc": zr_acc_list})
    acc_stds_init_df = pd.DataFrame({"xr_std": xr_acc_stds_list, "yr_std": yr_acc_stds_list, "zr_std": zr_acc_stds_list})

    # Create DataFrames from the list of gyroscope means and standard deviations
    gyro_df = pd.DataFrame({'xr_gyro': xr_gyro_list, 'yr_gyro': yr_gyro_list, 'zr_gyro': zr_gyro_list})
    gyro_stds_df = pd.DataFrame({'xr_gyro_std': xr_gyro_stds_list, 'yr_gyro_std': yr_gyro_stds_list, 'zr_gyro_std': zr_gyro_stds_list})

    # Calibration algorithm
    # Remove the gravity for the bias of the accelerometer
    xr_bias_acc = 1-np.abs(xr_acc_list[2])
    yr_bias_acc = 1-np.abs(yr_acc_list[1])
    zr_bias_acc = 1-np.abs(zr_acc_list[0])
    bias = np.array([xr_bias_acc, yr_bias_acc, zr_bias_acc])

    # Accelerometer standard deviations
    xr_std = xr_acc_stds_list[2]
    yr_std = yr_acc_stds_list[1]
    zr_std = zr_acc_stds_list[0]
    acc_std = np.array([xr_std, yr_std, zr_std])

    # Biases for the gyroscope
    xr_gyro_bias = np.mean(gyro_df['xr_gyro'])
    yr_gyro_bias = np.mean(gyro_df['yr_gyro'])
    zr_gyro_bias = np.mean(gyro_df['zr_gyro'])
    gyro_bias = np.array([xr_gyro_bias,yr_gyro_bias,zr_gyro_bias])

    # Standard deviations for the gyroscope
    xr_gyro_std = np.mean(gyro_stds_df['xr_gyro_std'])
    yr_gyro_std = np.mean(gyro_stds_df['yr_gyro_std'])
    zr_gyro_std = np.mean(gyro_stds_df['zr_gyro_std'])
    gyro_std = np.array([xr_gyro_std, yr_gyro_std, zr_gyro_std])

    output = {
        'gyro bias': gyro_bias,
        'acc bias': bias,
        'gyro std': gyro_std,
        'acc std': acc_std
    }
    return output
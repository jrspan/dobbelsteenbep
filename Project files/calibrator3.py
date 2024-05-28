import numpy as np
from dobbel import dobbellogger
from help_functies import *
import time
import pandas as pd

def calibrate(dob, logtime, waittime, freq, acc_range, gyro_range, rotation_quat=np.array([1,0,0,0])):
    acc_means = []
    gyro_means = []
    acc_stds = []
    gyro_stds = []
    for i in range(6):
        print("Leg de dobbelsteen met nummer ", i + 1, " boven")
        print(f"Wacht {waittime} secondes")
        time.sleep(waittime)
        dob.connect()

        #Log the data of the dice
        dob.log(logtime, freq, acc_range, gyro_range)

        # Download the logged data from the dice
        dob.download()
        data = dob.datadf
        data = remove_nan(data)
        data = rotate_data(data, rotation_quat)
        acc_zxyyxz = [data['z_acc'], data['x_acc'], data['y_acc'], data['y_acc'], data['x_acc'], data['z_acc']]
        gyro_ar = np.array([data['x_gyro'].tolist(), data['y_gyro'].tolist(), data['z_gyro'].tolist()]).T

        acc_means.append(np.mean(acc_zxyyxz[i]))
        gyro_means.append(np.mean(gyro_ar, axis=0))
        acc_stds.append(np.std(acc_zxyyxz[i]))
        gyro_stds.append(np.std(gyro_ar, axis=0))

    acc_values = np.array([acc_means[i] for i in [1,4,2,3,0,5]])
    acc_stds_out = np.array([np.mean([acc_stds[i], acc_stds[i+3]]) for i in range(3)])
    gyro_means = np.reshape(np.concatenate(gyro_means), (6, 3))
    gyro_means = np.mean(gyro_means, axis=0)
    gyro_stds = np.reshape(np.concatenate(gyro_stds), (6, 3))
    gyro_stds = np.mean(gyro_stds, axis=0)

    cali = {
        'gyro bias': gyro_means,
        'gyro std': gyro_stds,
        'acc values': acc_values,
        'acc std': acc_stds_out
    }

    dob.disconnect()

    return cali
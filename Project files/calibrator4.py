import numpy as np
from dobbel import dobbellogger
from help_functies import *
from calibrator3 import calibrate
from matrix_helper import *
import matplotlib.pyplot as plt
import pandas as pd
import time

def calibrate(dob, logtime, waittime, freq, acc_range, gyro_range):
    acc_stds = []
    gyro_stds = []
    sides = {}
    gyro_biasses = []
    acc_biasses = []
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

        means = {}
        stds = {}
        for column in data.columns:
            means[column] = data[column].mean()
            stds[column] = data[column].std()
        sides[i+1] = (means, stds)

    for i in [(2, 5)]: #, (3, 4), (1, 6)]:
        gyro_means_pos = np.array([sides[i[0]][0]['x_gyro'], sides[i[0]][0]['y_gyro'], sides[i[0]][0]['z_gyro']])
        gyro_means_neg = np.array([sides[i[1]][0]['x_gyro'], sides[i[1]][0]['y_gyro'], sides[i[1]][0]['z_gyro']])

        gyro_stds_pos = np.array([sides[i[0]][1]['x_gyro'], sides[i[0]][1]['y_gyro'], sides[i[0]][1]['z_gyro']])
        gyro_stds_neg = np.array([sides[i[1]][1]['x_gyro'], sides[i[1]][1]['y_gyro'], sides[i[1]][1]['z_gyro']])

        acc_means_pos = np.array([sides[i[0]][0]['x_acc'], sides[i[0]][0]['y_acc'], sides[i[0]][0]['z_acc']])
        acc_means_neg = np.array([sides[i[1]][0]['x_acc'], sides[i[1]][0]['y_acc'], sides[i[1]][0]['z_acc']])

        acc_stds_pos = np.array([sides[i[0]][1]['x_acc'], sides[i[0]][1]['y_acc'], sides[i[0]][1]['z_acc']])
        acc_stds_neg = np.array([sides[i[1]][1]['x_acc'], sides[i[1]][1]['y_acc'], sides[i[1]][1]['z_acc']])

        gyro_biasses.append([gyro_means_pos, gyro_means_neg])
        gyro_stds.append([gyro_stds_pos, gyro_stds_neg])
        acc_biasses.append(acc_means_pos + acc_means_neg)
        acc_stds.append([acc_stds_pos, acc_stds_neg])

    print(gyro_biasses)
    print(acc_biasses)

    gyro_bias = np.mean(np.reshape(np.concatenate(gyro_biasses), (6, 3)), axis=0)
    gyro_stds = np.std(np.reshape(np.concatenate(gyro_stds), (6, 3)), axis=0)

    acc_bias = 0.5 * np.mean(np.reshape(np.concatenate(acc_biasses), (3, 3)), axis=0)
    acc_stds = np.std(np.reshape(np.concatenate(acc_stds), (6, 3)), axis=0)

    cali = {
        'gyro bias': gyro_bias,
        'gyro std': gyro_stds,
        'acc bias': acc_bias,
        'acc std': acc_stds
    }

    return cali


def rotate_cali(dob, cali, logtime, waittime, freq, acc_range, gyro_range):
    print('Leg de dobbelsteen met de 1 naarboven')
    print(f'Wacht {waittime} seconden')
    time.sleep(waittime)
    print(f'Loggen voor {logtime} seconden')

    dob.connect()
    dob.log(logtime, freq, acc_range, gyro_range)
    dob.download()
    data = dob.datadf
    data = remove_nan(data)
    data['x_acc'] = data['x_acc'] - cali['acc bias'][0]
    data['y_acc'] = data['y_acc'] - cali['acc bias'][1]
    data['z_acc'] = data['z_acc'] - cali['acc bias'][2]
    data['x_gyro'] = data['x_gyro'] - cali['gyro bias'][0]
    data['y_gyro'] = data['y_gyro'] - cali['gyro bias'][1]
    data['z_gyro'] = data['z_gyro'] - cali['gyro bias'][2]
    y_mean_1 = np.mean(np.array([data['x_acc'], data['y_acc'], data['z_acc']]), axis=1)

    print(f'Wacht {waittime} seconden')
    time.sleep(waittime)
    print(f'Loggen voor {logtime} seconden')

    dob.connect()
    dob.log(logtime, freq, acc_range, gyro_range)
    dob.download()
    data = dob.datadf
    data = remove_nan(data)
    data['x_acc'] = data['x_acc'] - cali['acc bias'][0]
    data['y_acc'] = data['y_acc'] - cali['acc bias'][1]
    data['z_acc'] = data['z_acc'] - cali['acc bias'][2]
    data['x_gyro'] = data['x_gyro'] - cali['gyro bias'][0]
    data['y_gyro'] = data['y_gyro'] - cali['gyro bias'][1]
    data['z_gyro'] = data['z_gyro'] - cali['gyro bias'][2]
    y_mean_2 = np.mean(np.array([data['x_acc'], data['y_acc'], data['z_acc']]), axis=1)

    gb = y_mean_1 / np.linalg.norm(y_mean_1)
    gn = np.array([0, 0, 1])
    mb = np.cross(gb, np.cross(y_mean_2 / np.linalg.norm(y_mean_2), gb))
    mn = np.array([1, 0, 0])

    A = - np.matmul(left_quat_mul(np.array([0, *gn])), right_quat_mul(np.array([0, *gb]))) - np.matmul(left_quat_mul(np.array([0, *mn])), right_quat_mul(np.array([0, *mb])))
    eigenvalues, eigenvectors = np.linalg.eigh(A)
    max_eigenvalue_index = np.argmax(eigenvalues)
    max_eigenvector = eigenvectors[:, max_eigenvalue_index]

    return max_eigenvector
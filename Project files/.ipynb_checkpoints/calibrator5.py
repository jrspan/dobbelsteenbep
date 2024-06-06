from help_functies import *
from matrix_helper import *
import time


def calibrate_rot_bias(dob, logtime, waittime, freq, acc_range, gyro_range):
    measurements = []
    Y_list = []
    gyro_data = []
    y_means = []
    for i, (column, sign) in zip(range(6), [(2, 1), (0, 1), (1, 1), (1, -1), (0, -1), (2, -1)]):
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

        y_means.append(np.mean(np.array([data['x_acc'], data['y_acc'], data['z_acc']]), axis=1))

        acc_arr = np.array([data['x_acc'], data['y_acc'], data['z_acc']])
        measurements.append(acc_arr.T)
        y_arr = np.zeros((acc_arr.shape[1], 3))
        y_arr[:, column] = sign
        Y_list.append(y_arr)

        gyro_arr = np.array([data['x_gyro'].mean(), data['y_gyro'].mean(), data['z_gyro'].mean()])
        gyro_data.append(gyro_arr)


    Y = np.concatenate(Y_list)
    w = np.concatenate(measurements)
    w = np.hstack((w, np.ones((w.shape[0], 1))))
    X = np.matmul(np.matmul(np.linalg.inv(np.matmul(w.T, w)), w.T), Y)

    acc_bias = np.reshape(X[3, :], (3, 1))
    acc_rotmat = X[0:3, :].T

    gyro_data = np.reshape(np.concatenate(gyro_data), (6, 3))
    gyro_bias = np.mean(gyro_data, axis=0)

    gb = y_means[0] / np.linalg.norm(y_means[0])
    gnl = np.array([0, 0, 1])
    mb = np.cross(gb, np.cross(y_means[1] / np.linalg.norm(y_means[1]), gb))
    mn = np.array([1, 0, 0])

    A = - np.matmul(left_quat_mul(np.array([0, *gnl])), right_quat_mul(np.array([0, *gb]))) - np.matmul(left_quat_mul(np.array([0, *mn])), right_quat_mul(np.array([0, *mb])))
    eigenvalues, eigenvectors = np.linalg.eigh(A)
    max_eigenvalue_index = np.argmax(eigenvalues)
    rot_quat = eigenvectors[:, max_eigenvalue_index]

    cali = {
        'acc rotmat': acc_rotmat,
        'acc bias': acc_bias,
        'gyro bias': gyro_bias,
        'rot quat gyro': rot_quat
    }


    return cali


def rotate_remove_bias(data, cali):
    rotmat, biasvec, gyro_bias = cali['acc rotmat'], cali['acc bias'], cali['gyro bias']
    data_nb = data.copy()
    data_nb['x_gyro'] = data_nb['x_gyro'] - gyro_bias[0]
    data_nb['y_gyro'] = data_nb['y_gyro'] - gyro_bias[1]
    data_nb['z_gyro'] = data_nb['z_gyro'] - gyro_bias[2]

    no_bias_list = []
    for i, row in data.iterrows():
        meas = np.array([[row['x_acc']], [row['y_acc']], [row['z_acc']]])
        no_bias = np.matmul(rotmat, meas) + np.reshape(biasvec, (3, 1))
        no_bias_list.append(np.reshape(no_bias, 3))

    no_bias = np.reshape(np.concatenate(no_bias_list), (len(no_bias_list), 3))
    data_nb['x_acc'] = no_bias[:, 0]
    data_nb['y_acc'] = no_bias[:, 1]
    data_nb['z_acc'] = no_bias[:, 2]

    for i, row in data_nb.iterrows():
        data_nb.loc[i, 'x_gyro'], data_nb.loc[i, 'y_gyro'], data_nb.loc[i, 'z_gyro'] = rotate_vector(np.array([row['x_gyro'], row['y_gyro'], row['z_gyro']]), cali['rot quat gyro'])

    return data_nb


def cali_std(dob, logtime, freq, acc_range, gyro_range):
    print('Leg de dobbelsteen stil')
    dob.connect()
    dob.log(logtime, freq, acc_range, gyro_range)
    dob.download()
    data = dob.datadf
    gyro_stds = np.array([data['x_gyro'].std(), data['y_gyro'].std(), data['z_gyro'].std()])
    acc_stds = np.array([data['x_acc'].std(), data['y_acc'].std(), data['z_acc'].std()])

    return {'gyro stds': gyro_stds, 'acc stds': acc_stds}

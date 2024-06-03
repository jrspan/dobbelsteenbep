import numpy as np

def expq(vector, multiplier=1):
    x, y, z = vector[0] * multiplier, vector[1] * multiplier, vector[2]  * multiplier
    absq = (x ** 2 + y ** 2 + z ** 2) ** 0.5
    if absq == 0:
        return np.array([1, 0, 0, 0])
    w = np.cos(absq)
    sinabs = np.sin(absq)
    xq = x * sinabs / absq
    yq = y * sinabs / absq
    zq = z * sinabs / absq
    return np.array([w, xq, yq, zq])

def quat_mul(p, q):
    p0 = p[0]
    q0 = q[0]
    pv = p[1:]
    qv = q[1:]
    out0 = p0 * q0 - np.dot(pv, qv)
    outv = p0 * qv + q0 * pv + np.cross(pv, qv)
    out = np.array([out0, *outv])
    return out


def quaternion_conjugate(q):
    w, x, y, z = q
    return np.array([w, -x, -y, -z])


# Actual Rotation Fuction - Input = Acceleration vector = 1x3 , rotation_quaternion = 1*4
def rotate_vector(vector, rotation_quaternion):
    # Convert the vector to a quaternion
    vector_quaternion = np.concatenate(([0], vector))

    # Calculate the rotated quaternion
    rotated_quaternion = quat_mul(rotation_quaternion, quat_mul(vector_quaternion, quaternion_conjugate(rotation_quaternion)))

    # Extract the rotated vector from the quaternion
    rotated_vector = rotated_quaternion[1:]

    return np.array(rotated_vector)

def quat_to_euler(q):
    w, x, y, z = q[0], q[1], q[2], q[3]
    psi = np.arctan((2*x*y-2*w*z)/((2*w**2)+(2*x**2)-1))
    theta = -np.arcsin(2*x*z+2*w*y)
    phi = np.arctan((2*y*z-2*w*x)/((2*w**2)+(2*z**2)-1))
    return np.array([psi, theta, phi])

import numpy as np

def quaternion_to_euler(q):
    q0, q1, q2, q3 = q
    psi = np.arctan2(2 * (q1 * q2 - q0 * q3), 2 * (q0**2 + q1**2) - 1)
    theta = np.arcsin(2 * (q1 * q3 + q0 * q2))
    phi = np.arctan2(2 * (q2 * q3 - q0 * q1), 2 * (q0**2 + q3**2) - 1)
    return np.array([psi, theta, phi])

def logq(q):
    q0 = q[0]
    qv = np.array([q[1], q[2], q[3]])
    if np.linalg.norm(qv) == 0:
        return np.array([0, 0, 0])
    return np.arccos(q0) * qv / np.linalg.norm(qv)

def remove_nan(df):
    counter = 0
    nan = True
    while nan:
        if not df.loc[counter].isna().any():
            nan = False
        counter += 1
    for i in range(counter - 1):
        df = df.drop(index=i)
    df = df.reset_index(drop=True)
    counter = len(df) - 1
    nan = True
    while nan:
        if not df.loc[counter].isna().any():
            nan = False
        counter -= 1
    maxlen = len(df)
    for i in range(maxlen - 1, counter + 1, -1):
        df = df.drop(index=i)
    df = df.reset_index(drop=True)
    for i in range(len(df)):
        df['timestamp'][i] = df['timestamp'][i] - df['timestamp'][0]
    for i in range(len(df)):
        for column in df.columns:
            if np.isnan(df[column][i]):
                deler = (df['timestamp'][i] - df['timestamp'][i - 1]) / (df['timestamp'][i + 1] - df['timestamp'][i - 1])
                df[column][i] = df[column][i - 1] + deler * (df[column][i + 1] - df[column][i - 1])
    return df

def left_quat_mul(q):
    q0, q1, q2, q3 = q
    lqm = np.array([
        [q0, -q1, -q2, -q3],
        [q1, q0, -q3, q2],
        [q2, q3, q0, -q1],
        [q3, -q2, q1, q0]
    ])
    return lqm

def right_quat_mul(q):
    q0, q1, q2, q3 = q
    rqm = np.array([
        [q0, -q1, -q2, -q3],
        [q1, q0, q3, -q2],
        [q2, -q3, q0, q1],
        [q3, q2, -q1, q0]
    ])
    return rqm

def rotate_data(data, quat):
    for i, row in data.iterrows():
        data.loc[i, 'x_acc'], data.loc[i, 'y_acc'], data.loc[i, 'z_acc'] = rotate_vector(np.array([row['x_acc'], row['y_acc'], row['z_acc']]), quat)
        data.loc[i, 'x_gyro'], data.loc[i, 'y_gyro'], data.loc[i, 'z_gyro'] = rotate_vector(np.array([row['x_gyro'], row['y_gyro'], row['z_gyro']]), quat)
    return data

def remove_bias(data, cali):
    data_nb = data.copy()
    acc_values = cali['acc values']
    for i, ax in zip(range(3), ['x_acc', 'y_acc', 'z_acc']):
        posi = acc_values[i * 2]
        nega = acc_values[i * 2 + 1]
        no_bias = np.array(data_nb[ax]) - (posi + nega) * 0.5
        scaled = no_bias * 2 / (posi - nega)
        data_nb[ax] = scaled

    gyro_means = cali['gyro bias']
    for i, ax in zip(range(3), ['x_gyro', 'y_gyro', 'z_gyro']):
        data_nb[ax] = data_nb[ax] - gyro_means[i]

    return data_nb

def zv_checker(data, N, gamma, first_last=False):
    zv_data = data.copy()
    zv_data['squared norm'] = data['x_gyro'] ** 2 + data['y_gyro'] ** 2 + data['z_gyro'] ** 2
    zv = [first_last] * len(zv_data)
    for i in range(N, len(zv_data) - N):
        if zv_data['squared norm'][i-N:i+N].mean() < gamma:
            zv[i] = True
    zv_data['zero velocity'] = zv
    return zv_data
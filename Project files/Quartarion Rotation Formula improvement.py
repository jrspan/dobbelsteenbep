import numpy as np


# Functions needed for rotation code --------------------

def quaternion_multiply(q1, q2):
    w1, x1, y1, z1 = q1
    w2, x2, y2, z2 = q2
    w = w1*w2 - x1*x2 - y1*y2 - z1*z2
    x = w1*x2 + x1*w2 + y1*z2 - z1*y2
    y = w1*y2 + y1*w2 + z1*x2 - x1*z2
    z = w1*z2 + z1*w2 + x1*y2 - y1*x2
    return np.array([w, x, y, z])


def quaternion_conjugate(q):
    w, x, y, z = q
    return np.array([w, -x, -y, -z])

# Actual Rotation Fuction - Input = Acceleration vector = 1x3 , rotation_quaternion = 1*4
def rotate_vector(vector, rotation_quaternion):
    # Convert the vector to a quaternion
    vector_quaternion = np.concatenate(([0], vector))

    # Calculate the rotated quaternion
    rotated_quaternion = quaternion_multiply(rotation_quaternion, quaternion_multiply(vector_quaternion, quaternion_conjugate(rotation_quaternion)))

    # Extract the rotated vector from the quaternion
    rotated_vector = rotated_quaternion[1:]

    return rotated_vector


a=np.array(0,0,1)

#print(np.concatenate(([0],a)))


# Singular test around y axis


print(2)

q = [1,2,3,4]

rotation_angle = -np.pi/2
rotation_axis = np.array([0, 1, 0])  # y-axis
rotation_y  = np.array([np.cos(rotation_angle/2),
                                rotation_axis[0]*np.sin(rotation_angle/2),
                                rotation_axis[1]*np.sin(rotation_angle/2),
                                rotation_axis[2]*np.sin(rotation_angle/2)])

Test = rotate_vector(a, rotation_y)
print(Test)

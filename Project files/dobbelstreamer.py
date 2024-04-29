from mbientlab.metawear import MetaWear, libmetawear, parse_value
import mbientlab.metawear.cbindings as cbindings
from ctypes import Structure, c_void_p, cast, POINTER, c_int, c_float
from threading import Event
from time import sleep
import pandas as pd

def stream(length):
    # MAC address of the MetaWear device
    device_address = 'D4:06:BD:85:8F:23'

    # Create and connect the device
    device = MetaWear(device_address)
    device.connect()

    timestamps = []
    x_accs = []
    y_accs = []
    z_accs = []
    x_gyros = []
    y_gyros = []
    z_gyros = []

    def data_handler(context, data):
        values = parse_value(data, n_elem = 2)
        timestamp = int(data.contents.epoch)
        #print("timestamp: %.1f, acc: (%.4f,%.4f,%.4f), gyro; (%.4f,%.4f,%.4f)" % (timestamp, values[0].x, values[0].y, values[0].z, values[1].x, values[1].y, values[1].z))
        timestamps.append(timestamp)
        x_accs.append(values[0].x)
        y_accs.append(values[0].y)
        z_accs.append(values[0].z)
        x_gyros.append(values[1].x)
        y_gyros.append(values[1].y)
        z_gyros.append(values[1].z)

    e = Event()
    callback = cbindings.FnVoid_VoidP_DataP(data_handler)

    # Callback for processor creation
    def processor_created(context, pointer):
        global processor
        processor = pointer
        e.set()

    # Function pointer
    fn_wrapper = cbindings.FnVoid_VoidP_VoidP(processor_created)

    # Acc and gyro signals
    acc = libmetawear.mbl_mw_acc_get_acceleration_data_signal(device.board)
    gyro = libmetawear.mbl_mw_gyro_bmi160_get_rotation_data_signal(device.board)


    # Fuse the signals together
    signals = (c_void_p * 1)()
    signals[0] = gyro
    libmetawear.mbl_mw_dataprocessor_fuser_create(acc, signals, 1, None, fn_wrapper)
    e.wait()

    # Start logger
    libmetawear.mbl_mw_logging_start(d.board, 0)

    # Subscribe to it
    libmetawear.mbl_mw_datasignal_subscribe(processor, None, callback)

    # Start the gyro and acc
    libmetawear.mbl_mw_gyro_bmi160_enable_rotation_sampling(device.board)
    libmetawear.mbl_mw_acc_enable_acceleration_sampling(device.board)
    libmetawear.mbl_mw_gyro_bmi160_start(device.board)
    libmetawear.mbl_mw_acc_start(device.board)

    # Stream data for a duration (e.g., 30 seconds)
    sleep(length)

    # Stop and clean up
    libmetawear.mbl_mw_acc_stop(device.board)
    libmetawear.mbl_mw_acc_disable_acceleration_sampling(device.board)
    libmetawear.mbl_mw_datasignal_unsubscribe(processor)
    libmetawear.mbl_mw_debug_disconnect(device.board)
    #print("Disconnected and cleaned up")



    #data_array = np.array([timestamps, x_accs, y_accs, z_accs, x_gyros, y_gyros, z_gyros])
    data_df = pd.DataFrame(columns=['time', 'x_acc', 'y_acc', 'z_acc', 'x_gyro', 'y_gyro', 'z_gyro'])

    data_df['time'] = timestamps
    data_df['x_acc'] = x_accs
    data_df['y_acc'] = y_accs
    data_df['z_acc'] = z_accs
    data_df['x_gyro'] = x_gyros
    data_df['y_gyro'] = y_gyros
    data_df['z_gyro'] = z_gyros

    return data_df

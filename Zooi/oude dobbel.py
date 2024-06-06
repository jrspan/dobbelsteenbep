from mbientlab.warble import *
from mbientlab.metawear import *
from mbientlab.metawear.cbindings import *
from ctypes import cast, byref
from threading import Event
from time import sleep
import pandas as pd
from math import nan

class dobbellogger():
    def __init__(self):
        e = Event()
        address = None
        def device_discover_task(result):
            global address
            if (result.has_service_uuid(MetaWear.GATT_SERVICE)):
                # grab the first discovered metawear device
                address = result.mac
                e.set()

        BleScanner.set_handler(device_discover_task)
        BleScanner.start()
        e.wait()

        BleScanner.stop()
        d = MetaWear('D4:06:BD:85:8F:23')
        d.connect()
        self.d = d

    def disconnect(self):
        self.d.on_disconnect = lambda status: print ("we are disconnected!")
        self.d.disconnect()

    def reconnect(self):
        self.d.connect()

    def reset(self):
        libmetawear.mbl_mw_logging_clear_entries(self.d.board)
        libmetawear.mbl_mw_debug_reset(self.d.board)

    def log(self, duration, freq, acc_range, gyro_range):
        self.e = Event()

        libmetawear.mbl_mw_acc_set_odr(self.d.board, freq)
        libmetawear.mbl_mw_acc_set_range(self.d.board, acc_range)
        libmetawear.mbl_mw_acc_write_acceleration_config(self.d.board)

        if freq == 800:
            gyro_freq = GyroBoschOdr._800Hz
        elif freq == 400:
            gyro_freq = GyroBoschOdr._400Hz
        elif freq == 200:
            gyro_freq = GyroBoschOdr._200Hz
        elif freq == 100:
            gyro_freq = GyroBoschOdr._100Hz
        elif freq == 50:
            gyro_freq = GyroBoschOdr._50Hz
        elif freq == 25:
            gyro_freq = GyroBoschOdr._25Hz
        else:
            gyro_freq = GyroBoschOdr._100Hz

        if gyro_range == 2000:
            gyro_ra = GyroBoschRange._2000dps
        elif gyro_range == 1000:
            gyro_ra = GyroBoschRange._1000dps
        elif gyro_range == 500:
            gyro_ra = GyroBoschRange._500dps
        elif gyro_range == 250:
            gyro_ra = GyroBoschRange._250dps
        elif gyro_range == 125:
            gyro_ra = GyroBoschRange._125dps
        else:
            gyro_ra = GyroBoschRange._2000dps

        libmetawear.mbl_mw_gyro_bmi160_set_odr(self.d.board, gyro_freq)
        libmetawear.mbl_mw_gyro_bmi160_set_range(self.d.board, gyro_ra)
        libmetawear.mbl_mw_gyro_bmi160_write_config(self.d.board)

        # Acc and gyro signals
        acc = libmetawear.mbl_mw_acc_get_acceleration_data_signal(self.d.board)
        gyro = libmetawear.mbl_mw_gyro_bmi160_get_rotation_data_signal(self.d.board)

        # Create a logger
        self.acc_logger = create_voidp(lambda fn: libmetawear.mbl_mw_datasignal_log(acc, None, fn), resource = "acc_logger")
        self.gyro_logger = create_voidp(lambda fn: libmetawear.mbl_mw_datasignal_log(gyro, None, fn), resource = "gyro_logger")

        # Start logger
        libmetawear.mbl_mw_logging_start(self.d.board, 0)
        # Turn on the accelerometer
        libmetawear.mbl_mw_acc_enable_acceleration_sampling(self.d.board)
        libmetawear.mbl_mw_gyro_bmi160_enable_rotation_sampling(self.d.board)
        libmetawear.mbl_mw_acc_start(self.d.board)
        libmetawear.mbl_mw_gyro_bmi160_start(self.d.board)


        print(f"Logging data for {duration}s")
        sleep(duration)

        # Turn off the accelerometer
        libmetawear.mbl_mw_acc_stop(self.d.board)
        libmetawear.mbl_mw_gyro_bmi160_stop(self.d.board)
        libmetawear.mbl_mw_acc_disable_acceleration_sampling(self.d.board)
        libmetawear.mbl_mw_gyro_bmi160_disable_rotation_sampling(self.d.board)
        # Stop logging
        libmetawear.mbl_mw_logging_stop(self.d.board)


    def download(self):
        print("Downloading data")
        # Callback function to handle logger entries as we download them
        def progress_update_handler(context, entries_left, total_entries):
            if (entries_left == 0):
                self.e.set()

        # Function pointer and handlers for the logger download (LogDownloadHandler -> in the cbindings)
        fn_wrapper = FnVoid_VoidP_UInt_UInt(progress_update_handler)
        download_handler = LogDownloadHandler(context = None, received_progress_update = fn_wrapper, received_unknown_entry = cast(None, FnVoid_VoidP_UByte_Long_UByteP_UByte), received_unhandled_entry = cast(None, FnVoid_VoidP_DataP))

        acc_data = {}
        gyro_data = {}

        def acc_data_handler(context, p):
            parsed = parse_value(p)
            acc_data[int(p.contents.epoch)] = {'x': parsed.x, 'y': parsed.y, 'z': parsed.z}

        def gyro_data_handler(context, p):
            parsed = parse_value(p)
            gyro_data[int(p.contents.epoch)] = {'x': parsed.x, 'y': parsed.y, 'z': parsed.z}

        acc_callback = FnVoid_VoidP_DataP(acc_data_handler)
        gyro_callback = FnVoid_VoidP_DataP(gyro_data_handler)

        # Stop logger
        libmetawear.mbl_mw_logger_subscribe(self.acc_logger, None, acc_callback)
        libmetawear.mbl_mw_logger_subscribe(self.gyro_logger, None, gyro_callback)

        # Download logger contents
        libmetawear.mbl_mw_logging_download(self.d.board, 0, byref(download_handler))
        self.e.wait()

        libmetawear.mbl_mw_logging_clear_entries(self.d.board)
        all_epochs = sorted(set(list(acc_data.keys()) + list(gyro_data.keys())))
        self.datadf = pd.DataFrame(columns=['timestamp', 'x_acc', 'y_acc', 'z_acc', 'x_gyro', 'y_gyro', 'z_gyro'])

        for epoch in all_epochs:
            row = [float(epoch - all_epochs[0])]
            if epoch in acc_data.keys() and epoch in gyro_data.keys():
                row += [acc_data[epoch]['x'], acc_data[epoch]['y'], acc_data[epoch]['z'], gyro_data[epoch]['x'], gyro_data[epoch]['y'], gyro_data[epoch]['z']]
            elif epoch in acc_data.keys():
                row += [acc_data[epoch]['x'], acc_data[epoch]['y'], acc_data[epoch]['z'], nan, nan, nan]
            else:
                row += [nan, nan, nan, gyro_data[epoch]['x'], gyro_data[epoch]['y'], gyro_data[epoch]['z']]
            self.datadf.loc[len(self.datadf)] = row

        libmetawear.mbl_mw_logging_clear_entries(self.d.board)
        libmetawear.mbl_mw_debug_reset(self.d.board)
        print('Done! The data is located in self.datadf')


    def show(self, length=20):
        self.datadf.head(length)

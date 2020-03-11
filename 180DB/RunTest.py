
print("Importing libraries")
import time
t1 = time.time()
import tensorflow as tf
import numpy as np
import IMU
import paho.mqtt.publish as publish
print("Libraries loaded")

MQTT_SERVER = "192.168.1.13"
MQTT_TOPIC = "RPiCommand"
model = tf.keras.models.load_model("Command_reload_new_gesture.h5")
print("Model loaded")

IMU.detectIMU()  # Detect if BerryIMUv1 or BerryIMUv2 is connected.
IMU.initIMU()  # Initialise the accelerometer, gyroscope and compass
t2 = time.time()

print("Everything loaded in {} seconds".format(t2-t1))

def GetData():
    G_GAIN = 0.070  # [deg/s/LSB]  If you change the dps for gyro, you need to update this value accordingly
    ACC_LPF_FACTOR = 0.4  # Low pass filter constant for accelerometer
    ACC_MEDIANTABLESIZE = 9  # Median filter table size for accelerometer. Higher = smoother but a longer delay
    MAG_MEDIANTABLESIZE = 9  # Median filter table size for magnetometer. Higher = smoother but a longer delay

    oldXAccRawValue = 0
    oldYAccRawValue = 0
    oldZAccRawValue = 0

    # Setup the tables for the mdeian filter. Fill them all with '1' so we dont get devide by zero error
    acc_medianTable1X = [1] * ACC_MEDIANTABLESIZE
    acc_medianTable1Y = [1] * ACC_MEDIANTABLESIZE
    acc_medianTable1Z = [1] * ACC_MEDIANTABLESIZE

    a = time.time()
    diff = 0
    new_val = np.zeros([1,6])
    res = 2
    val = np.zeros([1,6])
    cnt = 0
    while cnt < 250:


        # Read the accelerometer,gyroscope and magnetometer values
        ACCx = IMU.readACCx()
        ACCy = IMU.readACCy()
        ACCz = IMU.readACCz()
        GYRx = IMU.readGYRx()
        GYRy = IMU.readGYRy()
        GYRz = IMU.readGYRz()

        ###############################################
        #### Apply low pass filter ####
        ###############################################

        ACCx = ACCx * ACC_LPF_FACTOR + oldXAccRawValue * (1 - ACC_LPF_FACTOR);
        ACCy = ACCy * ACC_LPF_FACTOR + oldYAccRawValue * (1 - ACC_LPF_FACTOR);
        ACCz = ACCz * ACC_LPF_FACTOR + oldZAccRawValue * (1 - ACC_LPF_FACTOR);

        oldXAccRawValue = ACCx
        oldYAccRawValue = ACCy
        oldZAccRawValue = ACCz

        #########################################
        #### Median filter for accelerometer ####
        #########################################
        # cycle the table
        for x in range(ACC_MEDIANTABLESIZE - 1, 0, -1):
            acc_medianTable1X[x] = acc_medianTable1X[x - 1]
            acc_medianTable1Y[x] = acc_medianTable1Y[x - 1]
            acc_medianTable1Z[x] = acc_medianTable1Z[x - 1]

        # Insert the lates values
        acc_medianTable1X[0] = ACCx
        acc_medianTable1Y[0] = ACCy
        acc_medianTable1Z[0] = ACCz

        # Copy the tables
        acc_medianTable2X = acc_medianTable1X[:]
        acc_medianTable2Y = acc_medianTable1Y[:]
        acc_medianTable2Z = acc_medianTable1Z[:]

        # Sort table 2
        acc_medianTable2X.sort()
        acc_medianTable2Y.sort()
        acc_medianTable2Z.sort()

        # The middle value is the value we are interested in
        ACCx = acc_medianTable2X[int(ACC_MEDIANTABLESIZE / 2)]
        ACCy = acc_medianTable2Y[int(ACC_MEDIANTABLESIZE / 2)]
        ACCz = acc_medianTable2Z[int(ACC_MEDIANTABLESIZE / 2)]

        # Convert Gyro raw to degrees per second
        rate_gyr_x = GYRx * G_GAIN
        rate_gyr_y = GYRy * G_GAIN
        rate_gyr_z = GYRz * G_GAIN

        diff = float(time.time() - a)

        new_val = np.array([[ACCx, ACCy, ACCz, rate_gyr_x, rate_gyr_y, rate_gyr_z]])
        val = np.concatenate((val,new_val), axis=0)
        cnt = cnt + 1

    val = val[:1500]
    return val

def main():
    print("Start acquiring data")
    while True:
        val = GetData()
        val = val[1:,:]
        val = val.reshape(1,-1)
        pred = model.predict(val).argmax()
        print("Command:",pred)
        #publish.single(MQTT_TOPIC, str(pred), hostname=MQTT_SERVER, qos=2)

if __name__ == '__main__':
    main()

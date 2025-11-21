import random

def read_imu_data():
    """
    Simulate IMU readings: (acc_x, acc_y, acc_z)
    """
    return (random.uniform(-1, 1), random.uniform(-1, 1), random.uniform(-1, 1))
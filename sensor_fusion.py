import numpy as np

def fuse_data(camera_dist, imu_data):
    """
    Example sensor fusion: combine distance and motion vector.
    """
    if imu_data is None:
        return camera_dist
    fused = (camera_dist + np.linalg.norm(imu_data)) / 2
    return round(fused, 2)
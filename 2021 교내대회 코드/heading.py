#!/usr/bin/env python
# -*- coding: utf-8 -*
from imu import *
import math

imu = Imu()

while 1:
    forward_direction = imu.imu_read()-90
    if (forward_direction < 0):
        forward_direction = forward_direction + 360
    else:
        forward_direction = forward_direction
    print(forward_direction)

#!/usr/bin/env python
# -*- coding: utf-8 -*
from imu import *

imu = Imu()

while 1:
    forward_direction = imu.imu_read()+60 
    {
    if (forward_direction > 360)
        forward_direction = forward_direction - 360;

    else
        forward_direction = forward_direction ;
    }    

    print(forward_direction)

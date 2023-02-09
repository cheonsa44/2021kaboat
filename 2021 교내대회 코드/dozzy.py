#!/usr/bin/env python
# -*- coding: utf-8 -*-
import serial
import operator
import collections
import calcpoint
import math
from functools import reduce
from imu import *
import time
ser = serial.Serial(port = "/dev/ttyACM0", baudrate = 38400, timeout = 0.1)    

def GPSparser(data):
	gps_data = data.split(b",")
	idx_rmc = data.find(b'GNGGA')
	if data[idx_rmc:idx_rmc+5] == b"GNGGA":
		data = data[idx_rmc:]    
		if checksum(data):
		   # print(data)
			parsed_data = data.split(b",")
#			print(parsed_data)
			return parsed_data
		else :
			print ("checksum error")

def checksum(sentence):
	sentence = sentence.strip(b'\n')
	nmeadata, cksum = sentence.split(b'*',1)
	calc_cksum = reduce(operator.xor, (ord(chr(s)) for s in nmeadata), 0)
#	print(int(cksum,16), calc_cksum)
	if int(cksum,16) == calc_cksum:
		return True 
	else:
		return False 

def location(waypoint):

        way_latitude = waypoint[0]
        way_longitude = waypoint[1]
        rotate_way_latitude = way_latitude
        rotate_way_longitude = way_longitude
        imu = Imu()

        while True:
            data = ser.readline()
            result = collections.defaultdict()
            res = GPSparser(data) 
        #    print("I'm in GPS, ready to return del_lati, del_longi")
            if res == None:
                pass
                # print("I'm in Gps, and in res == None")
            else :
                   # res = str(res)
 #               print(res)
                lat = str (res[2])
                lon = str (res[4])
            # result['altitude'] = float(res[9])
                    
                if (res == "checksum error"):
                    print("")
            # print(result)
               # print(lat)
                lat_h = float(lat[2:4])
                lon_h = float(lon[2:5])
                lat_m = float(lat[4:12])
                lon_m = float(lon[5:13])
               # print('lat_h: %f lon_h: %f lat_m: %f lon_m: %f' %(lat_h, lon_h, lat_m, lon_m))

                latitude = lat_h + (lat_m/60)
                longitude = lon_h + (lon_m/60)
                
                print('latitude: %f longitude: %f' %(latitude,longitude))
                rotate_latitude = math.cos(-0.64)*latitude - math.sin(-0.64)*longitude
                rotate_longitude = math.sin(-0.64)*latitude + math.cos(-0.64)*longitude
                
                print('rotate_latitude: %f rotate_longitude: %f' %(rotate_latitude, rotate_longitude))
                del_lati = rotate_latitude -rotate_way_latitude    
                del_longi = rotate_longitude - rotate_way_longitude
                del_longi = del_longi * 100000
                print('del_lati: %f del_longi: %f' %(del_lati, del_longi))
                forward_direction = imu.imu_read()
                print("my heading angle is : ", forward_direction)
                if ( 0 <= forward_direction <= 170)  :
                    if (0):
                        print("Go straight")
              #          self.motor.motor_move(0, 30)
                        time.sleep(2)
                    else :
                        if (del_longi >= 0.3):
                            print("Left")
               #             self.motor.motor_move(-30, 13)
                            time.sleep(2)
                        elif (del_longi < -0.3):
                            print("Right")
                #            self.motor.motor_move(+30,13)
                            time.sleep(2)
                        else :
                            print("Go straight2")
                 #           self.motor.motor_move(0, 10)
                elif (170 < forward_direction < 290):
                    print("too left ,go right")
                  #  self.motor.motor_move(40,13)
                    time.sleep(1)
                elif (290 <= forward_direction <= 340) or ( 0<= forward_direction <= 10):
                    print("too right, go left")
                   # self.motor.motor_move(-40,13)
                    time.sleep(1)
                else:
                   # self.motor.motor_move(0,-11)
                    print("stop")

        return (del_lati, del_longi)
            #except:
            #    return (1 , 1)
            #    pass
if __name__ == '__main__':
    while True:
        way = [105.345249, 82.493466]
        location(way)

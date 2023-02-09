#!/usr/bin/env python
# -*- coding: utf-8 -*-
import serial
import operator
import collections
import calcpoint
#import rospy
import math
#from std_msgs.msg import Float64
#from std_msgs.msg import Float64MultiArray#,MultiArrayLayout,MultiArrayDimension
#import board                                                    #서보모터 드라이버 패키지에 종속된 패키지입니다
#import busio                                                    #위와같이 서보모터 드라이버 패키지에 종속된 패키지입니다
#import time                                                     #모터 제어시 delay를 주기 위해 time패키지를 불러옵니다
 # i2c 통신을 젯슨 나노의 27,28번 핀으로 시작합니다
#i2c_bus0 = (busio.I2C(5, 6))


ser = serial.Serial(port = "/dev/ttyACM0", baudrate = 38400, timeout = 0.1)	


def GPSparser(data):
	gps_data = data.split(",")
	idx_rmc = data.find('GNGGA')
	if data[idx_rmc:idx_rmc+5] == "GNGGA":
		data = data[idx_rmc:]	
		print (data)
		if checksum(data):
			parsed_data = data.split(",")
			return parsed_data
		else :
			print ("checksum error")

def checksum(sentence):
	sentence = sentence.strip('\n')
	nmeadata, cksum = sentence.split('*',1)
	calc_cksum = reduce(operator.xor, (ord(s) for s in nmeadata), 0)
	print(int(cksum,16), calc_cksum)
	if int(cksum,16) == calc_cksum:
		return True 
	else:
		return False 

def location():

#	pub = rospy.Publisher('gps_xy', Float64MultiArray, queue_size=10)
#	rospy.init_node('gps', anonymous=True)
#	rate = rospy.Rate(1) # 1hz

	way_latitude = float(input("way_latitude: "))
	way_longitude = float(input("way_longitude: "))
        
	#way_x, way_y = calcpoint.grid(way_latitude*100.0, way_longitude*100.0)
	#way__1 = float(input("way_x_1: "))
	#way_y_1 = float(input("way_y_1: "))
	#way_x_2 = float(input("way_x_2: "))
	#way_y_2 = float(input("way_y_2: "))


	while 1: 
		data = ser.readline()
		result = collections.defaultdict()
		res = GPSparser(data)
		if res == None:
			continue
		try:
			lat = str (res[2])
			lon = str (res[4])
			result['altitude'] = float(res[9])
			
			#print(data)

			if (res == "checksum error"):
				print("")
			print(result)
			#x, y = calcpoint.grid(result['latitude']*100.0,result['longitude']*100.0)
			
			
			lat_h = float(lat[0:2])
			lon_h = float(lon[0:3])
			lat_m = float(lat[2:10])
			lon_m = float(lon[3:11])
			print('lat_h: %f lon_h: %f lat_m: %f lon_m: %f' %(lat_h, lon_h, lat_m, lon_m))

			latitude = lat_h + (lat_m/60)
			longitude = lon_h + (lon_m/60)
			
			print('latitude: %f longitude: %f' %(latitude,longitude))
                        a = (way_longitude - longitude) / (way_latitude - latitude)
                        
			way_radi  = math.atan(a)
                        way_degree = way_radi*(180/math.pi)

			print(way_degree)
			#x, y = calcpoint.grid(latitude ,longitude)
			#print("x = %f y = %f" %(x,y))

#			value = Float64MultiArray()
		
#			del_lati = (way_latitude - latitude)*100
#			del_longi = (way_longitude - longitude)*100
#			print("del_lati = %f del_longi = %f" %(del_lati,del_longi))
#			value.data = [del_lati,del_longi]
			
			#del_x_2 = way_x_2 - x
			#del_y_2 = way_y_2 - y
			#print("del_x_2 = %f del_y_2 = %f" %(del_x_2,del_y_2))

				
			
#			pub.publish(value)
		    


#			rate.sleep()
			

		except:
			#print("not found data")

			#if KeyboardInterrupt :
			#	break
			pass
		


if __name__ == '__main__':
#	try:	
		location()

#	except rospy.ROSInterruptException:
		#pass

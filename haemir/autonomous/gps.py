#!/usr/bin/env python
import serial
import operator
import collections
import calcpoint
import rospy
import math
from std_msgs.msg import Int32

ser = serial.Serial(port = "/dev/ttyACM0", baudrate = 38400, timeout = 0.1)	
def GPSparser(data):
	gps_data = data.split(",")
	idx_rmc = data.find('GNGGA')
	if data[idx_rmc:idx_rmc+5] == "GNGGA":
		data = data[idx_rmc:]	
		#print (data)
		if checksum(data):
			parsed_data = data.split(",")
			return parsed_data
		else :
			print ("checksum error")
def checksum(sentence):
	sentence = sentence.strip('\n')
	nmeadata, cksum = sentence.split('*',1)
	calc_cksum = reduce(operator.xor, (ord(s) for s in nmeadata), 0)
	#print(int(cksum,16), calc_cksum)
	if int(cksum,16) == calc_cksum:
		return True 
	else:
		return False 

def location():

	pub = rospy.Publisher('gps_xy', Int32, queue_size=10)
	rospy.init_node('gps', anonymous=True)
	rate = rospy.Rate(1) # 1hz
	way_latitude = float(input("way_latitude: "))
	way_longitude = float(input("way_longitude: "))
	way_x, way_y = calcpoint.grid(way_latitude*100.0, way_longitude*100.0)

	while 1: 
		data = ser.readline()
		result = collections.defaultdict()
			result['latitude'] = float(res[2])
			result['longitude'] = float(res[4])
			result['altitude'] = float(res[9])
			print(data)

			if (res == "checksum error"):
				print("")
			print(result)
			x, y = calcpoint.grid(result['latitude']*100.0,result['longitude']*100.0)

			print("x =%f y =%f" %(x,y))

			angle = (way_y-y)/(way_x-x)
			way_angle = math.atan(angle)
			way_degree = way_angle*180/math.pi
			if (way_degree < 0):
				way_degree += 360
			print("way_angle: %f" %(way_degree))

			pub.publish(way_degree)


			rate.sleep()
		except:
			print("not found data")

			if KeyboardInterrupt :
				break




if __name__ == '__main__':
	try:	
		location()

	except rospy.ROSInterruptException:
		pass

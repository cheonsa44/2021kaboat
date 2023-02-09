#!/usr/bin/env python

import rospy

from std_msgs.msg import Float32
#from msg_package.msg import Min0b
#from msg_package.msg import MinBuoyancy
from msg_package.msg import HeadingAngle
#from geometry_msg.msg import Pose2D

class GlobalPath:
    def __init__(self):
        self.GPS_x = 0.0
        self.GPS_y = 0.0
        self.psi = 0.0
        self.i = 0 #for 'Waypoints List' Index
        self.error_Distance = 30.0 # if error_distance = 0
        self.DirectionAngle = 0.0
        rospy.Subscriber("/GPS_RealTime", GPS, self.gps_callback)
        rospy.Subscriber("/HeadingAngle_RealTime", HeadingAngle, self.HeadingAngle)

        self.direction_pub = rospy.Publisher("/Direction_Angle", DirectionAngle, queue_size = 10)
        self.thruster_pub = rospy.Publisher("/Error_Distance", Float32, queue_size = 10)

    def gps_callback(self, msg):
        self.GPS_x = msg.x
        self.GPS_y = msg.y

    def HeadingAngle_callback(self, msg):
        self.psi = msg.headingAngle # Heading Angle

    # unpack of 'waypoints list'

    def Global_Guidance(self, waypoint_x, waypoint_y):
        # Advance direction angle error

        if self.GPS_x == 0.0 and self.GPS_y == 0.0 and self.psi == 0.0
            return

        else:
            error_x = waypoint_x - self.GPS_x
            error_y = waypoint_y - self.GPS_y

            theta = math.atan2(error_x, error_y) # y axis = north
            theta = theta * 180 / math.pi # radian -> angle

            # theta : angle of waypoint direction in Earth Coordinate system

            error_N = theta - self.psi # psi = headingangle
            # error_N : error of y(angle) between the target and the ship
            # if error_N ~= 0 :True direction

            # compensate the angle representaion range from [-pi, pi] to [0, 2 * pi]

            if 180 <= error_N and error_N < 360:
                error_N -= 360
            elif -360 < error_N and error_N < -180
                error_N = error_N + 360 
            return error_N
   
class Path_Planner:
    def __init__(self):
        self.min_x = 0.0
        self.min_o_y = 0.0
        self.min_o_d = 0.0
        self.GPS_x = 0.0
        self.GPS_y = 0.0
        self.psi = 0.0
        self.min_x = 0.0
        self.min_d = 0.0
        self.Switch_Path_Planner_Distance = rospy.get_param('Switch_Path_Planner_Distance')
        rospy.Subscriber('/min_buoyance', MinBuoyancy, self.judgement_callback)
        rospy.Subscriber('/min_obstacle', Min0b, self.obstacle_callback)
        rospy.Subscriber('GPS_RealTime', GPS, self.gps_callback)
        rospy.Subscriber('/HeadingAngle_RealTime', HeadingAngle, self.HeadingAngle_callback)
        ## rospy.Subscriber('/optimal_degree', OptimalDegree, ??)

        self.direction_pub = rospy.Publisher("/Direction_Angle", DirectionAngle, queue_size = 10)
        self.thruster_pub = rospy.Publisher("/Error_Distance", Float32, queue_size = 10)

    def gps_callback(self, GPS):
        self.GPS_x = GPS.x
        self.GPS_y = GPS.y

    def HeadingAngle_callback(self, HeadingAngle):
        self.psi = HeadingAngle.headingAngle

    # LOS Guidance + PID control

    def LOS_Guidance(self, waypoint_x, waypoint_y):
        # Advance direction angle error

        if self.GPS_x == 0.0 and self.GPS_y == 0.0 and self.psi == 0.0
            return

        else:
            error_x = waypoint_x - self.GPS_x
            error_y = waypoint_y - self.GPS_y

            theta = math.atan2(error_x, error_y) # y axis = north
            theta = theta * 180 / math.pi # radian -> angle

            # theta : angle of waypoint direction in Earth Coordinate system

            error_N = theta - self.psi # psi = headingangle
            # error_N : error of y(angle) between the target and the ship
            # if error_N ~= 0 :True direction

            # compensate the angle representaion range from [-pi, pi] to [0, 2 * pi]

            if 180 <= error_N and error_N < 360:
                error_N -= 360
            elif -360 < error_N and error_N < -180
                error_N = error_N + 360 
            return error_N

    def judgement_Publish(self):
        #if 장애물이 있으면
            LOS_Guidance(self, waypoint_x, waypoint_y)
        #else
            global_path.Global_Guidance(self, waypoint_x, waypoint_y)

    def main():
        rospy.init_node('Judgement', anonymous = False)
        rate = rospy.Rate(10)

        path_planner = Path_Planner()
        global_path = GlobalPath()
        while not rospy.is_shutdown():
            path_planner.judgement_Publish()
            rate.sleep()
    if __name__ == '__main__':
        main()

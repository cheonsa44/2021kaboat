from motor import *
from socket import *
from graphic import *
from lidar import *
from camera import *
from imu import *
from gps import *
import calculate as cal

# mode2 : camera + lidar 사용해서 자율 주행
class ControlMode2:
    # 초기화
    def __init__(self):
        print("ControlMode2 init")

        # 모터 생성 및 기본값 설정
        self.motor = Motor()
        self.speed = 15
        self.direction = 0

        # IMU 생성 및 초기값(처음 각도) 저장
        self.imu = Imu()
        self.forward_direction = self.imu.imu_read()

        # 라이다 생성
        self.lidar = Lidar()

        
        # 목적지 향해서 주행
    def move_to_destination(self, rotate_angle, autopilot_angle):
        
        pass

    # 종료
    def __del__(self):
        pass

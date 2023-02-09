import rospy                            # ros 관련 명령어들을 사용하기 위해 rospy 패키지를 불러옵니다
from sensor_msgs.msg import LaserScan   # ros에서 사용하는 통신규칙 중 Float32라는 규칙을 라이다에서 사용하기 때문에 패키지를 불러옵니다
from tf2_msgs.msg import TFMessage      # ros에서 사용하는 통신규칙 중 tf2라는 규칙을 라이다에서 사용하기 때문에 패키지를 불러옵니다
import os                               # 라이다를 작동시키키 위한 ROS 프로그램들을 실행시키고 종료하기 위해, 터미널에 명령을 보낼 필요가 있습니다. 따라서 os 패키지를 불러옵니다
import time                             # 코드를 일시정지 시켜, 일정시간 delay를 주기 위해 time 패키지를 불러옵니다


class Lidar:
    # 초기화
    def __init__(self):
        print("lidar init")

        # roscore 프로그램을 백그라운드에서 실행합니다
        os.system("screen -dmS core roscore")
        # roscore가 실행되어야 다음 작업이 실행되므로 잠깐 기다려줍니다
        time.sleep(7)
        # 라이다 작동 프로그램을 백그라운드에서 실행합니다
        os.system("screen -dmS lidar roslaunch ydlidar_ros X4.launch")
        # 라이다가 움직이기까지 잠시 기다려줍니다
        time.sleep(7)
        # 라이다를 이용해 최적의 각도를 publish합니다
        os.system("screen -dmS optimal rosrun ydlidar_ros 7_22")

        self.block = []
        # ROS 시스템과 통신을 시작합니다(노드를 만든다고 합니다)
        self.lidar = rospy.init_node('listener', anonymous=True)        # ########################################################### 확인할 것!!

    def position_listen(self):
        # position 리스트에 담긴 쓸모없는 값을 지워줍니다
        self.position = []

        # position_callback()함수를 통해 유의미한 값이 리스트에 담겨진게 아니라면
        while len(self.position) == 0:
            # 계속 position_callback()함수를 이용하여 데이터를 받아옵니다
            self.lidar.Subscriber('/tf', TFMessage, Lidar.position_callback)

        # position 값을 반환합니다.
        return self.position

    def block_callback(self, data):
        self.block = data.ranges

    def block_listen(self):
        # block 리스트에 담긴 쓸모없는 값을 지워줍니다
        self.block = []

        # block_callback()함수를 통해 유의미한 값이 리스트에 담겨진게 아니라면
        while len(self.block) == 0:
            # 계속 block_callback()함수를 이용하여 데이터를 받아옵니다
            self.lidar.Subscriber('/scan', LaserScan, Lidar.block_callback)

        # block 값을 반환합니다.
        return self.block

    # 종료
    def __del__(self):
        print("lidar del")

        # 프로그램을 역순으로 끄기 시작합니다. 위치 파악 프로그램부터 종료합니다.
        os.system("screen -S mapping -X quit")
        # 끄는데는 딱히 기다림이 필요없으므로 조금만 delay를 줍니다
        time.sleep(1)
        # 라이다 작동 프로그램을 끕니다
        os.system("screen -S lidar -X quit")
        # 또 조금 기다립니다
        time.sleep(1)
        # ROS 핵심 프로그램을 끕니다
        os.system("screen -S core -X quit")

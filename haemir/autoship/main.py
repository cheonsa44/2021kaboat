##from imu import *
from single_motor import *
# ################### MODE LIST ####################
# mode1 : 사용자가 직접 조종
# mode2 : camera + lidar 사용해서 자율 주행
# ##################################################


# 메인 함수(프로그램 실행)
if __name__ == "__main__":
       motor = single_motor()
       motor.motor_move(-40,-40)
       #motor.motor_move_only_degree(-70)
       time.sleep(5)


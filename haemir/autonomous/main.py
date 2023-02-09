from control import *


# ################### MODE LIST ####################
# mode1 : 사용자가 직접 조종
# mode2 : camera + lidar 사용해서 자율 주행
# ##################################################


# 메인 함수(프로그램 실행)
if __name__ == "__main__":
        control = ControlMode2()

        # 주행 시작
        while True:
            control.set_destination()

    del control

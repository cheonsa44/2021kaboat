from control import *
from gps import *

# ################### MODE LIST ####################
# mode1 : 사용자가 직접 조종
# mode2 : camera + lidar 사용해서 자율 주행
# ##################################################


# 메인 함수(프로그램 실행)
if __name__ == "__main__":
    # 모드 입력
    # mode = int(input("어떤 모드를 실행할까요?(1: 직접 조종, 2: 카메라+라이다)\n"))
    mode = 2

    # mode1(직접 주행일 때)
    if mode == 1:
        # 클래스 불러오기
        control = ControlMode1(True)

        # 주행 시작
        control.drive_myself()

    # mode2(camera + lidar)
    elif mode == 2:
        # 클래스 불러오기
        control = ControlMode2()

        # set the destination
        #waypoints = [list(map(int, input().split())) for _ in range(n)]

        n,m=map(int, input().split())
        #1
        waypoints=[0 for _ in range(n)]
        for i in range(n):
            waypoints[i]=list(map(float, input().split()))

        waypoint = waypoints[0]
        print("I will tell you waypoints")
        print(*waypoints, sep = '\n')
        print("\n")

        #del_lati, del_longi = location(waypoint)
        #print("I'm in main.py and receive del_lati : ", del_lati, " and del_longi : ", del_longi)
        #error_distance = math.sqrt(math.pow(del_lati , 2) + math.pow(del_longi,2)) < 1
        tolerance = 30
        i = 0

        # 주행 시작
        while True:
            print("I'm in main.py , and start loop")
            control.move_to_destination(waypoint)
            x_diff, y_diff = location(waypoint)
            error_distance = math.sqrt(math.pow(x_diff , 2) + math.pow(y_diff,2)) 

            if i + 1 != len(waypoints):
                if error_distance > tolerance:
                    print("i + 1 != len(waypoints), and error_distance > tolerance\n")
                    waypoint = waypoints[i]
                elif error_distance <= tolerance:
                    waypoint = waypoints[i + 1]
                    print("i + 1 != len(waypoints), and error_distance <= tolerance\n")
                    i = i + 1
            elif i + 1 == len(waypoints):
                print("Let's break\n")
                break
    del control

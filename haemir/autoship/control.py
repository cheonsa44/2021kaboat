from motor import *
from socket import *
from graphic import *
from lidar import *
from camera import *
from imu import *
import calculate as cal


# 실제 부표 크기(cm)
REAL_BUOY_SIZE = 100


# mode1 : 사용자가 직접 조종
class ControlMode1:
    # 초기화
    def __init__(self, joy_stick):
        print("ControlMode1 init")

        # 모터
        self.motor = Motor()

        # 모터 기본 셋팅값
        self.speed = 20
        self.degree = 40
        self.direction = 0

        # 소켓 통신 셋팅
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.sock.bind(('', 1972))
        self.sock.listen(1)

        # 조이스틱 사용 여부
        self.joy_stick = joy_stick

    # 직접 주행 시작
    def drive_myself(self):
        # 소켓 통신 시작
        conn, _ = self.sock.accept()

        # 종료 버튼 입력까지 반복
        while True:
            try:
                # 소켓 통신으로 데이터 받아오기
                data = conn.recv(1024).decode('utf-8')

                # 조이스틱을 사용할 때
                if self.joy_stick:
                    if data != '':
                        conn.send("ok".encode('utf-8'))
                        self.motor.motor_move(int(data[0:3]), int(data[3:6]))

                # 조이스틱을 사용하지 않을 때
                else:
                    if data == "exit":
                        break
                    if data == "up":
                        self.direction = 1
                        self.motor.motor_move_only_speed(self.direction * self.speed)
                    elif data == "down":
                        self.direction = -1
                        self.motor.motor_move_only_speed(self.direction * self.speed)
                    elif data == "left":
                        self.direction = -1
                        self.motor.motor_move_only_degree(self.direction * self.degree)
                    elif data == "right":
                        self.direction = 1
                        self.motor.motor_move_only_degree(self.direction * self.degree)
                    elif data == "keyupbldc":
                        self.motor.motor_move_only_speed(0)
                    elif data == "keyupservo":
                        self.motor.motor_move_only_degree(0)
                    if data == "one":
                        self.speed = 15
                        self.motor.motor_move_only_speed(self.direction * self.speed)
                    elif data == "two":
                        self.speed = 25
                        self.motor.motor_move_only_speed(self.direction * self.speed)
                    elif data == "thr":
                        self.speed = 35
                        self.motor.motor_move_only_speed(self.direction * self.speed)
                    elif data == "for":
                        self.speed = 45
                        self.motor.motor_move_only_speed(self.direction * self.speed)
                    elif data == "fiv":
                        self.speed = 55
                        self.motor.motor_move_only_speed(self.direction * self.speed)
            # 오류 발생
            except error as err:
                print("오류 발생 : " + err)
                break

    # 종료
    def __del__(self):
        print("ControlMode1 del")
        del self.motor
        del self.sock


# mode2 : camera + lidar 사용해서 자율 주행
class ControlMode2:
    # 초기화
    def __init__(self):
        print("ControlMode2 init")

        # 모터 생성 및 기본값 설정
        self.motor = Motor()
        self.speed = 15
        self.direction = 0

        # 카메라 생성 및 출력 화면 설정
        self.camera = Camera(True, False)
        self.camera_graphic = Graphic("Camera Detect Result", FRAME_W, FRAME_H)

        # IMU 생성 및 초기값(처음 각도) 저장
        self.imu = Imu()
        self.forward_direction = self.imu.imu_read()

        # 지도 크기 설정 후 지도 생성(세로 : 14.5m * 6, 가로 : 4.5m * 6)
        self.map_w = 270
        self.map_h = 870
        self.map_graphic = Graphic("Map", self.map_w, self.map_h)
        self.map_graphic.set_image(np.full((self.map_h, self.map_w, 3), (150, 200, 250), dtype=np.uint8))

        # 라이다 생성
        self.lidar = Lidar()

        # 벽과의 거리, 각도 저장할 변수
        wall_distance_back = 100
        wall_distance_left = 100
        wall_distance_right = 100
        wall_degree_back = 0

        # 가장 짧은 거리가 후방에 위치할 때까지 라이다 인식
        while not 170 <= int(wall_degree) <= 190:
            # 130 ~ 230 각도 범위의 거리 중 가장 짧은 거리 탐색
            blocks = self.lidar.block_listen()
            for idx, block in enumerate(blocks[260:460]):
                if block < wall_distance_back:
                    wall_distance_back = block
                    wall_degree = (idx + 260) / 2.0

        # for left_block in blocks:
        #     if
        #
        # if
        #
        # # 지도에 선박 초기 위치 그리기
        # self.map_graphic.draw_ship_on_map([self.map_w / 2, self.map_h - (block_distance * 6)])
        #
        # # 적정 객체 크기
        # self.min_size = 100
        # self.max_size = 500
        #
        # # 지나온 부표 갯수
        # self.destination = []

    # 지도 갱신하기
    def update_map(self):
        # 라이다로 가장 가까운 장애물과의 거리 구하기(출발 지점 구하기)
        block_distance = 1

        # 지도에 현재 배 좌표 그리기
        self.map_graphic.draw_ship_on_map([self.map_w / 2, self.map_h - (block_distance * 6)])

    # 목적지 설정
    def set_destination(self):
        # 부표 정보 저장
        target_buoys_center = []        # 부표 중심 좌표(라이다 좌표 형식)
        target_buoys_distance = []      # 부표와의 거리

        # 카메라 객체가 실행되는 동안 반복
        while self.camera.cap.isOpened():
            # 객체 탐지 결과 저장
            img, results = self.camera.object_detection()

            # 화면에 출력할 이미지 설정
            self.camera_graphic.set_image(img)

            # 가장 큰 부표 정보 저장할 리스트
            biggest_buoy_xy = []
            biggest_buoy_size = 0

            # 탐지된 객체 수만큼 반복
            for result in results:
                # 객체 정보 이미지에 추가
                self.camera_graphic.draw_object_on_img(result)

                # 객체 크기 탐지
                object_size = cal.get_average_size(result[1:3], result[3:])

                # 가장 큰 부표 정보 저장
                if object_size > biggest_buoy_size:
                    biggest_buoy_size = object_size
                    biggest_buoy_xy = result[1:]

            # FPS 이미지에 추가
            self.camera_graphic.add_text_on_img("FPS : " + str(self.camera.get_fps()))

            # 사진 출력
            self.camera_graphic.show_image()

            # 부표를 감지했을 때
            if biggest_buoy_size != 0:
                # 부표 중심 좌표(라이다 좌표 형식), 부표와의 거리 구해서 리스트에 저장
                target_buoys_center.append([cal.get_center_point(biggest_buoy_xy[:2], biggest_buoy_xy[2:])])
                target_buoys_distance.append(cal.get_real_distance(REAL_BUOY_SIZE, biggest_buoy_size))

        #         # 부표 정보가 10번 저장됐을 때
        #         if len(target_buoys_distance) == 10:
        #             real_distance_average = sum(target_buoys_distance) / len(target_buoys_distance)
        #             pixel_size_average =
        #             real_size_average = cal.get_real_size(real_distance_average,
        #                                                   sum([buoy_center[0] for buoy_center in target_buoys_center]) / len(target_buoys_center) - (FRAME_W/2.0))
        #
        #             self.destination.append(
        #                 [,
        #                  sum(target_buoys_distance)])
        #
        #     # 10번 이상 부표를 감지하지 못 했을 때
        #     elif biggest_buoy_size != 0:
        #         # 부표 정보 추가
        #         target_buoy_xy.append(biggest_buoy_xy)
        #         target_buoy_size.append(biggest_buoy_size)
        #
        #     # 가장 가까운 부표를 찾았을 때(가장 큰 부표를 찾았을 때)
        #     if biggest_buoy_size != 0:
        #         # 가장 가까운 부표 정보 저장
        #
        #         break
        #
        # # 목적지 좌표 계산
        # destination_x =
        # destination_y = target_buoy_distance
        #
        # # 여유 공간 고려해서 목적지 조정
        # # 목적지 x 좌표가 양수일 때(우회전 할 때)
        # if destination_x > 0:
        #     # 부표 크기만큼 여유 공간 부여
        #     destination_x += REAL_BUOY_SIZE
        #
        # # 목적지 x 좌표가 0 또는 음수일 때(좌회전 할 때)
        # else:
        #     # 부표 크기만큼 여유 공간 부여
        #     destination_x -= REAL_BUOY_SIZE
        #
        # # 목적지 좌표 반환
        # return [destination_x, destination_y]

    # 목적지 향해서 주행
    def move_to_destination(self, destination):
        pass

    # 종료
    def __del__(self):
        pass

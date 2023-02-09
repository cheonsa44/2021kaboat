# 미리 측정해둔 픽셀 거리
pixel_distance = 123


# 가로 길이와 세로 길이의 평균
def get_average_size(point1, point2):
    # x좌표 길이(가로 길이)
    distance_x = abs(point1[0] - point2[0])

    # y좌표 길이(세로 길이)
    distance_y = abs(point1[1] - point2[1])

    # 평균 계산하여 반올림 후 반환
    return round((distance_x + distance_y) / 2.0, 1)


# 객체와의 실제 떨어진 거리 계산
def get_real_distance(real_size, pixel_size):
    # 객체와의 실제 거리 계산
    real_distance = (pixel_distance * real_size) / pixel_size

    # 객체좌의 실제 거리 반올림 후 반환
    return round(real_distance, 1)


# 객체의 실제 (가로, 세로) 크기 계산
def get_real_size(real_distance, pixel_size):
    real_size = (real_distance * pixel_size) / pixel_distance

    return round(real_size, 1)


# 두 점의 가운데 좌표
def get_center_point(point1, point2):
    center_x = (point1[0] + point2[0]) / 2.0
    center_y = (point1[1] + point2[1]) / 2.0
    return center_x, center_y

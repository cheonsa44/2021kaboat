# 1. JETSON NANO 처음 시작하기!(수정중)

## 준비물 H/W
>Jetson Nano Development Kit 2GB Memory 모델
>
>HDMI 지원 모니터, 모니터 전원 어댑터
>
>표준 HID 규격의 키보드와 마우스
>
>HDMI 케이블
>
>OS 설치용 MicroSD카드(최소 64GB)
>
>802.11ac 무선 어댑터(와이파이 어댑터)
>
>5V 3A USB C-Type 전원 어댑터
>
>원활한 무선 또는 유선 인터넷 환경(휴대폰 핫스팟은 비추천)
>
>iptime 공유기(추천)
>
>MicroSD USB 어댑터
>
>OS 이미지를 다운받고 USB에 이미지를 쓸 다른 컴퓨터

## 준비물 S/W
>Jetson Nano OS 이미지(jetson-nano-2gb-jp451-sd-card-image)
>
>rufus (디스크 이미지 쓰기 프로그램)

## 실행 과정
>### 젯슨 나노 OS 이미지 다운로드 받기
>https://developer.nvidia.com/embedded/learn/get-started-jetson-nano-devkit#write
>
>위의 사이트에서 OS 이미지를 다운받습니다
>
>![image](https://user-images.githubusercontent.com/16367967/129654578-94d8a4f9-3d85-4121-ba3c-1628539b2665.png)
>+ 현재까지 확인된 바로는, OS 이미지 버젼이 변하지 않는 것 같아 그때그때 다운받으면 될 것 같습니다!
>
>### 젯슨 나노 OS 이미지 쓰기
>
>MicroSD 카드가 꽂힌 어댑터를 연결하고 rufus를 실행합니다
>
>rufus 에서 방금 연결한 MicroSD저장소를 선택합니다
>
>![image](https://user-images.githubusercontent.com/16367967/129655175-41a9a986-a685-4f59-868e-d2d2167c420e.png)
>
>MicroSD 카드에 쓸 이미지 선택 창을 띄우고 방금 다운받은 JETSON NANO OS 이미지를 선택합니다
>
>![image](https://user-images.githubusercontent.com/16367967/129655312-290ceb2c-1c78-4b89-84dc-7b3166d3644c.png)
>
>시작을 누르고 경고창이 뜰 경우 모두 수락하시면 이미지 쓰기가 진행됩니다
>+ 약 15분 정도 걸립니다! 커피 한잔하고 오세요!
>
>### 젯슨 나노 처음 실행하기
>
>HDMI모니터, 마우스, 키보드, 802.11ac(와이파이)어댑터, MicroSD카드를 모두 JETSON NANO에 연결합니다
>
>모든 것이 연결된것을 확인 후에 USB 전원 어댑터를 연결합니다
>
>화면에 NVIDIA 로고가 뜨는것을 확인하고 잠시 뒤 설정 화면으로 들어갑니다
>
>### 젯슨 나노 원격접속 설정하기(선택)
>젯슨 나노가 연결된 와이파이 공유기와 같은 공유기에 접속합니다
>
>+ 이 아래부터는 iptime 공유기를 예시로 원격 접속 과정을 설명하고 있습니다. 
>+ 만약 다른 공유기일 경우, 해당 공유기의 메뉴얼을 참고해주세요


# 2. JETSON NANO에 ROS 설치하기!

## 준비물 H/W
>ROS가 설치된 JetsonNano
> 
>원격으로 터미널에 접속할 다른 컴퓨터(선택)

## 준비물 S/W
>Putty 나 Windows PowerShell 같은 ssh 원격 접속 프로그램

## 설치되는 프로그램
>ROS(Melodic Morenia 버전)
>+ ROS Melodic 이라고 줄여서 보통 말합니다

## 코드 실행 과정
>우선 JETSON NANO 터미널에 원격 접속하거나, 터미널을 띄운 뒤 아래의 명령어들을 실행합니다!
>
>### ROS 레포지토리 저장
>ROS 레포지토리를 apt 프로그램 설치 및 업데이트 시 찾아볼 장소로 등록합니다
>
>```sudo sh -c 'echo "deb http://packages.ros.org/ros/ubuntu $(lsb_release -sc) main" > /etc/apt/sources.list.d/ros-latest.list'```
>
>ROS 레포지토리를 접근하기 위한 키를 다운로드 합니다
>
>```curl -s https://raw.githubusercontent.com/ros/rosdistro/master/ros.asc | sudo apt-key add -```
>
>apt 업데이트시 찾아볼 장소 목록을 업데이트 합니다
>
>```sudo apt update```
>
>### ROS 설치
>ROS 패키지를 설치합니다
>
>```sudo apt install ros-melodic-desktop```
>
>쉘 바로가기에 ROS를 추가하여 명령어를 사용할 수 있도록 합니다
>
>```echo "source /opt/ros/melodic/setup.bash" >> ~/.bashrc```\
>```source ~/.bashrc```
>
>ROS를 실행하기 위한 프로그램들을 설치합니다
>
>```sudo apt install python-rosdep python-rosinstall python-rosinstall-generator python-wstool build-essential```
>
>ROS 실행 프로그램을 시작하고 공간을 만듭니다
>
>```sudo rosdep init```
>
>ROS 실행 프로그램을 업데이트 합니다
>
>```rosdep update```
>
>### 기타 발견된 오류들
>
>+ROS 레포지토리 등록 과정에서  curl이 설치 안된 케이스 발견!
>
>```sudo apt-get install curl```



# 2. JETSON NANO에 OpenCV 설치하기!

## 준비물 H/W
>ROS가 설치된 JetsonNano
>
>원격으로 터미널에 접속할 다른 컴퓨터(선택)

## 준비물 S/W
> Putty 나 Windows PowerShell 같은 ssh 원격 접속 프로그램

## 설치되는 프로그램
> OpenCV 4(4.1.1 버젼)

## 코드 실행 과정
>우선 JETSON NANO 터미널에 원격 접속하거나, 터미널을 띄운 뒤 아래의 명령어들을 실행합니다!
>
>### JETSON NANO 최신 상태로 만들기
>
>JETSON NANO를 최신으로 업데이트 합니다
>
>```sudo apt -y update```\
>```sudo apt -y upgrade```
>
>### OpenCV 에 필요한 패키지 설치
>
>OpenCV 코드 빌드에 필요한 패키지를 설치합니다
>
>```sudo apt -y install build-essential cmake pkg-config```
>
>사진을 불러오거나 저장하기 위한 패키지를 설치합니다
>
>```sudo apt -y install libjpeg-dev libtiff5-dev libpng-dev```
>
>동영상이나 카메라를 이용하기 위한 패키지를 설치합니다
>
>```sudo apt -y install libavcodec-dev libavformat-dev libswscale-dev```\
>```sudo apt -y install libdc1394-22-dev libxvidcore-dev libx264-dev```\
>```sudo apt -y install libxine2-dev libv4l-dev v4l-utils```\
>```sudo apt -y install libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev```
>
>GUI 창으로 결과물을 보여주기 위한 패키지를 설치합니다
>
>```sudo apt -y install libgtk-3-dev```
>
>파이썬으로 OpenCV를 이용하기 위한 패키지를 설치합니다
>
>```sudo apt -y install libatlas-base-dev libeigen3-dev gfortran```\
>```sudo apt -y install python3-dev python3-numpy libtbb2 libtbb-dev```
>
>### OpenCV 다운로드할 폴더 만들기
>
>사용자 폴더로 간뒤 opencv 폴더를 만들어 들어갑니다
>
>```cd ~```\
>```mkdir opencv```\
>```cd opencv```
>
>### OpenCV 다운로드 하기
>
>OpenCV 소스 코드를 다운로드 합니다
>
>```wget -O opencv-4.0.0.zip https://github.com/opencv/opencv/archive/4.0.0.zip```\
>```wget -O opencv_contrib-4.0.0.zip https://github.com/opencv/opencv_contrib/archive/4.0.0.zip```
>
>OpenCV 소스 코드를 압축 해제합니다
>
>```unzip opencv-4.0.0.zip```\
>```unzip opencv_contrib-4.0.0.zip```
>
>### OpenCV 빌드 시작하기
>
>OpenCV를 빌드할 폴더를 만들고 거기에 들어갑니다
>
>```mkdir build```\
>```cd build```
>
>OpenCV 빌드에 필요한 파일을 생성합니다
>
>```cmake \```\
>```-D CMAKE_BUILD_TYPE=Release \```\
>```-D CMAKE_INSTALL_PREFIX=/usr/local \```\
>```-D BUILD_WITH_DEBUG_INFO=OFF \```\
>```-D BUILD_EXAMPLES=ON \```\
>```-D BUILD_opencv_python3=ON \```\
>```-D INSTALL_PYTHON_EXAMPLES=ON \```\
>```-D OPENCV_ENABLE_NONFREE=ON \```\
>```-D OPENCV_EXTRA_MODULES_PATH=../opencv_contrib-4.0.0/modules \```\
>```-D OPENCV_GENERATE_PKGCONFIG=ON \```\
>```-D WITH_TBB=ON \```\
>```../opencv-4.0.0/```\
>
>### OpenCV 빌드하기
>
>OpenCV 소스 코드를 최종적으로 컴파일합니다
>
>```make -j2```
>+ 이 명령어는 작업시간이 1 ~ 2시간 소요됩니다!
>
>### OpenCV 설치하기
>
>마지막으로 OpenCV를 JETSON NANO에 설치합니다
>
>```sudo make install```\
>```sudo ldconfig```
>
> 이 과정을 모두 마치고 나면, OpenCV가 설치되었을 것입니다.
> 아래 명령어를 통해 설치 여부를 확인해보세요!
> ```pkg-config --list-all | grep opencv```
> 
> OpenCV installation guide copyright https://sunkyoo.github.io/opencv4cvml/OpenCV4Linux.html


# 3. ROS Lidar와 SLAM 사용하기!

## 준비물 H/W
>ROS가 설치된 JetsonNano
>
>원격으로 터미널에 접속할 다른 컴퓨터(선택)
>
>YDLiDAR X4 라이다센서
>
>micro usb b-type 케이블(5핀 스마트폰 케이블)
>
>usb c-type to a-type 케이블(c타입 단자 반대편에 a타입 단자있는 케이블)
>
>5V 2A USB 어댑터(배가 없을 경우에)

## 준비물 S/W
>Putty 나 Windows PowerShell 같은 ssh 원격 접속 프로그램
> 
>JETSON NANO에 설치된 ROS

## 설치되는 프로그램
>ydlidar ROS 패키지
>
>hector_slam 패키지

## 코드 실행 과정

>### ROS 패키지 만들기
>
>ROS 명령어를 불러옵니다
>
>```source /opt/ros/melodic/setup.bash```
>
>폴더를 하나 만들고 거기에 패키지를 만듭니다
>
>```mkdir -p ~/catkin_ws/src```\
>```cd ~/catkin_ws/```\
>```catkin_make -DPYTHON_EXECUTABLE=/usr/bin/python3```
>
>(최근 이슈)만약 catkin_pkg라는 패키지가 파이썬에 설치되지 않았다고 에러가 뜨면!
>
>```sudo apt-get install python3-pip```\
>```sudo pip3 install catkin_pkg```
>
>이 폴더를 'ROS 빌드시 포함할 폴더들' 리스트에 넣어줍니다
>
>```source devel/setup.bash```\
>```echo $ROS_PACKAGE_PATH /home/유저이름/catkin_ws/src/opt/ros/melodic/share```\
>```sudo nano ~/.bashrc```
>
>텍스트 에디터가 열렸다면
>
> ```source ~/catkin_ws/devel/setup.bash``` 
> 
> 맨 밑줄에 추가하고 저장합니다
> 
>### 라이다 패키지 src폴더에 다운받기
>
>작업중인 패키지 폴더의 src 폴더로 들어갑니다
>
>```cd ~/catkin_ws/src```
>
>라이다 패키지를 인터넷에서 받아옵니다
>
>```git clone https://github.com/YDLIDAR/ydlidar_ros.git```
>
>### 라이다 소스 관련 에러해결 작업하기
>
>ydlidar 패키지 관련 에러해결 작업을 해줍니다
>
>```cd ydlidar_ros/sdk```\
>```git submodule init```\
>```git submodule update```
>
>다시 패키지 폴더로 돌아와서 빌드합니다
>
>```cd ~/catkin_ws```\
>```catkin_make ydlidar_ros```
>
>ydlidar 패키지 관련 에러해결 작업을 해줍니다
>
>```roscd ydlidar_ros/startup```\
>```sudo chmod 777 ./* ```\
>```sudo sh initenv.sh```
>
>### 라이다 작동시키기
>
>이제 라이다에 마이크로 5핀(전원)케이블과 USB-C Type(데이터)케이블을 각각 연결하고
>
>데이터 케이블을 젯슨 나노에 연결한 채로 재부팅을 해줍니다
>
>```sudo reboot```
>
>재부팅 후 아래 명령어를 쳤을 때 라이다가 작동하면 성공입니다
>
>```roslaunch ydlidar_ros X4.launch```
>
>### SLAM  패키지 src 폴더에 다운받기
>
>작업중인 패키지 폴더의 src 폴더로 들어갑니다
>
>```cd ~/catkin_ws/src```
>
>SLAM 패키지를 인터넷에서 받아옵니다
>
>```git clone https://github.com/tu-darmstadt-ros-pkg/hector_slam.git```
>
>SLAM 패키지 관련 에러해결 작업을 해줍니다
>
>```sudo apt-get install qt5-default```\
>```git clone https://github.com/ros-perception/vision_opencv.git```\
>```sudo nano vision_opencv/cv_bridge/CMakeLists.txt```\
>```pip3 install empy```
>텍스트 에디터가 열리면
>
>```#Debian Buster```\
>```find_package(Boost REQUIRED python37)```
>   
>부분을
>
>```#Debian Buster```\
>```find_package(Boost REQUIRED python)```
>   
>으로 바꾸어줍니다!
>
>다시 패키지 폴더로 돌아와서 빌드합니다
>
>```cd ~/catkin_ws```\
>```catkin_make -DPYTHON_EXECUTABLE=/usr/bin/python3 hector_slam```
>




# 나중에 추가할 코드들
```sudo apt-get install screen```\
```sudo apt-get install nano```\
```sudo pip3 install adafruit-circuitpython-servokit```\
```sudo apt-get install ros-kinetic-hector-slam```\
```sudo pip3 install rospkg```
tflite, tensorflow

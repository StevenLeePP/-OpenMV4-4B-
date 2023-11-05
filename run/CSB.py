import RPi.GPIO as GPIO
import time
import serial

# 设置GPIO模式为BCM
GPIO.setmode(GPIO.BCM)

# 定义超声波传感器的引脚
TRIG_PIN = 23  # 触发引脚
ECHO_PIN = 24  # 回声引脚

# 设置超声波传感器的引脚模式
GPIO.setup(TRIG_PIN, GPIO.OUT)
GPIO.setup(ECHO_PIN, GPIO.IN)

# 定义小车的控制引脚
# 你可以根据你的硬件配置调整这些引脚
LEFT_MOTOR_PIN1 = 17
LEFT_MOTOR_PIN2 = 18
RIGHT_MOTOR_PIN1 = 22
RIGHT_MOTOR_PIN2 = 27

# 设置小车的控制引脚模式
GPIO.setup(LEFT_MOTOR_PIN1, GPIO.OUT)
GPIO.setup(LEFT_MOTOR_PIN2, GPIO.OUT)
GPIO.setup(RIGHT_MOTOR_PIN1, GPIO.OUT)
GPIO.setup(RIGHT_MOTOR_PIN2, GPIO.OUT)


# 定义小车的前进和后退函数
def forward():
    GPIO.output(LEFT_MOTOR_PIN1, GPIO.HIGH)
    GPIO.output(LEFT_MOTOR_PIN2, GPIO.LOW)
    GPIO.output(RIGHT_MOTOR_PIN1, GPIO.HIGH)
    GPIO.output(RIGHT_MOTOR_PIN2, GPIO.LOW)


def backward():
    GPIO.output(LEFT_MOTOR_PIN1, GPIO.LOW)
    GPIO.output(LEFT_MOTOR_PIN2, GPIO.HIGH)
    GPIO.output(RIGHT_MOTOR_PIN1, GPIO.LOW)
    GPIO.output(RIGHT_MOTOR_PIN2, GPIO.HIGH)


def stop():
    GPIO.output(LEFT_MOTOR_PIN1, GPIO.LOW)
    GPIO.output(LEFT_MOTOR_PIN2, GPIO.LOW)
    GPIO.output(RIGHT_MOTOR_PIN1, GPIO.LOW)
    GPIO.output(RIGHT_MOTOR_PIN2, GPIO.LOW)


# 发射超声波信号并测量回声时间
def distance_measurement():
    GPIO.output(TRIG_PIN, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(TRIG_PIN, GPIO.LOW)

    while GPIO.input(ECHO_PIN) == 0:
        pulse_start = time.time()

    while GPIO.input(ECHO_PIN) == 1:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 34300 / 2  # 声速约为343米/秒
    return distance

# 打开串口
ser = serial.Serial('/dev/ttyUSB0', 9600)  # 根据实际情况指定串口名称和波特率

while True:
    data = ser.readline().decode('utf-8')  # 读取一行数据并解码为字符串
    print(data)  # 处理接收到的数据，这里仅打印出来

''''''
try:
    while True:
        dist = distance_measurement()
        print("距离: {:.2f}厘米".format(dist))

        if dist < 80:  # 如果前方有障碍物距离小于80厘米
            backward()  # 后退
            time.sleep(1)
            stop()
        else:
            forward()  # 前进
except KeyboardInterrupt:
    stop()
    GPIO.cleanup()

import time
from adafruit_pca9685 import PCA9685
import CSB
import RPi.GPIO as GPIO

# 初始化PCA9685对象
pca = PCA9685()
pca.frequency = 50  # 设置PWM频率

# 设置舵机和马达的通道
servo_channel = 0
motor_channel = 1

# 定义小车的控制引脚
# 你需要根据你的硬件配置来设置这些引脚
LEFT_MOTOR_PIN1 = 17
LEFT_MOTOR_PIN2 = 18
RIGHT_MOTOR_PIN1 = 22
RIGHT_MOTOR_PIN2 = 27

# 设置小车的控制引脚模式
GPIO.setmode(GPIO.BCM)
GPIO.setup(LEFT_MOTOR_PIN1, GPIO.OUT)
GPIO.setup(LEFT_MOTOR_PIN2, GPIO.OUT)
GPIO.setup(RIGHT_MOTOR_PIN1, GPIO.OUT)
GPIO.setup(RIGHT_MOTOR_PIN2, GPIO.OUT)

# 设置舵机和马达的控制范围
servo_min = 150  # 舵机的最小脉冲宽度
servo_max = 600  # 舵机的最大脉冲宽度
motor_min = 0   # 马达的最小脉冲宽度
motor_max = 4095  # 马达的最大脉冲宽度

# 设置小车前进
def forward():
    pca.channels[servo_channel].duty_cycle = servo_max
    pca.channels[motor_channel].duty_cycle = motor_max

def backward():
    GPIO.output(LEFT_MOTOR_PIN1, GPIO.LOW)
    GPIO.output(LEFT_MOTOR_PIN2, GPIO.HIGH)
    GPIO.output(RIGHT_MOTOR_PIN1, GPIO.LOW)
    GPIO.output(RIGHT_MOTOR_PIN2, GPIO.HIGH)

def left_turn():
    GPIO.output(LEFT_MOTOR_PIN1, GPIO.LOW)
    GPIO.output(LEFT_MOTOR_PIN2, GPIO.LOW)
    GPIO.output(RIGHT_MOTOR_PIN1, GPIO.HIGH)
    GPIO.output(RIGHT_MOTOR_PIN2, GPIO.LOW)

def right_turn():
    GPIO.output(LEFT_MOTOR_PIN1, GPIO.HIGH)
    GPIO.output(LEFT_MOTOR_PIN2, GPIO.LOW)
    GPIO.output(RIGHT_MOTOR_PIN1, GPIO.LOW)
    GPIO.output(RIGHT_MOTOR_PIN2, GPIO.LOW)

def stop():
    GPIO.output(LEFT_MOTOR_PIN1, GPIO.LOW)
    GPIO.output(LEFT_MOTOR_PIN2, GPIO.LOW)
    GPIO.output(RIGHT_MOTOR_PIN1, GPIO.LOW)
    GPIO.output(RIGHT_MOTOR_PIN2, GPIO.LOW)

# 设置小车停止
def stop():
    pca.channels[servo_channel].duty_cycle = (servo_max + servo_min) // 2
    pca.channels[motor_channel].duty_cycle = (motor_max + motor_min) // 2

if(CSB()):
    forward()
else:
    try:
        forward()  # 前进
        time.sleep(2)
        stop()

        left_turn()  # 左转
        time.sleep(1)
        stop()

        forward()  # 直行
        time.sleep(2)
        stop()

        right_turn()  # 右转
        time.sleep(1)
        stop()
    except KeyboardInterrupt:
        stop()
        GPIO.cleanup()
# 前进一段时间
forward()
time.sleep(2)

# 停止小车
stop()

# 清理PCA9685资源
pca.deinit()

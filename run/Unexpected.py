import time
from adafruit_pca9685 import PCA9685
import board
import busio

# 初始化I2C总线和PCA9685对象
i2c = busio.I2C(board.SCL, board.SDA)
pca = PCA9685(i2c)
pca.frequency = 50  # 设置PWM频率，通常为50Hz

# 通道0用于舵机
servo_channel = 0
# 通道1用于马达
motor_channel = 1

# 初始化OpenMV检测结果
openmv_detected_blind_lane = False

# 控制舵机的方向，例如，设置舵机向左转
def set_servo_left():
    pca.channels[servo_channel].duty_cycle = 0x6FFF

# 控制舵机的方向，例如，设置舵机向右转
def set_servo_right():
    pca.channels[servo_channel].duty_cycle = 0x8FFF

# 停止马达（设置占空比为0）
def stop_motor():
    pca.channels[motor_channel].duty_cycle = 0

# 模拟OpenMV检测，如果检测到盲道，设置openmv_detected_blind_lane为True
def simulate_openmv_detection():
    global openmv_detected_blind_lane
    openmv_detected_blind_lane = True  # 模拟检测到盲道

# 异常处理模块，例如，停车并采取其他措施
def exception_handling():
    print("执行异常处理模块")
    # 在这里可以执行异常处理操作

# 中断暂停，例如，停车并等待
def interrupt_pause():
    print("执行中断暂停")
    stop_motor()  # 停止马达
    # 在这里可以执行中断暂停操作

# 一些示例操作
try:
    while True:
        set_servo_left()  # 将舵机向左转
        time.sleep(2)

        # 模拟OpenMV检测
        simulate_openmv_detection()

        # 判断OpenMV检测结果
        if openmv_detected_blind_lane:
            print("检测到盲道")
            # 执行异常处理模块
            exception_handling()
        else:
            print("未检测到盲道")
            # 舵机向右转，寻找盲道
            set_servo_right()
            time.sleep(2)

            # 再次检测
            simulate_openmv_detection()

            # 如果仍未检测到盲道，执行中断暂停
            if not openmv_detected_blind_lane:
                interrupt_pause()

        stop_motor()  # 停止马达
        time.sleep(2)
except KeyboardInterrupt:
    # 用户按下Ctrl+C，退出程序
    stop_motor()  # 确保停止马达

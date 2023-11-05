# Untitled - By: Alicia - Tue Sep 26 2023

import sensor, image, time,ustruct
from pyb import UART,LED
from pid import PID
rho_pid = PID(p=0.4, i=0)
theta_pid = PID(p=0.001, i=0)
#THRESHOLD = (60, 99, -20, 4, 9, 42)
THRESHOLD = (40, 60, -15, 2, -12, 6)
#设置串口通信
uart = UART(3,115200)
uart.init(115200, bits=8, parity=None, stop=1)


#设置缓冲区
data = [0x00]
task=0

#接受数据 接收数据可能暂时不是很需要 可以让openmv一直运行
def UartReceiveDate():  #这个函数不能运行太快，否则会导致串口读取太快导致出错
    global task
    if uart.any():
        data[0]=uart.readchar()
        task = data[0]
        print(data[0])

#发送数据
def outuart(x):
    global uart;
    data = ustruct.pack("<f",
                   float(x)
                   )
    uart.write(data)
    print(data)
    time.sleep_ms(50)


sensor.reset()
sensor.set_vflip(True)
sensor.set_hmirror(True)
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QQVGA) # 80x60 (4,800 pixels) - O(N^2) max = 2,3040,000.
sensor.skip_frames(time = 2000)     # WARNING: If you use QQVGA it may take seconds
clock = time.clock()                # to process a frame sometimes.


def find_max(blobs):
    max_size=0
    for blob in blobs:
        if blob[2]*blob[3] >= max_size:
            max_blob=blob
            max_size = blob[2]*blob[3]
    return max_blob

while(True):
    clock.tick()
    #提取出颜色
    img = sensor.snapshot().lens_corr(strength = 1.8, zoom = 1.0).binary([THRESHOLD])
    img = img.histeq(adaptive=True, clip_limit=3)
    #提取出直线
    line = img.get_regression([(100,100)], robust = True)
    if (line):
        rho_err = abs(line.rho())-img.width()/2
        if line.theta()>90:
            theta_err = line.theta()-180
        else:
            theta_err = line.theta()
        img.draw_line(line.line(), color = 127)
        if line.magnitude()>8:
            #if -40<b_err<40 and -30<t_err<30:
            rho_output = rho_pid.get_pid(rho_err,1)
            theta_output = theta_pid.get_pid(theta_err,1)
            #计算出两个轮子的转速差
            output = rho_output+theta_output
            print(output)
            outuart(output)#标志位暂时设计为1
        else:
            outuart(2)
            print(2)
    else:
        outuart(2)
        print(2)

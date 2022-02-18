#import dynamixel_sdk as dynamixel
# from curses import baudrate
from time import sleep
from dynamixel_sdk import *
from serial import SerialException
import os
from math import radians, sin
import matplotlib.pyplot as plt
from numpy import array

def main():
    device_name = '/dev/ttyUSB0'
    port_num = PortHandler(device_name)
    baudrate = 57600 
    #this number can be increased but this is for testing pourposes
    # max baudrate is 4.5Mbps
    protocol = 2
    dynamxel_id = 1
    tourque_enable = 1
    tourque_disable = 0
    tourque_enable_id = 64
    control_id = 11
    position_enable = 3
    position_id = 116

    ph = PacketHandler(protocol)
    
    # init of serial port and baudrate
    try:
        os.system('sudo chmod 777 %s' % device_name)
        if port_num.openPort():
            print("Succeeded to open the port!")
        else:
            print('Unable to open port')
            return 0
    except SerialException:
        print('could not find / permission is denied for device : %s' % device_name)
        
        return 0
    # except : 

    if port_num.setBaudRate(baudrate):
        print('BaudRate set to', baudrate)
    else:
        print('BaudRate could not be set')
        return 0

    ph.write1ByteTxRx(port_num, dynamxel_id, tourque_enable_id, tourque_enable)
    if ph.read1ByteTxRx(port_num, dynamxel_id, tourque_enable_id)[0] != 1: #comm sucess is 0
        print('setting tourque failed')
        return 0
    else:
        print("Dynamixel has been successfully connected")

    min_pos = int(4095/4)
    max_pos = int(4095/2)+min_pos+3

    ph.write1ByteTxRx(port_num, dynamxel_id, control_id, position_enable) #this enables position control
    ph.write4ByteTxRx(port_num, dynamxel_id, position_id, int(max_pos-min_pos))
    sleep(1) #sleep for one second for init

    myplot = []
    myplot2 = []
    mystep = 1
    myvel = 2000
    print("min_pos: " + str(min_pos) + " max_pos: " + str(max_pos))
    position = lambda index : (float((max_pos - min_pos) + (min_pos * sin(radians(index)))))
    derivative = lambda index : (float(myplot[index]) - float(myplot[index-1])) # velocity function is not really used that well and somthing seems fishy

    #velocity will increase as sample points decrease

    periods = 3
    count = 0
    for period in range(0, periods, 1):
        for i in range(90, 270, mystep):
            sinfunct = position(i)
            myplot.append(sinfunct)
            if i == 90 and period == 0:
                myplot2.append(0)
            else:
                myplot2.append(derivative(count))
            count += 1
            
        for i in range(270, 90, (-1)*mystep):
            sinfunct = position(i)
            myplot.append(sinfunct)
            myplot2.append(derivative(count))
            count += 1

    time = []
    flaps_ps = 0.5
    time_funct = lambda index : float(index*mystep/(flaps_ps*60.0*6))
    for i in range(len(myplot)):
        time.append(time_funct(i))

    xpoints = array(time)
    ypoints_pos = array(myplot)
    ypoints_der = array(myplot2)
    # print(myplot2)

    plt.subplot(1,2,1, title='position')
    plt.plot(xpoints, ypoints_pos, color='r')
    plt.subplot(1,2,2, title='velocity')
    plt.plot(xpoints, ypoints_der, color='b')
    plt.show()

    # print(time[1])
    # i might have to use velocity control since that has some variation on time
    # the time to sleep needs to be fixed to produce an accurate flaps per second or make it as efficent as possible
    for pos in myplot:
        ph.write4ByteTxRx(port_num, dynamxel_id, position_id, int(pos))
        sleep(time[1])
    
    
    ph.write4ByteTxRx(port_num, dynamxel_id, position_id, int(max_pos-min_pos))
    sleep(0.5)
    ph.write1ByteTxRx(port_num, dynamxel_id, tourque_enable_id, tourque_disable)
    if ph.read1ByteTxRx(port_num, dynamxel_id, tourque_enable_id)[0] != 0: #comm sucess is 0
        print('setting tourque failed')
        return 0
    else:
        print("Dynamixel has been successfully disconnected")
    
    print('Closing port..')
    port_num.closePort()


if __name__ == '__main__':
    main()
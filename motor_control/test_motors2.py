#import dynamixel_sdk as dynamixel
# from curses import baudrate
from time import sleep, time
from dynamixel_sdk import *
from serial import SerialException
import os

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
    # velocity_limit = 1311 #this is for ~300rev/min
    dynamxel_velocity_conversion = lambda velocity : int(velocity*4.366797)
    dynamxel_acceleration_converstion = lambda acceleration: int(acceleration*214.577)
    velocity = lambda flaps_ps : (float(flaps_ps*60.0))
    accelleration = lambda flaps_ps, max_velocity : (float((360.0*flaps_ps))*max_velocity)
    velocity_limit = 300.0

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

    min_pos = int(4095/4)
    max_pos = int(4095/2)+min_pos+3

    ph.write1ByteTxRx(port_num, dynamxel_id, control_id, position_enable) #this enables position control
    ph.write1ByteTxRx(port_num, dynamxel_id, tourque_enable_id, tourque_enable)
    if ph.read1ByteTxRx(port_num, dynamxel_id, tourque_enable_id)[0] != 1: #comm sucess is 0
        print('setting tourque failed')
        return 0
    else:
        print("Dynamixel has been successfully connected")
    ph.write4ByteTxRx(port_num, dynamxel_id, position_id, int(max_pos-min_pos))
    sleep(1) #sleep for one second for init

    ph.write1ByteTxRx(port_num, dynamxel_id, tourque_enable_id, tourque_disable)
    sleep(1)
    #position control is not a great idea for this setup because it tries to move to poaint A to point B as fast as it can
    #velocity control is a better bet

    # for this is going to be a a profile of the max points of the position with a wait until done script completed to do the next rotationb back
    # https://emanual.robotis.com/docs/en/dxl/x/xl330-m077/#profile-acceleration



    # this will be done by setting profile velocity and then setting the acceleratiion.
    # acceleration depends on the fime per flap needed or how many flaps per second there is
    # max_position = {"id": 48 , "value": 3073 }
    # min_position = {"id": 52 , "value": 1023 }
    # ph.write4ByteTxRx(port_num, dynamxel_id, max_position["id"], max_position["value"])
    # ph.write4ByteTxRx(port_num, dynamxel_id, min_position["id"], min_position["value"])



    # ph.write4ByteTxRx(port_num, dynamxel_id, velocity_limit_id, velocity_limit)
    # ph.write1ByteTxRx(port_num, dynamxel_id, control_id, velocity_enable)
    ph.write1ByteTxRx(port_num, dynamxel_id, tourque_enable_id, tourque_enable)
    if ph.read1ByteTxRx(port_num, dynamxel_id, tourque_enable_id)[0] != 1: #comm sucess is 0
        print('reseting tourque failed')
        return 0

    myflaps_ps = 1
    number_of_flaps = 10
    
    #max velocity i have been using is 300 rev/min. we can crank this up as we go but for right now
    #aslo ned to figure out how to incorperate

    myvelocity = velocity(myflaps_ps)
    if(myvelocity > velocity_limit):
        myvelocity = velocity_limit
    myacceleration = accelleration(myflaps_ps, myvelocity)
    velocity_profile = {"id": 112, "value": dynamxel_velocity_conversion(myvelocity)}
    accelleration_profile = {"id": 108, "value": dynamxel_acceleration_converstion(myvelocity)}

    print("Velocity : ", myvelocity)
    print("Accelleration : ", myacceleration)

    ph.write4ByteTxRx(port_num, dynamxel_id, velocity_profile["id"], velocity_profile["value"])
    ph.write4ByteTxRx(port_num, dynamxel_id, accelleration_profile["id"], accelleration_profile["value"])
    
    # control code for flapping here
    position_control = {"id": 116, "max_value": 3073, "min_value": 1023}
    monitor_position_control = {"id": 132}
    start_time = time.time()
    while number_of_flaps > 0:
        ph.write4ByteTxRx(port_num, dynamxel_id, position_control["id"], position_control["min_value"])
        while (ph.read4ByteTxRx(port_num, dynamxel_id, monitor_position_control["id"])[0] - position_control["min_value"]) >= 12:
            pass
        ph.write4ByteTxRx(port_num, dynamxel_id, position_control["id"], position_control["max_value"])
        while (position_control["max_value"] - ph.read4ByteTxRx(port_num, dynamxel_id, monitor_position_control["id"])[0]) >= 12:
            pass
        number_of_flaps -= 1

    print(time.time() - start_time)
    ph.write1ByteTxRx(port_num, dynamxel_id, tourque_enable_id, tourque_disable)
    ph.write1ByteTxRx(port_num, dynamxel_id, control_id, position_enable) #this enables position control
    ph.write1ByteTxRx(port_num, dynamxel_id, tourque_enable_id, tourque_enable)
    
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

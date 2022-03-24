#import dynamixel_sdk as dynamixel
# from curses import baudrate
from time import sleep, time
from dynamixel_sdk import *
from serial import SerialException
import os

#  DO NOT CHANGE BELOW
BAUDRATE = 57600 
DEVICE_NAME = '/dev/ttyUSB0'
INPUT_TABLE = {
    'id': 1,
    'protocol': 2,
    'tourque': {'id': 64,'enable': 1,'disable': 0},
    'control': {'id': 11,'position': 3},
    'position':{'id': 116,'max_value': 3073,'min_value': 1023,'mid_value': 2048},
    'velocity_profile': {'id': 112,'value': 0},
    'acceleration_profile': {"id": 108, "value": 0},
    'position_monitor': {'id': 132}
}

# Try to avoid changing this, the motor could overvolt and test would fail
VELOCITY_LIMIT = 300.0

# an issue i am seeing is that it is really not the velocity that we need to get the job done which leads me to beleive that the velocity is not correct
# with the points that are set

def motor_init(flaps_ps):
    port_num = PortHandler(DEVICE_NAME)
    myflaps_ps = flaps_ps
    # number_of_flaps = 10
    #this number can be increased but this is for testing pourposes
    # max baudrate is 4.5Mbps
    # velocity_limit = 1311 #this is for ~300rev/min
    dynamxel_velocity_conversion = lambda velocity : int(velocity*4.366797)
    dynamxel_acceleration_converstion = lambda acceleration: int(acceleration/214.577)
    velocity = lambda flaps_ps : (float(flaps_ps*60.0))
    acceleration = lambda flaps_ps, max_velocity : (float((360.0*flaps_ps))*max_velocity)

    ph = PacketHandler(INPUT_TABLE['protocol'])
    
    # init of serial port and baudrate
    try:
        os.system('sudo chmod 777 %s' % DEVICE_NAME)
        if port_num.openPort():
            print("Succeeded to open the port!")
        else:
            print('Unable to open port')
            return 0
    except SerialException:
        print('could not find / permission is denied for device : %s' % DEVICE_NAME)
        
        return 0
    # except : 

    if port_num.setBaudRate(BAUDRATE):
        print('BaudRate set to', BAUDRATE)
    else:
        print('BaudRate could not be set')
        return 0
    ph.write1ByteTxRx(port_num, INPUT_TABLE['id'], INPUT_TABLE['control']['id'], INPUT_TABLE['control']['position']) #this enables position control
    ph.write1ByteTxRx(port_num, INPUT_TABLE['id'], INPUT_TABLE['tourque']['id'], INPUT_TABLE['tourque']['enable'])
    if ph.read1ByteTxRx(port_num, INPUT_TABLE['id'], INPUT_TABLE['tourque']['id'])[0] != 1: #comm sucess is 0
        print('setting tourque failed')
        return 0
    else:
        print("Dynamixel has been successfully connected")
    ph.write4ByteTxRx(port_num, INPUT_TABLE['id'], INPUT_TABLE['position']['id'], INPUT_TABLE['position']['mid_value'])
    sleep(1) #sleep for one second for init

    # ph.write1ByteTxRx(port_num, dynamxel_id, tourque_enable_id, tourque_disable)
    # sleep(1)
    #position control is not a great idea for this setup because it tries to move to poaint A to point B as fast as it can
    #velocity control is a better bet

    # for this is going to be a a profile of the max points of the position with a wait until done script completed to do the next rotationb back
    # https://emanual.robotis.com/docs/en/dxl/x/xl330-m077/#profile-acceleration
 
    #max velocity i have been using is 300 rev/min. we can crank this up as we go but for right now
    #aslo ned to figure out how to incorperate

    myvelocity = velocity(myflaps_ps)
    if(myvelocity > VELOCITY_LIMIT):
        # theroetical flapsps for max velocity is around 4.5 fps for 270r/min
        # to get somthing hirger than this we need to edit positional data

        # (270/60)*(1/fps)
        INPUT_TABLE['position']['max_value'] = INPUT_TABLE['position']['max_value'] - int(INPUT_TABLE['position']['min_value']*(VELOCITY_LIMIT/60)/flaps_ps)
        INPUT_TABLE['position']['min_value'] = INPUT_TABLE['position']['min_value'] + int(INPUT_TABLE['position']['min_value']*(VELOCITY_LIMIT/60)/flaps_ps)
        
        myvelocity = VELOCITY_LIMIT
        # if this is over the velocity limit then the bounds of max and min position should be changed
        # this should be done here
        

    myacceleration = acceleration(myflaps_ps, myvelocity)
    INPUT_TABLE['velocity_profile']['value'] = dynamxel_velocity_conversion(myvelocity)
    INPUT_TABLE['acceleration_profile']['value'] = dynamxel_acceleration_converstion(myacceleration) #FIXME make sure this is right

    print("Velocity : ", myvelocity)
    print("Accelleration : ", myacceleration )

    ph.write4ByteTxRx(port_num, INPUT_TABLE['id'], INPUT_TABLE['velocity_profile']['id'], INPUT_TABLE['velocity_profile']['value'])
    ph.write4ByteTxRx(port_num, INPUT_TABLE['id'], INPUT_TABLE['acceleration_profile']['id'], INPUT_TABLE['acceleration_profile']['value'])

    return [ph, port_num]

def motor_main(ph, port_num, number_of_flaps):
    # control code for flapping here

    start_time = time.time()
    while number_of_flaps > 0:
        ph.write4ByteTxRx(port_num, INPUT_TABLE['id'], INPUT_TABLE['position']['id'], INPUT_TABLE['position']['min_value'])
        while (ph.read4ByteTxRx(port_num, INPUT_TABLE['id'], INPUT_TABLE['position_monitor']['id'])[0] - INPUT_TABLE['position']['min_value']) >= 20:
            pass
        ph.write4ByteTxRx(port_num, INPUT_TABLE['id'], INPUT_TABLE['position']['id'], INPUT_TABLE['position']['max_value'])
        while (INPUT_TABLE['position']['max_value'] - ph.read4ByteTxRx(port_num, INPUT_TABLE['id'], INPUT_TABLE['position_monitor']['id'])[0]) >= 20:
            pass
        number_of_flaps -= 1
    return (time.time() - start_time)

def motor_exit(ph, port_num):
    ph.write4ByteTxRx(port_num, INPUT_TABLE['id'], INPUT_TABLE['position']['id'], INPUT_TABLE['position']['mid_value'])
    sleep(0.5)
    ph.write1ByteTxRx(port_num, INPUT_TABLE['id'], INPUT_TABLE['tourque']['id'], INPUT_TABLE['tourque']['disable'])
    if ph.read1ByteTxRx(port_num, INPUT_TABLE['id'], INPUT_TABLE['tourque']['id'])[0] != 0: #comm sucess is 0
        print('setting tourque failed')
        return 0
    else:
        print("Dynamixel has been successfully disconnected")
    
    print('Closing port..')
    port_num.closePort()

if __name__ == '__main__':
    flaps_ps = 5
    number_of_flaps = 10
    control = motor_init(flaps_ps)
#    print(control)

    #there are going to be two functions here for the paralization
    #init runner and exit

    motor_data = motor_main(control[0], control[1], number_of_flaps)

    print('Total time taken by motor: %f s' % motor_data)
    print('Flaps per second: %f ' % (number_of_flaps/motor_data))

    motor_exit(control[0], control[1])

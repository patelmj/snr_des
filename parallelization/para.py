#from threading import Thread
from multiprocessing.pool import ThreadPool
from time import time, sleep

from functs import *
from motor_control import motor_init, motor_main, motor_exit

def dataCollection(start,seconds,ms_step):
    overall=[]
    while time()-start<seconds:
        info_row = []
        ct = (time()-start)*1000 #ct is in Milliseconds
        info_row.append(ct)
        for channel in range(6):
            data = ai_device.a_in(channel, AiInputMode.SINGLE_ENDED, Range.BIP10VOLTS, AInFlag.DEFAULT)
            info_row.append(data)
            #print('Channel', channel, 'Data:', data)
        overall.append(info_row)
        #.01 = 10 miliseconds
        ms_interval = ms_step #this value must be in miliseconds, it is the step size in the data collection
        sleep((ms_interval-((time()-starttime)*1000)%ms_interval)/1000)
    return overall

def motors(control, flap_num):
    # motor control code runs off number of flaps needed. this can be changed by calculating the numbher of flaps to the number of flaps/ps
    # i should just be able to run the motor code and it should work with timing
    # while time()-start<seconds: #seconds is the amount of time to run
    #     ct = (time()-starttime)*1000 #ct is in Milliseconds


    # print("Hither I do Fancy Motor Stuffffffff")
    # sleep((10-((time()-starttime)*1000)%10)/1000)

    return motor_main(control[0], control[1], flap_num)
    # this will flap the wing to the specified flap num and flaps ps set in the motor_init
    # this will also print how many times it would take to flap the wing

if __name__ == '__main__':

    #Do Init stuff
    step_ms=5 #5 is the lowest it will go
    #FIXME add Motor INIT stuff here
    flaps_ps = 4.5
    flap_num = 15
    error = 4 # error is 5 seconds since i dont think it would be exactly what the fps is 
    runtime = (1/flaps_ps * flap_num) + error
    control = motor_init(flaps_ps)

    #Daq Init work
    daq_device,ai_device,ai_info = daq_init()
    #THIS IS DAQ Calibration for any bias such as weight of motor
    input("Hit Enter if Ready for calibration")
    bias  = daq_calibration(ai_device,ai_info)
    input("Hit Enter if Ready To Run the System")
    # runtime = 5 # Ask for runtime in seconds here, currently hard coded to 5
    # look above for runtime calculation
    
    pool = ThreadPool(processes=2) #FIXME check if it is correct to set it up like this
    starttime = time()
    load_cell_thread = pool.apply_async(dataCollection,(starttime,runtime,step_ms))
    motor_thread = pool.apply_async(motors,(control, flap_num))

    data = load_cell_thread.get()
    motor_data = motor_thread.get()
    print('Total time taken by motor: %f s' % motor_data)
    print('Flaps per second: %f ' % (flap_num/motor_data))
    motor_exit(control[0], control[1])
    data_time,data = convertToForces(data,bias)
    graphing(data_time,data)
    printOutCSV(data_time,data,"./para_forces.csv")
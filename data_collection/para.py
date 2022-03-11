#from threading import Thread
from multiprocessing.pool import ThreadPool
from time import time, sleep

from functs import *


def dataCollection(start,seconds):
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
        sleep((10-((time()-starttime)*1000)%10)/1000)
    return overall

def motors(start,seconds):
    while time()-start<seconds: #seconds is the amount of time to run
        ct = (time()-starttime)*1000 #ct is in Milliseconds

    print("Hither I do Fancy Motor Stuffffffff")
    sleep((10-((time()-starttime)*1000)%10)/1000)

# class ThreadWithReturnValue(Thread):
#     def __init__(self, group=None, target=None, name=None,
#                  args=(), kwargs={}, Verbose=None):
#         Thread.__init__(self, group, target, name, args, kwargs)
#         self._return = None
#     def run(self):
#         print(type(self._target))
#         if self._target is not None:
#             self._return = self._target(*self._args,
#                                                 **self._kwargs)
#     def join(self, *args):
#         Thread.join(self, *args)
#         return self._return




if __name__ == '__main__':

    #Do Init stuff
    #FIXME add Motor INIT stuff here

    #Daq Init work
    daq_device,ai_device,ai_info = daq_init()
    #THIS IS DAQ Calibration for any bias such as weight of motor
    input("Hit Enter if Ready for calibration")
    bias  = daq_calibration(ai_device,ai_info)
    input("Hit Enter if Ready To Run the System")
    runtime = 5 #FIXME Ask for runtime in seconds here, currently hard coded to 5
    
    pool = ThreadPool(processes=2) #FIXME check if it is correct to set it up like this
    starttime = time()
    load_cell_thread = pool.apply_async(dataCollection,(starttime,runtime))
    motor_thread = pool.apply_async(motors,(starttime,runtime))

    data = load_cell_thread.get()
    data_time,data = convertToForces(data,bias)
    graphing(data_time,data)
    printOutCSV(data_time,data,"./para_forces.csv")

    #print(data)

    # load_cell_thread = ThreadWithReturnValue(target = dataCollection(starttime,bias,runtime))
    # #motor_thread = Thread(target = motors(starttime,runtime))
    # load_cell_thread.start()
    # #motor_thread.start()
    # data = load_cell_thread.join()

    #Closing Arguments
    #Make this a function?
    #Write out the daq
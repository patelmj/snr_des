import numpy as np
from uldaq import (get_daq_device_inventory, DaqDevice, InterfaceType, AiInputMode, Range, AInFlag)
import csv
import matplotlib.pyplot as plt

conversion_matrix = [ #FT15818                                              WE are going to use this matrix becuase it is closer to the value that we are supposed to get
        [-0.00295,0.05062,0.06534,-3.42427,0.00226,3.4506],
        [0.08082,3.9462,0.0294,-1.91818,0.01453,-2.01788],
        [3.78816,-0.0191,3.77722,0.03131,3.80022,-0.01551],
        [-0.51347,24.11865,20.47774,-11.59215,-21.65748,-12.16591],
        [-24.66476,-0.23545,11.42543,21.02987,11.97242,-21.17553],
        [0.37493,14.52237,-0.26515,13.73721,0.07084,14.76302]
    ]
file_header = ["time(ms)","fx","fy","fz","tx","ty","tz"]

def daq_init():
    # Get a list of available DAQ devices
    devices = get_daq_device_inventory(InterfaceType.USB)
    # Create a DaqDevice Object and connect to the device
    daq_device = DaqDevice(devices[0])
    daq_device.connect()
    # Get AiDevice and AiInfo objects for the analog input subsystem
    ai_device = daq_device.get_ai_device()
    ai_info = ai_device.get_info()
    return daq_device,ai_device, ai_info

def daq_calibration(ai_device, ai_info):
    bias = []
    for channel in range(6):
        data = ai_device.a_in(channel, AiInputMode.SINGLE_ENDED, Range.BIP10VOLTS, AInFlag.DEFAULT)
        bias.append(data)
    print(f"Bias: {bias}")
    return bias 

def convertToForces(data,bias):
    time = np.array(data)[:,0]
    data = np.subtract(np.delete(data,0,1),bias) #FIXME, check if this is correct at some point. I think its right
    data = np.array(data)
    data = np.matmul(conversion_matrix,data.transpose()).transpose()
    return time,data

def graphing(time,data):
    figure, axis = plt.subplots(2,1)
    fx = data[:,0]
    fy = data[:,1]
    fz = data[:,2]
    tx = data[:,3]
    ty = data[:,4]
    tz = data[:,5]
    axis[0].plot(time,fx,label = "Fx")
    axis[0].plot(time,fy,label = "Fy")
    axis[0].plot(time,fz,label = "Fz")
    axis[0].legend()
    axis[1].plot(time,tx,label = "Tx")
    axis[1].plot(time,ty,label = "Ty")
    axis[1].plot(time,tz,label = "Tz")
    axis[1].legend()
    plt.show()


def printOutCSV(time,data,filename):
    out = np.concatenate((time[:,np.newaxis],data),axis=1)
    with open(filename,'w') as file:
        writer = csv.writer(file)
        writer.writerow(file_header)
        writer.writerows(out)

def disconnectDaq(device):
    device.disconnect()
    device.release()
##Test Script from uldaq

from uldaq import (get_daq_device_inventory, DaqDevice, InterfaceType, AiInputMode, Range, AInFlag)
import csv
from time import time,sleep
import numpy as np
#import pandas as pd
import matplotlib.pyplot as plt
#import threading

#Seconds parameter to figure out how long to collect data for
seconds = 5


file_header = ["time(ms)","fx","fy","fz","tx","ty","tz"]#,"c6","c7","c8","c9","c10","c11","c12","c13","c14","c15"]

try:
    # Get a list of available DAQ devices
    devices = get_daq_device_inventory(InterfaceType.USB)
    # Create a DaqDevice Object and connect to the device
    daq_device = DaqDevice(devices[0])
    daq_device.connect()
    # Get AiDevice and AiInfo objects for the analog input subsystem
    ai_device = daq_device.get_ai_device()
    ai_info = ai_device.get_info()

    # Read and display voltage values for all analog input channels
    overall = []
    starttime = time()#this is in seconds
    while time()-starttime< seconds: #collect data for a min = 60, 20 seconds = 20        
        info_row= []
        ct = (time()-starttime)*1000 #ct is in Milliseconds
        info_row.append(ct)

        for channel in range(ai_info.get_num_chans()): #changing it to range(6) works? I think- Mugi
            data = ai_device.a_in(channel, AiInputMode.SINGLE_ENDED, Range.BIP10VOLTS, AInFlag.DEFAULT)
            if channel >5: #Channels that have our data, 0,1,2,3,4,5,6, based off Kevin and Mugi's Analysis
                break
            info_row.append(data)
            #print('Channel', channel, 'Data:', data)
        overall.append(info_row)
        #.01 = 10 miliseconds
        sleep((10-((time()-starttime)*1000)%10)/1000)

    conversion_matrix = [ #FT15818                                              WE are going to use this matrix becuase it is closer to the value that we are supposed to get
        [-0.00295,0.05062,0.06534,-3.42427,0.00226,3.4506],
        [0.08082,3.9462,0.0294,-1.91818,0.01453,-2.01788],
        [3.78816,-0.0191,3.77722,0.03131,3.80022,-0.01551],
        [-0.51347,24.11865,20.47774,-11.59215,-21.65748,-12.16591],
        [-24.66476,-0.23545,11.42543,21.02987,11.97242,-21.17553],
        [0.37493,14.52237,-0.26515,13.73721,0.07084,14.76302]
    ]

    # conversion_matrix = [ #FT15819
    # [-0.00523,0.04788,0.06423,-3.42032,0.00131,3.44934],
    # [0.07999,3.9423,0.02829,-1.91718,0.0149,-2.0155],
    # [3.78414,-0.01983,3.77658,0.03099,3.79866,-0.01396],
    # [-0.39449,24.16045,20.58647,-11.5674,-21.52246,-12.24986],
    # [-24.68076,-0.21799,11.34409,20.98826,11.91443,-21.15598],
    # [0.35491,14.31408,-0.26424,13.83239,0.09919,114.81632]
    # ]
    
    #Change this to be Bias = first row 
    bias = [0.15437995145475725, 0.23347750437096693, -0.2867530412913766, 0.8718854215840111, 0.17688992698822403, 0.9641137935614097]
    #overall=np.array(overall)
    time = np.array(overall)[:,0]
    #print(time)
    overall = np.subtract(np.delete(overall,0,1),bias)#Fix I dropped the time column
    overall = np.array(overall)
    overall = np.matmul(conversion_matrix,overall.transpose()).transpose()
    
    print(overall)
    out = np.concatenate((time[:,np.newaxis],overall),axis=1)
    with open("./dataset_matrix18.csv",'w') as file:
        writer = csv.writer(file)
        writer.writerow(file_header)
        writer.writerows(out)

    daq_device.disconnect()
    daq_device.release()

except ULException as e:
    print('\n', e)  # Display any error messages



figure, axis = plt.subplots(2,1)

fx = overall[:,0]
fy = overall[:,1]
fz = overall[:,2]

tx = overall[:,3]
ty = overall[:,4]
tz = overall[:,5]
#Fix LABELS in subplotting https://matplotlib.org/3.5.1/gallery/text_labels_and_annotations/label_subplots.html
axis[0].plot(time,fx,label = "Fx")
axis[0].plot(time,fy,label = "Fy")
axis[0].plot(time,fz,label = "Fz")
axis[0].legend()

axis[1].plot(time,tx,label = "Tx")
axis[1].plot(time,ty,label = "Ty")
axis[1].plot(time,tz,label = "Tz")
axis[1].legend()
plt.show()

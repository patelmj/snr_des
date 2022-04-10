#pip install scipy
#pip install pandas
#pip install matplotlib

'''
This Script is created to test out a bandpass filter on the data and to see how it would look
'''

from scipy.signal import filtfilt, find_peaks
from scipy.fft import fft, fftfreq

import math
import scipy
import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def plot():
    #data = pd.read_csv("../data/fake_wing_single_foam.csv")
    data = pd.read_csv("../data/actual_single_foam.csv")
    #data = pd.read_csv("../data/just_motor2.csv")
    #To Cut out 2 thirds of the data to see the middle portion, do the following
    #data = data[1240:2480]
    data = data[2000:2480]

    raw_data = data[['tz']]
    raw_data = np.array(raw_data)
    time= np.array(data[["time(ms)"]])
    print(time[-1])
    figure,axis =plt.subplots(3,1)
    #The following is for plotting the x and y label for the whole plot
    #figure.add_subplot(111,frame_on=False)
    #plt.tick_params(labelcolor="none",bottom=False,left=False)
    #plt.xlabel("time (ms)")
    #plt.ylabel("Torque (Nmm)")
    axis[0].plot(time,raw_data,label = "Torque Lift Axis")
    axis[0].set(xlabel="time (ms)",ylabel='Torque (Nmm)')
    axis[0].legend()
    axis[0].set(xlabel="time (ms)",ylabel='Torque (Nmm)')
    axis[1].set(xlabel="time (ms)",ylabel='Torque (Nmm)')
    axis[2].set(xlabel="time (ms)",ylabel='Torque (Nmm)')


    filtered_sig=bandPass(raw_data)
    axis[1].plot(time,filtered_sig,label="Filtered")
    #axis[1].xlabel("time (ms)")
    #axis[1].ylabel("Torque (Nmm)")
    axis[1].legend()
    #Getting the rectified Signal
    full_rect_data = np.where(filtered_sig<0,filtered_sig*-1,filtered_sig)
    axis[2].plot(time,full_rect_data,label = "Signal Rectified")
    
    test = list(full_rect_data.flatten()) #converting from ndarray to regular array
    #print(list(result.flatten()))
    #peaks,_ = find_peaks(test,height=5) #The 5 is so that I ignore weird values that are lower in the signal, that are prolly due to doing wave rectification and filtering
    peaks,_ = find_peaks(test)
    axis[2].plot(time[peaks],full_rect_data[peaks],"x")
    #Finding average of the peaks
    avg_peak_torque = sum(full_rect_data[peaks])/len(full_rect_data[peaks])
    axis[2].axhline(y=avg_peak_torque,color='r',label=f'Avg Peak Tz: {avg_peak_torque[0]:0.2f}')
    #Then doing 2*avg/Pi because thats how u find the average via integration 
    avg_tz=(avg_peak_torque*2)/math.pi
    axis[2].axhline(y=avg_tz,color='c',label =f"Avg Tz: {avg_tz[0]:0.2f}")
    print(f"Force Avg Tz: {avg_tz}")

    axis[2].legend()




    plt.show()

def bandPass(signal):
    fs      = 100.0 #This is the sample frequency that we are using in our data, 10 ms
    lowcut  = 1.0
    highcut = 10.0
    nyq     = 0.5*fs
    low     = lowcut/nyq
    high    = highcut/nyq
    order   = 2
    b,a = scipy.signal.butter(order,[low,high],'bandpass',analog=False)
    y   = scipy.signal.filtfilt(b,a,signal,axis=0)
    return y

plot()
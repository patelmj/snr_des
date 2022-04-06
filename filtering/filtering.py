#pip install scipy
#pip install pandas
#pip install matplotlib

'''
This Script is created to test out a bandpass filter on the data and to see how it would look
'''
from scipy.signal import filtfilt
from scipy import stats
import scipy
import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def plot():
    data = pd.read_csv("../data/fake_wing_single_foam.csv")
    sensor_data = data[['tz']]
    sensor_data = np.array(sensor_data)
    time= np.array(data[["time(ms)"]])
    figure,axis =plt.subplots(2,1)
    axis[0].plot(time,sensor_data,label = "Raw")
    axis[0].legend()
    filtered_sig=bandPass(sensor_data)
    axis[1].plot(time,filtered_sig,label="Filtered")
    axis[1].legend()
    plt.show()

def bandPass(signal):
    fs      = 100.0 #This is the sample frequency that we are using in our data, 10 ms
    lowcut  = 1.0
    highcut = 5.0
    nyq     = 0.5*fs
    low     = lowcut/nyq
    high    = highcut/nyq
    order   = 2
    b,a = scipy.signal.butter(order,[low,high],'bandpass',analog=False)
    y   = scipy.signal.filtfilt(b,a,signal,axis=0)
    return y
plot()
#trying something to fill fft gaps and do an FFT
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import filtfilt, find_peaks
from scipy.fft import fft, fftfreq

data = pd.read_csv("../data/actual_single_foam.csv")
time = np.array(data[["time(ms)"]])
time = time.astype(int)
data[["time(ms)"]] = time
data = data.set_index('time(ms)')
#print(data)
new_index=list(*[range(0,time[-1][0]+10,10)])
#print(new_index)
data = data.reindex(new_index)
data = data.reset_index()
#print(data)




##FFT code?
SAMPLE_RATE = 100 #Hertz 1/ 10 ms
#data.iloc[-1].name gives me the last index value and i want to round all my points till im the nearest thousands
last_sec= round(data.iloc[-1].name,-2)
print(last_sec)
data = data.head(last_sec)
data=data.interpolate()
print(data)
#@print(data)
Duration = int(last_sec/100)  #needs to be in seconds

raw_data = data[['tz']]
yf = fft(raw_data)
xf = fftfreq(SAMPLE_RATE*Duration, 1 / SAMPLE_RATE)
data.to_csv('test.csv')
plt.plot(xf, np.abs(yf))
plt.show()
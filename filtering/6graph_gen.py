import math
from plistlib import FMT_XML
from turtle import color
import scipy
import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

data = pd.read_csv("../data/actual_single_foam.csv")
data = data[2200:2480]


fz = np.array(data[['fz']])
fx = np.array(data[['fx']])
fy = np.array(data[['fy']])

tz = np.array(data[['tz']])
tx = np.array(data[['tx']])
ty = np.array(data[['ty']])
time= np.array(data[["time(ms)"]])

figure,axis =plt.subplots(3,2)

axis[0][0].plot(time,fz,label = "Force fz: Lift Axis",color='#F10F0F')
axis[0][0].set(xlabel="time (ms)",ylabel='Force (N)')
axis[0][0].legend(loc="upper right")

axis[1][0].plot(time,fx,label = "Force fx Axis",color='#FE7300')
axis[1][0].set(xlabel="time (ms)",ylabel='Force (N)')
axis[1][0].legend(loc="upper right")

axis[2][0].plot(time,fy,label = "Force fy Axis",color='#FEA100')
axis[2][0].set(xlabel="time (ms)",ylabel='Force (N)')
axis[2][0].legend(loc="upper right")
#Torques
axis[0][1].plot(time,tz,label = "Torque tz: Lift Axis",color='#3157F2')
axis[0][1].set(xlabel="time (ms)",ylabel='Torque (Nmm)')
axis[0][1].legend(loc="upper right")

axis[1][1].plot(time,tx,label = "Torque tx Axis",color='#00BDFF')
axis[1][1].set(xlabel="time (ms)",ylabel='Torque (Nmm)')
axis[1][1].legend(loc="upper right")

axis[2][1].plot(time,ty,label = "Torque ty Axis",color='#2BED92')
axis[2][1].set(xlabel="time (ms)",ylabel='Torque (Nmm)')
axis[2][1].legend(loc="upper right")
#axis.legend(loc="upper right")

plt.show()
from time import sleep
from math import sin, radians
from numpy import array
import matplotlib.pyplot as plt

#do not use, this is the old way of doing thing and is outdated

myplot = []
myplot2 = []
mystep = 5
min_pos = int(4095/4)
max_pos = int(4095/2)+min_pos+3
print("min_pos: " + str(min_pos) + " max_pos: " + str(max_pos))
position = lambda index : (float((max_pos - min_pos) + (min_pos * sin(radians(index)))))
derivative = lambda index : (float(myplot[index]) - float(myplot[index-1]))
max_rps = 30.0/60.0

periods = 5
count = 0
for period in range(0, periods, 1):
    for i in range(90, 270, mystep):
        sinfunct = position(i)
        myplot.append(sinfunct)
        # print("i: " + str(i) + " rad: " + str((radians(i))) + " funct : " + str(sinfunct))
        # print("x2: " + str((myplot[count])) + " x1: " + str((myplot[count-1])) + " x2-x1: " + str((myplot[count] - myplot[count-1])))
        # print("count: " + str(count))
        # print(len(myplot))
        if i == 90 and period == 0:
            myplot2.append(0)
        else:
            myplot2.append(derivative(count))
        count += 1
        
    for i in range(270, 90, (-1)*mystep):
        sinfunct = position(i)
        myplot.append(sinfunct)
        # print("i: " + str(i) + " rad: " + str((radians(i))) + " funct : " + str(sinfunct))
        # print("x2: " + str((myplot[count])) + " x1: " + str((myplot[count-1])) + " x2-x1: " + str((myplot[count] - myplot[count-1])))
        # print("count: " + str(count))
        myplot2.append(derivative(count))
        count += 1

time = []
flaps_ps = 10.0
time_funct = lambda index : float(index*mystep/(flaps_ps*60.0*6))
for i in range(len(myplot)):
    time.append(time_funct(i))

xpoints = array(time)
ypoints_pos = array(myplot)
ypoints_der = array(myplot2)
# print(myplot2)

plt.subplot(1,2,1, title='position')
plt.plot(xpoints, ypoints_pos, color='r')
plt.subplot(1,2,2, title='velocity')
plt.plot(xpoints, ypoints_der, color='b')
plt.show()
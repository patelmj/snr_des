import csv
import numpy as np
import pandas as pd

#For this script we are using the lego weight object that was exactly 98.34 grams
#This should amount to about .964385 newtons

#Based off this analysis we are using the matrix 18 data as it is closer in value but isoff by about .05 newtons

'''
Output:

Avg 18 Matrix: time(ms)    2490.328992
fx            -0.001432
fy            -0.016416
fz            -1.012146
tx             1.268897
ty             2.341431
tz            -0.020400
dtype: float64
Avg 19 Matrix: time(ms)    2490.249196
fx            -0.000991
fy            -0.016096
fz            -1.011211
tx             1.237017
ty             2.353890
tz             0.083766
'''

data18 = pd.read_csv('dataset_matrix18.csv')
data19 = pd.read_csv('dataset_matrix19.csv')

avg18 = data18.mean()
avg19 = data19.mean()

print(f"Avg 18 Matrix: {avg18}")
print(f"Avg 19 Matrix: {avg19}")
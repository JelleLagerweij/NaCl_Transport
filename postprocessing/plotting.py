# -*- coding: utf-8 -*-
"""
Created on Thu Feb 16 16:33:01 2023

@author: Jelle
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
plt.close('all')
plt.rcParams['svg.fonttype'] = 'none'


t = [0.25, 0.5, 0.75, 1, 1.25, 1.5, 1.75, 2, 3, 5, 6, 7, 8, 9, 10, 12.5, 15,
     17.5, 20, 25, 30, 35, 40, 45, 50]

time = [0]*len(t)
for dt in range(1, 3):
    for i in range(len(t)):
        st1 = "../stored/dt_" + str(dt) + "/0"
        st2 = "../stored/dt_" + str(dt) + "/"
        st3 = "Mstep.csv"
        if t[i] < 10:
            time[i] = st1 + "{:.2f}".format(round(t[i], 2)) + st3
        else:
            time[i] = st2 + "{:.2f}".format(round(t[i], 2)) + st3

    properties = list(pd.read_csv(time[0]).columns.values)[1:]

    for i in range(len(properties)):
        data = np.zeros(len(time))
        data_error = np.zeros(len(time))

        for j in range(len(time)):
            info = pd.read_csv(time[j])[properties[i]]
            data[j] = info[0]
            data_error[j] = info[1]

        data = np.nan_to_num(data)
        data_error = np.nan_to_num(data_error)

        plt.figure(properties[i])
        plt.plot(np.array(t)*dt, data, marker='.')
        plt.fill_between(np.array(t)*dt, data-data_error, y2=data+data_error, alpha=.25)
        plt.xlabel('runtime/[ns]')
        plt.ylabel(properties[i])
        # plt.xlim(2, 24)
        # plt.ylim(min(data[:12]-data_error[:12]), max(data[:12]+data_error[:12]))

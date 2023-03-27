# -*- coding: utf-8 -*-
"""
Created on Thu Feb 16 16:33:01 2023

@author: Jelle
"""

import numpy as np
from scipy.optimize import curve_fit
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import (MultipleLocator)
plt.close('all')
plt.rcParams['text.usetex'] = True
import seaborn as sns
sns.set_theme(style='white')

# My Data
folder = ['../runningS/m_1', '../runningS/m_2', '../runningS/m_4', '../runningS/m_6']
file = '/postprocessed.csv'

m = np.array([1, 2, 4, 6])
m_real = np.zeros(len(m))
E_Ons = np.zeros(len(m))
E_Ons_err = np.zeros(len(m))

E_NE = np.zeros(len(m))
E_NE_err = np.zeros(len(m))

for i in range(len(m)):
    data = pd.read_csv(folder[i]+file)
    m_real[i] = data['Molality/[mol/kg]'][0]

    E_Ons[i] = data['E conduct Ons/[S/m]'][0]
    E_Ons_err[i] = data['E conduct Ons/[S/m]'][1]

    E_NE[i] = data['E conduct NEYH_cor /[S/m]'][0]
    E_NE_err[i] = data['E conduct NEYH_cor /[S/m]'][1]


# Vega Data
E_Ons_V = np.array([7.13, 14.10, 20.08, 23.27])
E_Ons_V_err = np.array([8.68, 15.61, 21.60, 24.79]) - E_Ons_V

E_NE_V = np.array([10.63, 18.83, 29.85, 35.29])
E_NE_V_err = np.zeros(len(m))

# # DATA GATHERING DONE
# # Plotting Madrid versus Delft
# fig = plt.figure('OCTP and Vega', figsize=(4.5, 4.5), dpi=800)
# ax = fig.add_axes([0, 0, 0.9, 0.9])
# sns.set_theme(style='white')
# for axis in ['top', 'bottom', 'left', 'right']:
#     ax.spines[axis].set_linewidth(2.5)

# ax.xaxis.set_tick_params(width=2)
# ax.yaxis.set_tick_params(width=2)
# ax.tick_params(which='both', width=2, direction='out', left=True, bottom=True)
# ax.tick_params(which='major', length=7)
# ax.tick_params(which='minor', length=4)
# plt.xticks(fontsize=18, rotation=0)
# plt.yticks(fontsize=18)
# sns.set_theme(style='white')

# cm = plt.cm.get_cmap('tab10')
# plt.errorbar(m_real, E_Ons, yerr=E_Ons_err, color=cm(0), fmt='o', capsize=11,
#               elinewidth=2, capthick=2, markersize=9, label=r'E $\sigma$')
# plt.errorbar(m_real, E_NE, yerr=E_NE_err, color=cm(1), fmt='<', capsize=11,
#               elinewidth=2, capthick=2, markersize=9, label=r'E $\sigma_{NE+YH}$')
# plt.errorbar(m, E_Ons_V, yerr=E_Ons_V_err, color=cm(2), fmt='o', capsize=11,
#               elinewidth=2, capthick=2, markersize=9, label=r'GK $\sigma$')
# plt.scatter(m, E_NE_V, color=cm(3), marker='>', s=64, label=r'GK $\sigma_{NE+YH}$')

# plt.xlabel('$m$/[mol/kg]', fontsize=22)
# plt.ylabel('$\sigma$/[S/m]', fontsize=22)
# plt.xlim(0, 6.3)
# plt.ylim(0, 50)
# plt.xticks(fontsize=18, rotation=0)
# plt.yticks(fontsize=18)

# handles, labels = plt.gca().get_legend_handles_labels()
# order = [1, 2, 3, 0]
# leg = ax.legend([handles[idx] for idx in order], [labels[idx] for idx in order],
#                 fontsize=12, labelspacing=0.4, loc='upper left')
# leg.get_frame().set_edgecolor('0')
# leg.get_frame().set_linewidth(2.0)
# plt.savefig('Delft_Madrid_NaCl.pdf', bbox_inches='tight')


# Now for system size effects
def fitting(L, data, data_err):
    # We want to investigate the scaling of the inverse properties.
    x = np.array([-.1, 0, 0.1, 0.3, 0.5, 0.6])
    L = 1/L
    d_L = L[1]-L[0]

    y1 = data[0] + data_err[0]
    y2 = data[1] - data_err[1]
    low = (x*(y2-y1)/d_L) + (L[1]*y1 - L[0]*y2)/d_L

    y1 = data[0] - data_err[0]
    y2 = data[1] + data_err[1]
    up = (x*(y2-y1)/d_L) + (L[1]*y1 - L[0]*y2)/d_L

    mid = (up+low)/2
    return x, mid, up, low

folder1 = ['../runningS/m_1', '../runningS/m_2', '../runningS/m_6']
folder2 = ['../Parsa/18', '../Parsa/36', '../Parsa/108']
file = '/postprocessed.csv'
m = [1, 2, 6]
m_real = np.zeros(len(folder1))

E_Ons = np.zeros((len(folder1), 2))
E_Ons_err = np.zeros((len(folder), 2))

E_NE = np.zeros((len(folder1), 2))
E_NE_err = np.zeros((len(folder1), 2))

E_NE_YH = np.zeros(len(folder))
E_NE_YH_err = np.zeros(len(folder))

L_box = np.zeros((len(folder1), 2))
L_box_err = np.zeros((len(folder1), 2))

for i in range(len(folder1)):
    data = pd.read_csv(folder1[i]+file)
    m_real[i] = data['Molality/[mol/kg]'][0]

    E_Ons[i, 0] = data['E conduct Ons/[S/m]'][0]
    E_Ons_err[i, 0] = data['E conduct Ons/[S/m]'][1]
    E_NE[i, 0] = data['E conduct NE/[S/m]'][0]
    E_NE_err[i, 0] = data['E conduct NE/[S/m]'][1]
    L_box[i, 0] = data['Box size/[m]'][0]
    L_box_err[i, 0] = data['Box size/[m]'][1]

    data = pd.read_csv(folder2[i]+file)
    E_Ons[i, 1] = data['E conduct Ons/[S/m]'][0]
    E_Ons_err[i, 1] = data['E conduct Ons/[S/m]'][1]
    E_NE[i, 1] = data['E conduct NE/[S/m]'][0]
    E_NE_err[i, 1] = data['E conduct NE/[S/m]'][1]
    L_box[i, 1] = data['Box size/[m]'][0]
    L_box_err[i, 1] = data['Box size/[m]'][1]

    E_NE_YH[i] = data['E conduct NEYH_cor /[S/m]'][0]
    E_NE_YH_err[i] = data['E conduct NEYH_cor /[S/m]'][1]

L_box *= 1e9
L_box_err *= 1e9

fig = plt.figure('system size effects', figsize=(4.5, 4.5), dpi=800)
ax = fig.add_axes([0, 0, 0.9, 0.9])
sns.set_theme(style='white')
for axis in ['top', 'bottom', 'left', 'right']:
    ax.spines[axis].set_linewidth(2.5)

ax.xaxis.set_tick_params(width=2)
ax.yaxis.set_tick_params(width=2)
ax.tick_params(which='both', width=2, direction='out', left=True, bottom=True)
ax.tick_params(which='major', length=7)
ax.tick_params(which='minor', length=4)

cm = plt.cm.get_cmap('tab10')
marker = ['o', '>', 's', '^']

for i in range(len(m)):
    string = r'$m= $' + str(m[i]) + r' $\sigma$'
    plt.errorbar(1/L_box[i, :], E_Ons[i, :], yerr=E_Ons_err[i, :], color=cm(2*i), fmt=marker[i], capsize=11, elinewidth=2, capthick=2, markersize=9, label=string)
    x, mid, up, low = fitting(L_box[i, :], E_Ons[i, :], E_Ons_err[i, :])
    plt.plot(x, mid, color=cm(2*i))
    plt.errorbar(x[1], mid[1], yerr=up[1]-mid[1], color=cm(2*i), fmt=marker[i], capsize=10, elinewidth=2, capthick=2, markersize=9)
    print('Exact m=', m[i], 'L=', x[1], 'cond =', mid[1], 'pm', up[1]-mid[1])
    
    string = r'$m= $' + str(m[i]) + r' $\sigma_{NE}$'
    plt.errorbar(1/L_box[i, :], E_NE[i, :], yerr=E_NE_err[i, :], color=cm(2*i+1), fmt=marker[i], capsize=11, elinewidth=2, capthick=2, markersize=9, label=string)
    plt.hlines(E_NE_YH[i], -0.1, 1, color=cm(2*i+1), linestyles=':')
    x, mid, up, low = fitting(L_box[i, :], E_NE[i, :], E_NE_err[i, :])
    plt.plot(x, mid, color=cm(2*i+1))
    plt.errorbar(x[1], mid[1], yerr=up[1]-mid[1], color=cm(2*i+1), fmt=marker[i], capsize=11, elinewidth=2, capthick=2, markersize=9)
    print('NE m=', m[i], 'L=', x[1], 'cond =', mid[1], 'pm', up[1]-mid[1])

plt.xlabel(r'$L^{-1}$/[nm$^{-1}$]', fontsize=22)
plt.ylabel(r'$\sigma$/[S/m]', fontsize=22)
plt.xlim(0.1, 0.6)
plt.ylim(0, 42)
plt.xticks(fontsize=18, rotation=0)
plt.yticks(fontsize=18)
handles, labels = plt.gca().get_legend_handles_labels()
order = [0, 2, 4, 1, 3, 5]
leg = ax.legend([handles[idx] for idx in order], [labels[idx] for idx in order],
                fontsize=12, labelspacing=0.4, loc='upper right', ncol=2, framealpha=1)

ax2 = ax.twiny()
new_tick_values = np.array([10000, 1000, 500, 250])
new_tick_locations = np.power(31.436032/new_tick_values, 1/3)
ax2.set_xlim(ax.get_xlim())
ax2.set_xticks(new_tick_locations)
ax2.set_xticklabels(new_tick_values)
ax2.set_xlabel(r"$n_{w}$", fontsize=22)

plt.xticks(fontsize=18, rotation=0)
plt.yticks(fontsize=18)
sns.set_theme(style='white')

leg.get_frame().set_edgecolor('0')
leg.get_frame().set_linewidth(2.0)
plt.savefig('ScalingNaCl4.pdf', bbox_inches='tight')
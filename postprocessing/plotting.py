# -*- coding: utf-8 -*-
"""
Created on Thu Feb 16 16:33:01 2023

@author: Jelle
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import (MultipleLocator)
plt.close('all')
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

# Parsa Data
folder = ['../Parsa/18', '../Parsa/36', '../Parsa/108']
m_real_P = np.zeros(len(folder))
E_Ons_P = np.zeros(len(folder))
E_Ons_P_err = np.zeros(len(folder))

E_NE_P = np.zeros(len(folder))
E_NE_P_err = np.zeros(len(folder))

for i in range(len(folder)):
    data = pd.read_csv(folder[i]+file)
    m_real_P[i] = data['Molality/[mol/kg]'][0]

    E_Ons_P[i] = data['E conduct Ons/[S/m]'][0]
    E_Ons_P_err[i] = data['E conduct Ons/[S/m]'][1]

    E_NE_P[i] = data['E conduct NEYH_cor /[S/m]'][0]
    E_NE_P_err[i] = data['E conduct NEYH_cor /[S/m]'][1]

# DATA GATHERING DONE

# Plotting Madrid versus Delft
fig = plt.figure('OCTP and Vega', figsize=(4.5, 4.5), dpi=400)
ax = fig.add_axes([0, 0, 0.9, 0.9])
sns.set_theme(style='white')
for axis in ['top', 'bottom', 'left', 'right']:
    ax.spines[axis].set_linewidth(2.5)

ax.xaxis.set_tick_params(width=2)
ax.yaxis.set_tick_params(width=2)
ax.tick_params(which='both', width=2, direction='out', left=True, bottom=True)
ax.tick_params(which='major', length=7)
ax.tick_params(which='minor', length=4)
plt.xticks(fontsize=18, rotation=0)
plt.yticks(fontsize=18)
sns.set_theme(style='white')


plt.errorbar(m_real, E_Ons, yerr=E_Ons_err, color='C0', fmt='o', capsize=8, label='Delft Einstein')
plt.errorbar(m_real, E_NE, yerr=E_NE_err, color='C1', fmt='<', capsize=8, label='Delft NE')
plt.errorbar(m, E_Ons_V, yerr=E_Ons_V_err, color='C2', fmt='o', capsize=8, label='Madrid GK')
plt.scatter(m, E_NE_V, color='C3', marker='>', label='Madrid NE')
plt.xlabel('molality/[mol/kg]', fontsize=22)
plt.ylabel('$\sigma$/[S/m]', fontsize=22)
plt.xlim(0, 6.3)
plt.ylim(0, 39)
plt.xticks(fontsize=18, rotation=0)
plt.yticks(fontsize=18)

handles, labels = plt.gca().get_legend_handles_labels()
order = [1, 2, 3, 0]
leg = ax.legend([handles[idx] for idx in order],[labels[idx] for idx in order],
                fontsize=11.5, labelspacing=0.25,loc='upper left')
leg.get_frame().set_edgecolor('0')
leg.get_frame().set_linewidth(2.0)
plt.savefig('Delft_Madrid_NaCl.pdf', bbox_inches='tight')



# Data again without molality 4
folder = ['../runningS/m_1', '../runningS/m_2', '../runningS/m_6']
file = '/postprocessed.csv'

m = np.array([1, 2, 6])
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
# Plotting system size effects
fig = plt.figure('System size effects', figsize=(4.5, 4.5), dpi=400)
ax = fig.add_axes([0, 0, 0.9, 0.9])
sns.set_theme(style='white')
for axis in ['top', 'bottom', 'left', 'right']:
    ax.spines[axis].set_linewidth(2.5)

ax.xaxis.set_tick_params(width=2)
ax.yaxis.set_tick_params(width=2)
ax.tick_params(which='both', width=2, direction='out', left=True, bottom=True)
ax.tick_params(which='major', length=7)
ax.tick_params(which='minor', length=4)
plt.xticks(fontsize=18, rotation=0)
plt.yticks(fontsize=18)
sns.set_theme(style='white')


plt.errorbar(m_real, E_Ons, yerr=E_Ons_err, color='C0', fmt='o', capsize=8, label='555 waters Einstein')
plt.errorbar(m_real, E_NE, yerr=E_NE_err, color='C1', fmt='<', capsize=8, label='Delft NE')
plt.errorbar(m_real_P, E_Ons_P, yerr=E_Ons_P_err, color='C2', fmt='o', capsize=8, label='1000 waters Einstein')
plt.errorbar(m_real_P, E_NE_P, yerr=E_NE_P_err, color='C3', fmt='>', capsize=8, label='1000 waters NE')
plt.xlabel('molality/[mol/kg]', fontsize=22)
plt.ylabel('$\sigma$/[S/m]', fontsize=22)
plt.xlim(0, 6.3)
plt.ylim(0, 49)
plt.xticks(fontsize=18, rotation=0)
plt.yticks(fontsize=18)

handles, labels = plt.gca().get_legend_handles_labels()
order = [0, 1, 2, 3]
leg = ax.legend([handles[idx] for idx in order], [labels[idx] for idx in order], fontsize=11.5, labelspacing=0.25, loc='upper left')
leg.get_frame().set_edgecolor('0')
leg.get_frame().set_linewidth(2.0)
plt.savefig('Systemsize_NaCl.pdf', bbox_inches='tight')
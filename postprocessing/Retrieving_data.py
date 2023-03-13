# -*- coding: utf-8 -*-
"""
Created on Wed Feb 15 14:29:42 2023

@author: Jelle
"""

import OCTP_postprocess_CLASS as octp
import uncertainties as unc
import scipy.constants as co


def cond_NE(octp, charges, YH_correction=True):
    # importing the correct properties
    groups = octp.groups
    N = octp.N_per_group

    V = octp.results['Volume/[m^3]'][0]
    V_err = octp.results['Volume/[m^3]'][1]
    V = unc.ufloat(V, V_err)

    T = octp.results['Temperature/[K]'][0]
    T_err = octp.results['Temperature/[K]'][1]
    T = unc.ufloat(T, T_err)

    if YH_correction is True:
        cor = 'YH_cor '
    else:
        cor = ''

    D = [0]*(len(groups))
    for i in range(len(groups)):
        Di = octp.results['Self diffusivity '+cor+groups[i]+'/[m^2/s]'][0]
        Di_err = octp.results['Self diffusivity '+cor+groups[i]+'/[m^2/s]'][1]
        D[i] = unc.ufloat(Di, Di_err)
    # setting up as uncertainties

    cond_NE_pos = D[1]*N[1]*(charges[0]*co.e)**2/(co.k*T*V)
    cond_NE_neg = D[2]*N[2]*(charges[1]*co.e)**2/(co.k*T*V)
    cond_NE = cond_NE_pos + cond_NE_neg

    words = 'E conduct NE' + cor + '/[S/m]'
    octp.results[words] = [cond_NE.n, cond_NE.s, len(octp.f_runs)]


def cond_Ons(octp, charges):
    # importing the correct properties
    N = sum(octp.N_per_group)

    V = octp.results['Volume/[m^3]'][0]
    V_err = octp.results['Volume/[m^3]'][1]
    V = unc.ufloat(V, V_err)

    T = octp.results['Temperature/[K]'][0]
    T_err = octp.results['Temperature/[K]'][1]
    T = unc.ufloat(T, T_err)

    Ons = octp.results['Onsager KK/[m^2/s]'][0]
    Ons_err = octp.results['Onsager KK/[m^2/s]'][1]
    Ons_pp = unc.ufloat(Ons, Ons_err)

    Ons = octp.results['Onsager KCl/[m^2/s]'][0]
    Ons_err = octp.results['Onsager KCl/[m^2/s]'][1]
    Ons_pm = unc.ufloat(Ons, Ons_err)

    Ons = octp.results['Onsager ClCl/[m^2/s]'][0]
    Ons_err = octp.results['Onsager ClCl/[m^2/s]'][1]
    Ons_mm = unc.ufloat(Ons, Ons_err)

    sig_pp = Ons_pp*(co.e**2*charges[0]**2*N)/(co.k*T*V)
    sig_pm = Ons_pm*(co.e**2*charges[0]*charges[1]*N)/(co.k*T*V)
    sig_mm = Ons_mm*(co.e**2*charges[1]**2*N)/(co.k*T*V)

    cond_Ons = sig_pp + 1*sig_pm + sig_mm
    words = 'E conduct Ons/[S/m]'
    octp.results[words] = [cond_Ons.n, cond_Ons.s, len(octp.f_runs)]

    words = 'sig ++/[S/m]'
    octp.results[words] = [sig_pp.n, sig_pp.s, len(octp.f_runs)]

    words = 'sig +-/[S/m]'
    octp.results[words] = [sig_pm.n, sig_pm.s, len(octp.f_runs)]

    words = 'sig --/[S/m]'
    octp.results[words] = [sig_mm.n, sig_mm.s, len(octp.f_runs)]


loc = '../stored/'

t = [0.25, 0.5, 0.75, 1, 1.25, 1.5, 1.75, 2, 3, 5, 6, 7, 8, 9, 10, 12.5, 15,
     17.5, 20, 25, 30, 35, 40, 45, 50]

time = [0]*len(t)
for dt in range(1, 3):
    for i in range(len(t)):
        if t[i] < 10:
            time[i] = "dt_" + str(dt) + "/0{:.2f}".format(round(t[i], 2)) + "Mstep"
        else:
            time[i] = "dt_" + str(dt) + "/{:.2f}".format(round(t[i], 2)) + "Mstep"

    for i in range(len(t)):
        # i = 20
        folder = loc+time[i]  # Path to the main folder

        f_runs = ['1', '2', '3', '4']  # All internal runs
        groups = ['wat', 'K', 'Cl']

        # Load the class
        mixture = octp.PP_OCTP(folder, f_runs, groups, dt=dt, plotting=False)

        # Change the file names
        mixture.filenames(Diff_Onsag='onsagercoefficient.dat',
                          T_conduc='thermconductivity.dat')

        mixture.changefit(Minc=12, Mmax=45)
        mixture.pressure(mov_ave=150)
        mixture.tot_energy(mov_ave=150)
        mixture.pot_energy(mov_ave=150)
        mixture.density()
        mixture.molarity('Cl')
        mixture.molality('Cl', 'wat', 18.01528)
        mixture.viscosity()
        mixture.thermal_conductivity()
        mixture.self_diffusivity(YH_correction=True, box_size_check=True)
        mixture.onsager_coeff(box_size_check=True)

        # Getting conductivity out of this
        cond_NE(mixture, [1, -1])
        cond_Ons(mixture, [1, -1])

        mixture.store(location='../stored/', name=time[i] + '.csv')
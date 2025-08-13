import numpy as np
import matplotlib.pyplot as plt
from Theoretical_AOA import *
from find_Toa_Def_temp import *
from blade_assembly_config import*
# Configuration of the blade assembly

def btt_simulation(reg_init,reg_end,reg_acc,xi,Na,Ra,f_resonance):

    # Configuration de la chaine d'acquisition
    fs = int(2.5 * 1e4)  # sampling frequency

    # Specification of the rotating speed of the engine

    Duration = (reg_end-reg_init)/reg_acc  # duration of the simulation
    time = np.arange(0, Duration + 1/fs, 1/fs)  # discrete time axis

    regime = reg_init + time * reg_acc

    # Generate blade vibration response
    #f_resonance = 3 * 1e3  # resonance frequency

    EO = 22  # Engine order
    Amax = 10  # maximum amplitude of the response in microns
    ######
    Position_Blade,Position_CTT,Nct = blade_assembly_config(Na)
    ######
    # Calculation of the theoretical angle of arrival of the blade without vibration
    theta = 2 * np.pi * np.cumsum(regime / 60) / fs  # angular displacement of the rotor or instantaneous position
    nbr_tour = np.fix((max(theta) - 2 * np.pi * (max(Position_CTT) - min(Position_Blade)) / 360) / (2 * np.pi))
    nbr_tour = int(nbr_tour)
    sens = "anhoraire"  # Choose the direction of the angular rotation
    theta_theoretical = Theoretical_AOA(Position_Blade, Position_CTT, nbr_tour, sens)
    # Calcul des Toa, ToaR et Def et organisation dans une structure de 3 elements
    ToaR_struct, Toa_struct, Def_struct, Reg_struct, amp_struct, phi_struct, noise_std = find_Toa_Def_temp(theta, theta_theoretical, time, regime, Ra, Position_CTT, EO, f_resonance, xi, Amax)
    return ToaR_struct, Toa_struct, Def_struct,Reg_struct,Na,nbr_tour,Nct,theta_theoretical
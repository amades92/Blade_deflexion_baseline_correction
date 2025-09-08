import sys
import os

# Ajoute le dossier parent du script au PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import numpy as np
from preprocessing.data_structuration import *
from preprocessing.accel_correct import *
from preprocessing.zeroing_function_ct import *

def center_time(Toa_struct, Ra, correc, select_revolution):
    # Calcul de la deflexion des aubes par center-time
    Na = Toa_struct.shape[0]
    nbr_tour = Toa_struct.shape[1]
    Nct = Toa_struct.shape[2]

    Toa_mat = data_structuration(Toa_struct, Na, nbr_tour, Nct)
    T_ref_CT = np.mean(Toa_mat, axis=1)  # Temps de référence par tour
    # Speed estimation and correction by interpolating
    Fr_CT = 1.0 / np.diff(T_ref_CT)  # Fréquence de rotation moyenne par tour
    Fr_CT = np.concatenate((Fr_CT, [Fr_CT[-1]]))  # Append last element
  
    Fr_struct_CT = accel_correc(T_ref_CT, Fr_CT, Toa_struct, correc)

    D = np.zeros((Na, nbr_tour, Nct))

    for i in range(Na):
        for k in range(Nct):
            D[i, :, k] = 2 * np.pi * Ra * Fr_struct_CT[i, :, k] * (Toa_struct[i, :, k] - T_ref_CT[:])

    Fr_CT = Fr_CT[select_revolution]
    Fr_struct_CT = Fr_struct_CT[:, select_revolution, :]
    D = D[:, select_revolution, :]

    return D, T_ref_CT, Fr_CT, Fr_struct_CT,Toa_mat

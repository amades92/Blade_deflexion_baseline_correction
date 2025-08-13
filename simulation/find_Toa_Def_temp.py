import numpy as np
from decimal import Decimal, getcontext
import math

def find_Toa_Def_temp(theta, theta_theoretical, time, regime, Ra, Position_CTT, EO, f_resonance, xi, Amax, snr=None):
    Na = theta_theoretical.shape[0]
    Nct = theta_theoretical.shape[2]
    getcontext().prec = 32
    time = time.flatten()
    regime = regime.flatten()

    w0 = 2 * np.pi * f_resonance

    phi_excitation = 2 * np.pi * EO * np.arange(Na) / Na

    ToaR_struct = np.zeros((Na, theta_theoretical.shape[1], Nct))
    Reg_struct = np.zeros((Na, theta_theoretical.shape[1], Nct))
    amp_struct = np.zeros((Na, theta_theoretical.shape[1], Nct))
    phi_struct = np.zeros((Na, theta_theoretical.shape[1], Nct))
    Def_struct = np.zeros((Na, theta_theoretical.shape[1], Nct))
    Toa_struct = np.zeros((Na, theta_theoretical.shape[1], Nct))
    Toa_struct_noise = np.zeros((Na, theta_theoretical.shape[1], Nct))
    Def_struct_noise = np.zeros((Na, theta_theoretical.shape[1], Nct))

    for i in range(Na):
        for k in range(Nct):
            AoA = theta_theoretical[i, :, k]

            ToaR_struct[i, :, k] = np.interp(AoA, theta, time)
            Reg_struct[i, :, k] = np.interp(AoA, theta, regime)
            w = 2 * np.pi * Reg_struct[i, :, k] * EO / 60
            amp_struct[i, :, k] = 1 / np.sqrt((2 * xi * w0 * w) ** 2 + (w0 ** 2 - w ** 2) ** 2)
            amp_struct[i, :, k] = Amax * amp_struct[i, :, k] / np.max(amp_struct[i, :, k])
            phi_struct[i, :, k] = phi_excitation[i] + np.arctan2(-2 * xi * w0 * w, (w0 ** 2 - w ** 2))

            Def_struct[i, :, k] = amp_struct[i, :, k] * np.sin(EO * np.deg2rad(Position_CTT[k]) + phi_struct[i, :, k])
            Toa_struct[i, :, k] = ToaR_struct[i, :, k] + Decimal((Def_struct[i, :, k] / (Ra * 2 * np.pi * Reg_struct[i, :, k] / 60)))

            # Ajout bruit SNR
            if snr is not None:
                var_signal = np.var(Toa_struct[i, :, k]) / (10**(snr/10))
                std_noise = np.sqrt(var_signal)
                noise = np.random.normal(0, 1, Toa_struct.shape[1])
                noise=noise*snr*1e-9
                Toa_struct_noise[i, :, k] = Toa_struct[i, :, k] + noise
                Def_struct_noise[i, :, k]= (Toa_struct_noise[i,:,k]-ToaR_struct[i, :, k])*(Ra * 2 * np.pi * Reg_struct[i, :, k] / 60)
            else:
                Toa_struct_noise[i, :, k] = Toa_struct[i, :, k]*(Ra * 2 * np.pi * Reg_struct[i, :, k] / 60)

            


    return ToaR_struct, Toa_struct, Toa_struct_noise, Def_struct, Def_struct_noise, Reg_struct, amp_struct, phi_struct, noise

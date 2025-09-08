def run_simulation(reg_init=5000, reg_end=8000, EO=22, Amax=10, xi=5 * 1.1 * 1e-3, f_resonance=2.5 * 1e3, snr=100):
    import sys
    import os

    # Ajoute le dossier parent du script au PYTHONPATH
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

    import numpy as np
    from simulation.Theoretical_AOA import Theoretical_AOA
    from simulation.find_Toa_Def_temp import find_Toa_Def_temp
    from data.blade_assembly_config import Na, Ra, Position_Blade, Position_CTT

    Duration = 5
    fs = int(2.5 * 1e4)
    time = np.arange(0, Duration + 1/fs, 1/fs)
    n = len(time)

    reg_init = 6000
    reg_end = 8000
    reg_acc = 200
    Duration = (reg_end - reg_init) / reg_acc
    time = np.arange(0, Duration + 1/fs, 1/fs)
    regime = reg_init + time * reg_acc

    f_resonance = 2.5 * 1e3
    xi = 1e-3
    Amax = 10
    EO = 22

    phi_excitation = 2 * np.pi * EO * np.arange(0, Na) / Na
    theta = 2 * np.pi * np.cumsum(regime / 60) / fs
    nbr_tour = int(np.fix((max(theta) - 2 * np.pi * (max(Position_CTT) - min(Position_Blade)) / 360) / (2 * np.pi)))
    sens = "anhoraire"

    theta_theoretical = Theoretical_AOA(Position_Blade, Position_CTT, nbr_tour, sens)

    EToa_struct, Toa, Toa_noise, Def_struct, Def_struct_noise, Reg_struct, amp_struct, phi_struct, noise = find_Toa_Def_temp(
        theta, theta_theoretical, time, regime, Ra, Position_CTT, EO, f_resonance, xi, Amax, snr
    )

    return Toa, Toa_noise, Def_struct, Def_struct_noise, regime, reg_init, reg_end, EO, Na, nbr_tour, xi, noise

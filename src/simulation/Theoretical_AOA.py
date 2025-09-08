import numpy as np

def Theoretical_AOA(Position_Blade, Position_CTT, nbr_tour, sens):
    # Determine the number of blades and CTT positions
    Na = len(Position_Blade)
    Nct = len(Position_CTT)
    # Preallocate the arrays for theta_theoretical and CT_error_correction with zeros
    theta_theoretical = np.zeros((Na, nbr_tour, Nct))
    # CT_error_correction = np.zeros((Na, nbr_tour, Nct))
    for i in range(1, Na+1):
        for j in range(1, nbr_tour+1):
            for k in range(1, Nct+1):
                if sens == "horaire":
                    if Position_Blade[i-1] <= Position_CTT[k-1]:
                        theta_theoretical[i-1, j-1, k-1] = 2 * np.pi * (j-1) + 2 * np.pi * (Position_CTT[k-1] - Position_Blade[i-1]) / 360
                        #CT_error_correction[i-1, j-1, k-1] = Ra*(1+(1/Na/Nct))*(2*np.pi*(j-1)+2*np.pi*(Position_CTT[k-1]-Position_Blade[i-1])/360)
                    else:
                        theta_theoretical[i-1, j-1, k-1] = 2 * np.pi * j + 2 * np.pi * (Position_CTT[k-1] - Position_Blade[i-1]) / 360
                else:
                    if Position_Blade[i-1] < Position_CTT[k-1]:
                        theta_theoretical[i-1, j-1, k-1] = 2 * np.pi * j + 2 * np.pi * (Position_Blade[i-1] - Position_CTT[k-1]) / 360
                    else:
                        theta_theoretical[i-1, j-1, k-1] = 2 * np.pi * (j-1) + 2 * np.pi * (Position_Blade[i-1] - Position_CTT[k-1]) / 360
    return theta_theoretical

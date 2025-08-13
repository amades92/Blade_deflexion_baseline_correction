import numpy as np

def accel_correc(T_ref_CT, Fr_CT, Toa_struct, correc):
    Fr_struct_CT = np.zeros((Toa_struct.shape[0], Toa_struct.shape[1], Toa_struct.shape[2]))
    
    if correc == 'no':
        for i in range(Toa_struct.shape[0]):
            for k in range(Toa_struct.shape[2]):
                for j in range(1, Toa_struct.shape[1] - 1):
                    if (T_ref_CT[j - 1] <= Toa_struct[i, j, k]) and (Toa_struct[i, j, k] < T_ref_CT[j]):
                        Fr_struct_CT[i, j, k] = Fr_CT[j - 1]
                    elif (T_ref_CT[j] <= Toa_struct[i, j, k]) and (Toa_struct[i, j, k] < T_ref_CT[j + 1]):
                        Fr_struct_CT[i, j, k] = Fr_CT[j]
    
    elif correc == 'yes':
        for i in range(Toa_struct.shape[0]):
            for k in range(Toa_struct.shape[2]):
                for j in range(1, Toa_struct.shape[1] - 1):
                    if (Toa_struct[i, j, k] <= T_ref_CT[j]):
                        Fr_struct_CT[i, j, k] = ((Fr_CT[j] - Fr_CT[j - 1]) * (Toa_struct[i, j, k] - T_ref_CT[j]) / (T_ref_CT[j] - T_ref_CT[j - 1])) + Fr_CT[j]
                    elif (Toa_struct[i, j, k] > T_ref_CT[j]):
                        Fr_struct_CT[i, j, k] = ((Fr_CT[j + 1] - Fr_CT[j]) * (Toa_struct[i, j, k] - T_ref_CT[j]) / (T_ref_CT[j + 1] - T_ref_CT[j])) + Fr_CT[j]
    else:
        print('Choose "yes" or "no" for accel_correc option')
    
    return Fr_struct_CT
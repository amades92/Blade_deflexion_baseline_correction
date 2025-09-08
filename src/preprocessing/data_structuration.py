import numpy as np
 
def data_structuration(data_struct, Na, nbr_tour, Nct):
    data_mat = np.zeros((nbr_tour, Na * Nct))
    for j in range(nbr_tour):
        tmp = []
        for i in range(Na):
            for k in range(Nct):
                tmp.append(data_struct[i, j, k])
        data_mat[j, :] = tmp
    return data_mat
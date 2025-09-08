import numpy as np

def zeroing_function_ct(D, regime, reg_min, reg_max, ordre):
    pos_min = np.zeros(len(reg_min), dtype=int)
    pos_max = np.zeros(len(reg_min), dtype=int)
    for i in range(D.shape[0]):
        for k in range(D.shape[2]):
            for z in range(len(reg_min)):
                pos_min[z] =  (regime[i, :, k] < reg_min[z]).sum() #np.argmax(regime[i, :, k] > reg_min[z]) #if np.any(regime[i, :, k] > reg_min[z]) else 0
                pos_max[z] =  (regime[i, :, k] < reg_max[z]).sum() #np.argmax(regime[i, :, k] < reg_max[z]) #if np.any(regime[i, :, k] < reg_max[z]) else 0
               
            pos = np.column_stack((pos_min, pos_max))
            
            # construction des zones de zeros
            reg = []
            def_ = []
            #print(len(np.arange(pos[z, 0],pos[z, 1]+1,1)))
            for z in range(len(reg_min)):
                reg.extend(regime[i, pos[z, 0]:pos[z, 1]+1, k].flatten())
                def_.extend(D[i, pos[z, 0]:pos[z, 1]+1, k].flatten())
                #print(len(D[i, pos[z, 0]:pos[z, 1]+1, k].flatten()))
            p = np.polyfit(reg, def_, ordre)
            Z = np.polyval(p, regime[i, :, k])
            D[i, :, k] = D[i, :, k] - Z

    return D

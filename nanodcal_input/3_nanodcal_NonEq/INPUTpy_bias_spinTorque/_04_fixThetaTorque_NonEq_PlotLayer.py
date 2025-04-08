import numpy as np # type: ignore
import matplotlib.pyplot as plt # type: ignore

import matplotlib.pyplot as plt # type:ignore
import numpy as np # type:ignore
import os
# ===============
import sys
sys.path.append('/home/tangtang89/Example_Lab/')
from Tools import MKdir   # type: ignore
plt.style.use("/home/tangtang89/presentation.mplstyle")
# ===============

TorqueType = 'Txc'
Voltage    = 0.01

for Theta in [0]:
    
    targetPath = f'Bias_spinTorque_fixTheta_{Theta:>003}'

    MKdir(f'{targetPath}/Bias_Layer', rm=False)
    
    for dir in ['x', 'y', 'z']:
        
        data = np.loadtxt(f'{targetPath}/bias_Layer{TorqueType}_{dir}.txt')
        data = np.transpose(data)
        index_num = np.int64(data[0][1:])
        Bias = np.transpose(data)[0][1:]
        pos  = np.where(Bias==Voltage)
        i_data = data[pos[0][0]+1][1:]
        i_data = i_data*1000 #meV
        print(dir, np.sum(i_data))

        fig = plt.figure(figsize = (8, 6))
        ax  = plt.subplot(111)
        ax.scatter(index_num, i_data)
        ax.set_ylabel(r'Total $T^{}_{}$ (meV)'.format('{xc}', dir), fontsize=14)
        ax.set_xlabel("Atom index", fontsize=14)
        plt.tight_layout()
        plt.savefig(f'{targetPath}/Bias_Layer/bias_Layer{TorqueType}_{dir}.png')
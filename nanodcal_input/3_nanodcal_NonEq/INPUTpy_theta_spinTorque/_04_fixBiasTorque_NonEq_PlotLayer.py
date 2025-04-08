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
angle      = 0

for Voltage in [0]:
    
    targetPath = f'Theta_spinTorque_fixBias_{Voltage:.2f}'

    MKdir(f'{targetPath}/theta_Layer', rm=False)
    
    for dir in ['x', 'y', 'z']:
        
        data = np.loadtxt(f'{targetPath}/theta_Layer{TorqueType}_{dir}.txt')
        data = np.transpose(data)
        index_num = np.int64(data[0][1:])
        theta = np.transpose(data)[0][1:]
        pos = np.where(theta==angle)
        i_data = data[pos[0][0]+1][1:]
        i_data = i_data*1000 #meV
        print(dir, np.sum(i_data))

        fig = plt.figure(figsize = (8, 6))
        ax  = plt.subplot(111)
        ax.scatter(index_num, i_data)
        ax.set_ylabel(r'Total $T^{}_{}$ (meV)'.format('{xc}', dir), fontsize=14)
        ax.set_xlabel("Atom index", fontsize=14)
        plt.tight_layout()
        plt.savefig(f'{targetPath}/theta_Layer/theta_Layer{TorqueType}_{dir}.png')
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
dir = 'z'

for Theta in [0]:
    
    targetPath = f'Bias_spinTorque_fixTheta_{Theta:>003}'

    MKdir(f'{targetPath}/Bias_ALL', rm=False)

    data = np.loadtxt(f'{targetPath}/bias_ALL{TorqueType}.txt')
    data = np.transpose(data)
    Bias = data[0]
    print(Bias)
    
    for dir in ['x', 'y', 'z']:
    
        match dir: #type: ignore
            case 'x':
                i_data = data[1]
            case 'y':
                i_data = data[2]
            case 'z':
                i_data = data[3]
        
        i_data = i_data*1000 # meV

        fig = plt.figure(figsize = (8, 6))
        ax  = plt.subplot(111)
        ax.scatter(Bias, i_data)
        ax.set_ylabel(r'Total $T^{}_{}$ (meV)'.format('{xc}', dir), fontsize=14)
        ax.set_xlabel("Bias", fontsize=14)
        plt.tight_layout()
        plt.savefig(f'{targetPath}/Bias_ALL/Bias_ALL{TorqueType}_{dir}.png')

    fig = plt.figure(figsize = (8, 6))
    ax  = plt.subplot(111)
    for i, i_data in enumerate(data[1:]):
        i_data = i_data*1000 # meV
        if i==0:
            dir = 'x'
        elif i==1:
            dir = 'y'
        elif i==2:
            dir = 'z'
        ax.scatter(Bias, i_data, label=f'{dir}')
    ax.set_title(f"Torque with theta={Theta:>003}")
    ax.set_ylabel(r'Total $T^{xc}$ (meV)', fontsize=14)
    ax.set_xlabel("Bias", fontsize=14)
    ax.legend(loc='best')
    plt.tight_layout()
    plt.savefig(f'{targetPath}/Bias_ALL/Bias_ALL{TorqueType}_alldir.png')


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

for Voltage in [0]:
    
    targetPath = f'Theta_spinTorque_fixBias_{Voltage:.2f}'

    MKdir(f'{targetPath}/theta_ALL', rm=False)

    data = np.loadtxt(f'{targetPath}/theta_ALL{TorqueType}.txt')
    data = np.transpose(data)
    theta = data[0]
    print(theta)
    
    for dir in ['x', 'y', 'z']:
    
        match dir: #type: ignore
            case 'x':
                T_data = data[1]
            case 'y':
                T_data = data[2]
            case 'z':
                T_data = data[3]
        
        T_data = T_data*1000

        fig = plt.figure(figsize = (8, 6))
        ax  = plt.subplot(111)
        ax.scatter(theta, T_data)
        ax.set_ylabel(r'Total $T^{}_{}$ (meV)'.format('{xc}', dir), fontsize=14)
        ax.set_xlabel("Theta", fontsize=14)
        plt.tight_layout()
        plt.savefig(f'{targetPath}/theta_ALL/theta_ALL{TorqueType}_{dir}.png')

    fig = plt.figure(figsize = (8, 6))
    ax  = plt.subplot(111)
    for i, T_data in enumerate(data[1:]):
        if i==0:
            dir = 'x'
        elif i==1:
            dir = 'y'
        elif i==2:
            dir = 'z'

        ax.scatter(theta, T_data*1000, label=f'{dir}')
    ax.set_title(f"Torque with bios={Voltage:.2f}")
    ax.set_ylabel(r'Total $T^{xc}$ (meV)', fontsize=14)
    ax.set_xlabel("Theta", fontsize=14)
    ax.legend(loc='best')
    plt.tight_layout()
    plt.savefig(f'{targetPath}/theta_ALL/theta_ALL{TorqueType}_alldir.png')


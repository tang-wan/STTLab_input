import matplotlib.pyplot as plt # type:ignore
import numpy as np # type:ignore
import os

plt.style.use("/home/tangtang89/presentation.mplstyle")

TorqueType = 'Tso'

if os.path.isdir(f'theta_ALL{TorqueType}'):
    os.system(f'rm -r theta_ALL{TorqueType}')
    os.system(f'mkdir theta_ALL{TorqueType}')
else:
    os.system(f'mkdir theta_ALL{TorqueType}')


data = np.loadtxt(f'./PdTF_theta_ALL{TorqueType}.txt')
data = np.transpose(data)
theta = data[0][1::]
print(theta)

for T_data in data[1::]:

    layer = T_data[0]
    T_data = T_data[1::]*1000
    
    # print(layer)

    fig = plt.figure(figsize = (8, 6))
    ax  = plt.subplot(111)
    ax.set_title(f'Pd{int(layer)}')
    ax.scatter(theta, -T_data)
    ax.set_ylabel(r'Total $-T^{so}$ (meV)', fontsize=14)
    ax.set_xlabel("Theta", fontsize=14)
    # ax.hlines(y=0, xmin=0, xmax=18, colors='gray', zorder=0, linestyles='--')
    # ax.set_xbound(2, 16)
    plt.tight_layout()
    plt.savefig(f'theta_ALL{TorqueType}/PdTF_{layer}_theta_ALL{TorqueType}.png')
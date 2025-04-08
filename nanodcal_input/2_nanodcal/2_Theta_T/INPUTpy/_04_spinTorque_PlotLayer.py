import matplotlib.pyplot as plt # type:ignore
import numpy as np # type:ignore
import os

plt.style.use("/home/tangtang89/presentation.mplstyle")

TorqueType = 'Tso'

if os.path.isdir(f'theta_Layer{TorqueType}'):
    pass
else:
    os.system(f'mkdir theta_Layer{TorqueType}')

# layer = int(input('Which Layer do you want? => ') or "6")
for layer in [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]:
    atom_type  = f'Pd{layer}'
    targetPath = f"{layer}_{atom_type}_spinTorque"

    data = np.loadtxt(f'{targetPath}/PdTF_theta_Layer{TorqueType}.txt')
    # print(data)
    layer = data[0][0]
    angle_array = data[0][1::]
    index_array = data[:,0][1::]
    # print(angle_array)
    # print(index_array)

    specAng = float(input('Which Angle do you want? => ') or "45")
    specAng_index = np.where(angle_array==specAng)[0][0]
    specAng_T = data[:,specAng_index+1][1::]*(-1) # -Tso
    print(specAng_index)
    print(specAng_T)

    fig = plt.figure(figsize = (8, 6))
    ax  = plt.subplot(111)
    ax.set_title(f'Pd{int(layer)}')
    ax.scatter(index_array, specAng_T*1000) # meV
    ax.plot(index_array, specAng_T*1000) # meV
    ax.set_ylabel(r'$-T^{so}$ (meV)', fontsize=14)
    ax.set_xlabel("Pd index", fontsize=14)
    # ax.hlines(y=0, xmin=0, xmax=18, colors='gray', zorder=0, linestyles='--')
    # ax.set_xbound(2, 16)
    ax.grid('--')
    plt.tight_layout()
    plt.savefig(f'theta_Layer{TorqueType}/PdTF_Pd{layer}_theta={specAng}_Layer{TorqueType}.png')
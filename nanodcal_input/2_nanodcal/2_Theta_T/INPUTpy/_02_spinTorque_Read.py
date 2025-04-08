import os
import numpy as np # type: ignore
import matplotlib.pyplot as plt # type: ignore

# for layer in range(3, 15+1, 1):

origin_theta_array = np.array([0, 30, 45, 60, 90])
layer_array = np.array([3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15])

# ================== ALL ================== #
Theta_Txc_array = origin_theta_array
Theta_Tso_array = origin_theta_array
for layer in layer_array:
    
    atom_type  = f'Pd{layer}'
    targetPath = f"{layer}_{atom_type}_spinTorque"

    data = np.loadtxt(f"{targetPath}/AngleALL_SumAllResult.txt", skiprows=2)
    
    # Each Layer
    Tso_array  = np.array([])
    Txc_array  = np.array([])
    for theta_data in data:

        Tso_y  = float(theta_data[4])
        Txc_y  = float(theta_data[1])
        Tso_array = np.append(Tso_array, Tso_y)
        Txc_array = np.append(Txc_array, Txc_y)
    # print(np.shape(Tso_array))
    # print(np.shape(Theta_Tso_array))

    Theta_Txc_array = np.c_[Theta_Txc_array, Txc_array]
    Theta_Tso_array = np.c_[Theta_Tso_array, Tso_array]

label_array = np.insert(layer_array, 0, 0)

Theta_Tso_array = np.c_[label_array, np.transpose(Theta_Tso_array)]
Theta_Tso_array = np.transpose(Theta_Tso_array)
Theta_Txc_array = np.c_[label_array, np.transpose(Theta_Txc_array)]
Theta_Txc_array = np.transpose(Theta_Txc_array)

np.savetxt("PdTF_theta_ALLTso.txt", Theta_Tso_array)
np.savetxt("PdTF_theta_ALLTxc.txt", Theta_Txc_array)

# ================== Layer (Tso) ================== #

for layer in layer_array:

    theta_array = origin_theta_array
    
    atom_type  = f'Pd{layer}'
    targetPath = f"{layer}_{atom_type}_spinTorque"

    data = np.loadtxt(f'{targetPath}/AngleTso_LayerResult.txt', skiprows=2)
    
    atom_Torque = np.linspace(1, layer, layer)
    for theta_data in data:
        atom_Torque = np.c_[atom_Torque, theta_data]

    theta_array = np.insert(theta_array, 0, layer)
    atom_Torque = np.insert(atom_Torque, 0, theta_array).reshape(layer+1, len(theta_array))
    np.savetxt(f"{targetPath}/PdTF_theta_LayerTso.txt", atom_Torque)

# ================== Layer (Txc) ================== #

for layer in layer_array:

    theta_array = origin_theta_array
    
    atom_type  = f'Pd{layer}'
    targetPath = f"{layer}_{atom_type}_spinTorque"

    data = np.loadtxt(f'{targetPath}/AngleTxc_LayerResult.txt', skiprows=2)    
    
    atom_Torque = np.linspace(1, layer, layer)
    for theta_data in data:
        atom_Torque = np.c_[atom_Torque, theta_data]

    theta_array = np.insert(theta_array, 0, layer)
    atom_Torque = np.insert(atom_Torque, 0, theta_array).reshape(layer+1, len(theta_array))
    np.savetxt(f"{targetPath}/PdTF_theta_LayerTxc.txt", atom_Torque)
    
    
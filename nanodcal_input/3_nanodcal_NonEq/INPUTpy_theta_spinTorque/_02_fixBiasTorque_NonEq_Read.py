import os
import numpy as np # type: ignore
import matplotlib.pyplot as plt # type: ignore

origin_theta_array = np.array([0, 45])
startLayer = 24
endLayer   = startLayer+24

# ================== ALL ================== #
Theta_Txc_array = origin_theta_array
Theta_Tso_array = origin_theta_array

for Voltage in [0]:
    
    targetPath = f'Theta_spinTorque_fixBias_{Voltage:.2f}'
    data = np.loadtxt(f"{targetPath}/AngleALL_SumAllResult.txt", skiprows=2)

    # Each Layer
    Tso_x_array, Tso_y_array, Tso_z_array  = np.array([]), np.array([]), np.array([])
    Txc_x_array, Txc_y_array, Txc_z_array  = np.array([]), np.array([]), np.array([])
    for theta_data in data:
        Tso_x, Tso_y, Tso_z  = float(theta_data[3]), float(theta_data[4]), float(theta_data[5])
        Txc_x, Txc_y, Txc_z  = float(theta_data[0]), float(theta_data[1]), float(theta_data[2])
        Tso_x_array = np.append(Tso_x_array, Tso_x)
        Tso_y_array = np.append(Tso_y_array, Tso_y)
        Tso_z_array = np.append(Tso_z_array, Tso_z)
        
        Txc_x_array = np.append(Txc_x_array, Txc_x)
        Txc_y_array = np.append(Txc_y_array, Txc_y)
        Txc_z_array = np.append(Txc_z_array, Txc_z)

    Theta_Txc_array = np.c_[Theta_Txc_array, Txc_x_array, Txc_y_array, Txc_z_array]
    Theta_Tso_array = np.c_[Theta_Tso_array, Tso_x_array, Tso_y_array, Tso_z_array]

    np.savetxt(f"{targetPath}/theta_ALLTso.txt", Theta_Tso_array, header=f'theta, Tso_x, Tso_y, Tso_z')
    np.savetxt(f"{targetPath}/theta_ALLTxc.txt", Theta_Txc_array, header=f'theta, Txc_x, Txc_y, Txc_z')

# ================== Layer (Tso) ================== #
    for dir in ['x', 'y', 'z']:
        data = np.loadtxt(f'{targetPath}/AngleTso_{dir}_LayerResult.txt', skiprows=2)
        theta_array = origin_theta_array
        theta_array = np.insert(origin_theta_array, 0, 0)
        
        atom_Torque = np.linspace(1, len(data[0]), len(data[0]))[startLayer:endLayer]
        for theta_data in data:
            atom_Torque = np.c_[atom_Torque, theta_data[startLayer:endLayer]]

        atom_Torque = np.insert(atom_Torque, 0, theta_array).reshape(len(atom_Torque)+1, 3)
        np.savetxt(f"{targetPath}/theta_LayerTso_{dir}.txt", atom_Torque, header=f'index, theta, {startLayer}:{endLayer}')

# # ================== Layer (Txc) ================== #
    for dir in ['x', 'y', 'z']:
        data = np.loadtxt(f'{targetPath}/AngleTxc_{dir}_LayerResult.txt', skiprows=2)
        
        atom_Torque = np.linspace(1, len(data[0]), len(data[0]))[startLayer:endLayer]
        for theta_data in data:
            atom_Torque = np.c_[atom_Torque, theta_data[startLayer:endLayer]]
        
        atom_Torque = np.insert(atom_Torque, 0, theta_array).reshape(len(atom_Torque)+1, 3)
        np.savetxt(f"{targetPath}/theta_LayerTxc_{dir}.txt", atom_Torque, header=f'index, theta, {startLayer}:{endLayer}')
    
    
import os
import numpy as np # type: ignore
import matplotlib.pyplot as plt # type: ignore

origin_bias_array = np.array([0, 0.01])
startLayer = 24
endLayer   = startLayer+24

# ================== ALL ================== #
bias_Txc_array = origin_bias_array
bias_Tso_array = origin_bias_array

for angle in [0]:
    
    targetPath = f'Bias_spinTorque_fixTheta_{angle:>003}'
    data = np.loadtxt(f"{targetPath}/BiasALL_SumAllResult.txt", skiprows=2)

    # Each Layer
    Tso_x_array, Tso_y_array, Tso_z_array  = np.array([]), np.array([]), np.array([])
    Txc_x_array, Txc_y_array, Txc_z_array  = np.array([]), np.array([]), np.array([])
    for bias_data in data:
        Tso_x, Tso_y, Tso_z  = float(bias_data[3]), float(bias_data[4]), float(bias_data[5])
        Txc_x, Txc_y, Txc_z  = float(bias_data[0]), float(bias_data[1]), float(bias_data[2])
        Tso_x_array = np.append(Tso_x_array, Tso_x)
        Tso_y_array = np.append(Tso_y_array, Tso_y)
        Tso_z_array = np.append(Tso_z_array, Tso_z)
        
        Txc_x_array = np.append(Txc_x_array, Txc_x)
        Txc_y_array = np.append(Txc_y_array, Txc_y)
        Txc_z_array = np.append(Txc_z_array, Txc_z)

    bias_Txc_array = np.c_[bias_Txc_array, Txc_x_array, Txc_y_array, Txc_z_array]
    bias_Tso_array = np.c_[bias_Tso_array, Tso_x_array, Tso_y_array, Tso_z_array]

    np.savetxt(f"{targetPath}/bias_ALLTso.txt", bias_Tso_array, header='bias, Tso_x, Tso_y, Tso_z')
    np.savetxt(f"{targetPath}/bias_ALLTxc.txt", bias_Txc_array, header='bias, Txc_x, Txc_y, Txc_z')

# ================== Layer (Tso) ================== #
    for dir in ['x', 'y', 'z']:
        data = np.loadtxt(f'{targetPath}/BiasTso_{dir}_LayerResult.txt', skiprows=2)
        bias_array = origin_bias_array
        bias_array = np.insert(origin_bias_array, 0, 0)
        
        atom_Torque = np.linspace(1, len(data[0]), len(data[0]))[startLayer:endLayer]
        for bias_data in data:
            atom_Torque = np.c_[atom_Torque, bias_data[startLayer:endLayer]]

        atom_Torque = np.insert(atom_Torque, 0, bias_array).reshape(len(atom_Torque)+1, 3)
        np.savetxt(f"{targetPath}/bias_LayerTso_{dir}.txt", atom_Torque, header=f'index, bias, {startLayer}:{endLayer}')

# # ================== Layer (Txc) ================== #
    for dir in ['x', 'y', 'z']:
        data = np.loadtxt(f'{targetPath}/BiasTxc_{dir}_LayerResult.txt', skiprows=2)

        atom_Torque = np.linspace(1, len(data[0]), len(data[0]))[startLayer:endLayer]
        for bias_data in data:
            atom_Torque = np.c_[atom_Torque, bias_data[startLayer:endLayer]]
        
        atom_Torque = np.insert(atom_Torque, 0, bias_array).reshape(len(atom_Torque)+1, 3)
        np.savetxt(f"{targetPath}/bias_LayerTxc_{dir}.txt", atom_Torque, header=f'index, bias, {startLayer}:{endLayer}')
    
    
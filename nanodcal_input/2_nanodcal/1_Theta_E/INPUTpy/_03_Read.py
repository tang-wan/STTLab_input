import numpy as np #type: ignore
import matplotlib.pyplot as plt #type: ignore
import scipy.io as scio #type: ignore

# layer_list = [int(input("Which layer do you want? => "))]
# theta_list = [int(input("Which Angle do you want? => "))]
# theta_list = [0]

def totalE(atom, layer_list, theta_list):
    print()
    print('~~~~! TotalEnergy OUTPUT START !~~~~')
    print()
    for layer in layer_list:
        atom_type  = f'{atom}{layer}'
        for theta in theta_list:
            targetPath = f'{layer}_{atom_type}_f/{theta:>003}_theta'
            dataFile = f'{targetPath}/analysis/totalEnergy/TotalEnergy.mat'
            data = scio.loadmat(dataFile)['data']

            
            print('TotalEnergy = ', data[0][0]*27.211389)
            
    print()
    print('~~~~! TotalEnergy OUTPUT FINISH !~~~~')
    print()

def Charge(atom, layer_list, theta_list):
    for layer in layer_list:
        atom_type  = f'{atom}{layer}'
        for theta in theta_list:
            targetPath = f'{layer}_{atom_type}_f/{theta:>003}_theta'
            dataFile = f'{targetPath}/analysis/charge/Charge.mat'
            data = scio.loadmat(dataFile)['data'][0][0]

            name_array = [f"{'Index':^18}" +
                          f"{'totalCharge':^18}" +
                          f"{'Polarized_r':^27}" +
                          f"{'Polarized_theta':^9}" +
                          f"{'Polarized_phi':^27}" +
                          f"{'MagneticMoment':^16}"
                        ]
            Index_array = [i for i in range(len(data[6][0]))]

            print()
            print(name_array[0])
            for i in range(len(data[6][0])):
        
                print(f"{Index_array[i]+1:^6} ",
                        f" {np.round(data[0][i][0], 18):.16f} ",
                        f" {np.round(data[1][i][0], 18):.16f} ",
                        f" {np.round(data[2][i][0], 18):.16f} ",
                        f" {np.round(data[3][i][0], 18):.16f} ",
                        f" {np.round(data[4][i][0], 18):.16f} ",
                    )
                with open(f'{targetPath}/analysis/charge/Charge_parse.dat', 'a') as A_File:
                    A_File.writelines([f"{Index_array[i]+1:^6} ",
                                    f" {np.round(data[0][i][0], 16):.16f} ",
                                    f" {np.round(data[1][i][0], 16):.16f} ",
                                    f" {np.round(data[2][i][0], 3):.16f} ",
                                    f" {np.round(data[3][i][0], 3):.16f} ",
                                    f" {np.round(data[4][i][0], 17):.16f}\n"]
                                        )
            print(name_array[0])
            print()
            print('~~~~! Charge OUTPUT FINISH !~~~~')
            print()

# =======================

# totalE(atom='Pd', layer_list=[6], theta_list=[0])
Charge(atom='Pd', layer_list=[6], theta_list=[0])

import numpy as np #type: ignore
import matplotlib.pyplot as plt #type: ignore
import scipy.io as scio #type: ignore
import sys

sys.path.append('/home/tangtang89/Example_Lab/')
from Tools import MKdir, Check_out_Word, Process_Word # type: ignore

def Charge(targetPath):
    
    dataFile = f'{targetPath}/analysis/charge/Charge.mat'
    data = scio.loadmat(dataFile)['data'][0][0]

    name_array = [f"{'Index':7} " +
                    f" {'totalCharge':^18} " +
                    f" {'Polarized_r':^19} " +
                    f" {'Polarized_theta':^21} " +
                    f" {'Polarized_phi':^18} " +
                    f" {'MagneticMoment':^21} "
                ]
    Index_array = [i for i in range(len(data[6][0]))]

    print()
    print(name_array[0])
    with open(f'{targetPath}/analysis/charge/Charge_parse.dat', 'w') as W_File:
        W_File.writelines(f'{name_array[0]}\n')
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

basis_list = [
    '1_nanodcalbasis_DZP',          # 0, LDA
    '2_PBE-Basis-beta_DZP',         # 1, PBE
    '4_neutralatomdatabase_DZP',    # 2, BOTH
    '5_nano_tm_DZP',                # 3, BOTH
    '6_psdojo_TZP',                 # 4, BOTH
    '7_Nano_TM_DZP',                # 5, BOTH
    '8_psdojo_TZP',                 # 6, BOTH (not SOC)
    '8_psdojo_DZP',                 # 7, PBE  (not SOC)
    '8_psdojo_SZP'                  # 8, PBE  (not SOC)
    ]

basis_type = ["PBE", "LDA"]
SOC_list = [True, False]

# basis   = basis_type[1]
# SOC     = SOC_list[0]

atom = 'Pt'
r    = 0.5
for basis in basis_type:
    for SOC in SOC_list:
        if basis == 'PBE':
            run_list = range(1, 6, 1)
        elif basis == 'LDA':
            run_list = [0, 2, 3, 4, 5]

        for i in run_list:
            nd_basis = basis_list[i]
            if SOC:
                targetPath = f"{atom}_bulk_r={r}/{basis.upper()}/{nd_basis}_{basis.upper()}_soc_xz0_mz{r:.1f}"
                print()
                Check_out_Word(f"{nd_basis}_{basis.upper()}_soc_xz0_mz{r:.1f}")
            else:
                targetPath = f"{atom}_bulk_r={r}/{basis.upper()}/{nd_basis}_{basis.upper()}_ncl_xz0_mz{r:.1f}"
                print()
                Check_out_Word(f"{nd_basis}_{basis.upper()}_ncl_xz0_mz{r:.1f}")
            
            Charge(targetPath)
import numpy as np #type: ignore
import matplotlib.pyplot as plt #type: ignore
import scipy.io as scio #type: ignore
import sys

sys.path.append('/home/tangtang89/Example_Lab/')
from Tools import MKdir, Check_out_Word, Process_Word # type: ignore



def Charge(targetPath):
    
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
    print(name_array)
    for i in range(len(data[6][0])):
        
        print(f"{Index_array[i]+1:^18}",
                f"{np.round(data[0][i][0], 16):.18f}",
                f"{np.round(data[1][i][0], 16):.18f}",
                f"{np.round(data[2][i][0], 3):.18f}",
                f"{np.round(data[3][i][0], 3):.18f}",
                f"{np.round(data[4][i][0], 17):.18f}",
            )
    print(name_array)
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

basis   = basis_type[1]
SOC     = SOC_list[0]
atom    = 'Pt'

if basis == 'PBE':
    run_list = range(1, 6, 1)
elif basis == 'LDA':
    run_list = [0, 2, 3, 4, 5]

for i in run_list:
    nd_basis = basis_list[i]
    if SOC:
        targetPath = f"{atom}_bulk_r=0/{basis.upper()}/{nd_basis}_{basis.upper()}_soc_xz0_mz0.0"
        print()
        Check_out_Word(f"{nd_basis}_{basis.upper()}_soc_xz0_mz0.0")
    else:
        targetPath = f"{atom}_bulk_r=0/{basis.upper()}/{nd_basis}_{basis.upper()}_ncl_xz0_mz0.0"
        print()
        Check_out_Word(f"{nd_basis}_{basis.upper()}_ncl_xz0_mz0.0")
    
    Charge(targetPath)
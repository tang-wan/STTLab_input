import numpy as np # type: ignore
import os
import re
#----------------------------------------
import sys
sys.path.append('/home/tangtang89/Example_Lab/nanodcal_input/2_nanodcal/1_Theta_E/')
sys.path.append('/home/tangtang89/Example_Lab/')
import nd_analysis as nda # type: ignore
from Tools import MKdir, Check_out_Word, Process_Word # type: ignore
# =========================
# =========================
MKdir('OUTFILE', rm=True)
# ==========
## Setting
# run      = False
run      = True
# ==========
ana_list = [('charge', 'i5x', '1'),
            ('totalEnergy', 'i5x', '1'),
            ('spinTorque', 'dl2x', '56'),
            ('band', 'i91', '18')
            ]
ana = -1
ana_type = ana_list[ana][0]

grid_num = (64, 64, 6) # Only necessary for Spintorque

matPath = "../../NanodcalObject.mat"
# ==========
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
SOC     = SOC_list[1]
atom    = 'Pt'


if basis == 'PBE':
    # run_list = range(1, 6, 1)
    run_list = [3]
elif basis == 'LDA':
    # run_list = [0, 2, 3, 4, 5]
    run_list = [3]
# ==========

for i in run_list:
    nd_basis = basis_list[i]
    print(nd_basis)
    # if SOC:
    #     targetPath = f"{atom}_bulk/{basis.upper()}/{nd_basis}_{basis.upper()}_soc_xz0_mz0.5"
    # else:
    #     targetPath = f"{atom}_bulk/{basis.upper()}/{nd_basis}_{basis.upper()}_ncl_xz0_mz0.5"
    if SOC:
        targetPath = f"{atom}_bulk_r=0/{basis.upper()}/{nd_basis}_{basis.upper()}_soc_xz0_mz0.0"
    else:
        targetPath = f"{atom}_bulk_r=0/{basis.upper()}/{nd_basis}_{basis.upper()}_ncl_xz0_mz0.0"
    print()
    Check_out_Word('analysis file')
    if not(os.path.isdir(f'{targetPath}/analysis')):
        os.system(f'mkdir {targetPath}/analysis')
        Process_Word(f"Making {targetPath}/analysis")
    else:
        Process_Word(f"{targetPath}/analysis is exist")
    print()
    Check_out_Word(f'{ana_type} file')
    if not(os.path.isdir(f'{targetPath}/analysis/{ana_type}')):
        os.system(f'mkdir {targetPath}/analysis/{ana_type}')
        Process_Word(f"Making {targetPath}/analysis/{ana_type}")
    else:
        Process_Word(f"{targetPath}/analysis/{ana_type} is exist. Removing...")
        os.system(f'rm -r {targetPath}/analysis/{ana_type}')
        os.system(f'mkdir {targetPath}/analysis/{ana_type}')
        Process_Word(f"Making {targetPath}/analysis/{ana_type}")

    BasisTest = nda.Nd_analysis(matPath=matPath)
    # main.input / main.py
    BasisTest.main(analysis_type = ana_type,
                    grid_num=grid_num,
                    symmetryKPoints="D",
                    Coor_symmetryKPoints="D"
                    )
    
    # nanodcal.pbs
    if SOC:
        name = f"{atom}_{nd_basis[:-4:]}_soc_basisTest_{ana_type}"
    else:
        name = f"{atom}_{nd_basis[:-4:]}_ncl_basisTest_{ana_type}"

    mechine = ana_list[ana][1]
    ppn = ana_list[ana][2]
    BasisTest.ndpbs(
                    name = name,
                    mechine = mechine,
                    ppn = ppn
                    )

# ========================================================
    os.system(f'mv OUTFILE/* {targetPath}/analysis/{ana_type}')
    #----------------------
    os.chdir(f"{targetPath}/analysis/{ana_type}")
    print()
    os.system('pwd')
    Check_out_Word(f"{nd_basis} with SOC is {SOC}, analysising {ana_type}")
    #----------------------
    if (run == True):
        os.system('qsub nanodcal.pbs')
    else:
        pass
    #----------------------
    os.chdir('../../../../../')
    os.system('pwd')
    print("# ====================")
    print()
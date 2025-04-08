import numpy as np # type: ignore
import os
import re
#----------------------------------------
import sys
sys.path.append('/home/tangtang89/Example_Lab/nanodcal_input/2_nanodcal/1_Theta_E/')
import nd_analysis as nda # type: ignore
# ========================================================
# ========================================================
sys.path.append('/home/tangtang89/Example_Lab/')
from Tools import MKdir, Check_out_Word, Process_Word # type: ignore
# ========================================================
MKdir('OUTFILE', rm=True)

## Setting
# run = False
run = True

ana_list = [('charge', 'dl2x', '2'),
            ('totalEnergy', 'i5x', '1'),
            ('spinTorque', 'i91', '16'),
            ('band', 'i91', '18')]
ana = -2
Co_list = [
    3, 4, 5, 6, 7, 8, 9, 10, 11, 12
    ]

ana_type = ana_list[ana][0]

grid_num             = (100, 100, 1) # Only necessary for Spintorque
symmetryKPoints      = "{'G','M','K','G'}", # Only for Band
Coor_symmetryKPoints = "[0 0 0; 1/2 1/2 0; 1/3 1/3 2/3; 0 0 0]" # Only for Band

if (ana_type == "spinTorque"):
    CoPd_nanod = nda.Nd_analysis(matPath = "\'../../1run/NanodcalStructObject.mat\'")
else:
    CoPd_nanod = nda.Nd_analysis(matPath = "../../1run/NanodcalObject.mat")

for layer in Co_list:
    atom_type  = f'Pd{layer}'
    for theta in [
                0
                ]:
        target_Path = f'{layer}_{atom_type}_f/{theta:>003}_theta'
        if not(os.path.isdir(f'{target_Path}/analysis')):
            os.system(f'mkdir {target_Path}/analysis')
            print(f"Making {target_Path}/analysis")
        else:
            print(f"{target_Path}/analysis is exist")

        if not(os.path.isdir(f'{target_Path}/analysis/{ana_type}')):
            os.system(f'mkdir {target_Path}/analysis/{ana_type}')
            print(f"Making {target_Path}/analysis/{ana_type}")
        else:
            print(f"{target_Path}/analysis/{ana_type} is exist")
            os.system(f'rm -r {target_Path}/analysis/{ana_type}')
            os.system(f'mkdir {target_Path}/analysis/{ana_type}')
            print(f"Making {target_Path}/analysis/{ana_type}")

        # main.input / main.py
        CoPd_nanod.main(analysis_type = ana_type,
                    grid_num=grid_num,
                    symmetryKPoints=symmetryKPoints,
                    Coor_symmetryKPoints=Coor_symmetryKPoints
                    )
        
        # nanodcal.pbs
        name = f"{atom_type}_TF_{theta:>003}_scf_HIGH_{ana_type}"
        mechine = ana_list[ana][1]
        ppn = ana_list[ana][2]
        CoPd_nanod.ndpbs(
                    name = name,
                    mechine = mechine,
                    ppn = ppn
                    )

# ========================================================
# ========================================================
        os.chdir(f"{target_Path}/1run/")
        
        if (ana_type == "spinTorque"):
            if not(os.path.isfile("NanodcalStructObject.mat")):
                os.system("ndconvert NanodcalObject.mat .")
            else:
                print("NanodcalStructObject.mat is exist")
        else:
            pass

        os.chdir("../../../")
# ========================================================
        os.system(f'mv OUTFILE/* {target_Path}/analysis/{ana_type}')
        #----------------------
        os.chdir(f"{target_Path}/analysis/{ana_type}")
        print()
        os.system('pwd')
        print(f"{atom_type} at {theta:>003}, analysising {ana_type}")
        #----------------------
        if (run == True):
            if ana_type == 'spinTorque':
                os.system('qsub junpy.pbs')
            else:
                os.system('qsub nanodcal.pbs')
        else:
            pass
        #----------------------
        os.chdir('../../../../')
        os.system('pwd')
        print("# ====================")
        print()
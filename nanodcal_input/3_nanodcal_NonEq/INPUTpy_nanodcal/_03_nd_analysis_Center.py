import numpy as np # type: ignore
import os
import re
#----------------------------------------
import sys
sys.path.append('/home/tangtang89/Example_Lab/nanodcal_input/3_nanodcal_NonEq/')
import nd_NonEq_analysis as nda # type: ignore
# ========================================================
# ========================================================
sys.path.append('/home/tangtang89/Example_Lab/')
from Tools import MKdir, Check_out_Word, Process_Word # type: ignore
# ========================================================
MKdir('OUTFILE', rm=True)

## Setting
# run = False
run = True

# repeatType, layerNum = ('u4x', 24)
# repeatGroup, LeadrepeatType, LeadlayerNum = ('Hex', 'u2x', 12)

repeatType, layerNum = ('u4y', 24)
repeatGroup, LeadrepeatType, LeadlayerNum = ('Tex', 'u2y', 12)

# =====

ana_list = [('charge', 'i5x', '2'),
            ('totalEnergy', 'i5x', '1'),
            ('spinTorque', 'dl2x', '56'),
            ('current', 'dl2x', '56')]
# ana = 0
# ana = -2
ana = -1
# =====
ana_type = ana_list[ana][0]

# grid_num = (1, 180, 1) # Hex
grid_num = (170, 1, 1) # Tex
BiasWin  = 1e-3

if (ana_type=="spinTorque" or ana_type=="current"):
    CoPd_nanod = nda.Nd_analysis(matPath = "\'../../1run/NanodcalStructObject.mat\'")
else:
    CoPd_nanod = nda.Nd_analysis(matPath = "../../1run/NanodcalObject.mat")
# =====
layer = layerNum
for Voltage in [0.02, 0.03, 0.04]:
    atom_type  = f'Co{layer}'
    for theta in [
                0
                ]:
        target_Path = f"{repeatGroup}_Center_{repeatType}/{theta:>003}_theta/vb{Voltage:.2f}"
        MKdir(f'{target_Path}/analysis', rm=False)
        MKdir(f'{target_Path}/analysis/{ana_type}', rm=True)


        # main.input / main.py
        CoPd_nanod.main(analysis_type = ana_type,
                        BiasWin       = BiasWin,
                        grid_num      = grid_num
                        )
        
        # nanodcal.pbs
        name = f"{atom_type}TF_{theta:>003}_{repeatGroup}_{repeatType}_{Voltage}_{ana_type}"
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
        
        if (ana_type == "spinTorque" or ana_type=='current'):
            if not(os.path.isfile("NanodcalStructObject.mat")):
                os.system("ndconvert NanodcalObject.mat .")
            else:
                print("NanodcalStructObject.mat is exist")
        else:
            pass

        os.chdir('../../../../')
# ========================================================
        os.system(f'mv OUTFILE/* {target_Path}/analysis/{ana_type}')
        #----------------------
        os.chdir(f"{target_Path}/analysis/{ana_type}")
        print()
        os.system('pwd')
        print(f"{atom_type} at {theta:>003}, analysising {ana_type}")
        #----------------------
        if (run == True):
            if ana_type=='spinTorque' or ana_type=='current':
                os.system('qsub junpy.pbs')
            else:
                os.system('qsub nanodcal.pbs')
        else:
            pass
        #----------------------
        os.chdir('../../../../../')
        os.system('pwd')
        print("# ====================")
        print()
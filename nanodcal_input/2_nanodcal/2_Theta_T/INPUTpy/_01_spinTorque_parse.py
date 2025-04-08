import numpy as np # type: ignore
import os
import re
#----------------------------------------
import sys
sys.path.append('/home/tangtang89/Example_Lab/nanodcal_input/2_nanodcal/2_Theta_T/')
sys.path.append('/home/tangtang89/Example_Lab/')
import jp_analysis as jpa # type: ignore
from Tools import MKdir
# ========================================================
# ========================================================

## Setting
run = False
# run = True

atom_index = 0
for layer in [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]:
    atom_type  = f'Pd{layer}'
    pickle_path = []
    # -----
    MKdir("parse_spinTorque", rm=True)
    # -----
    for theta in [0, 30, 45, 60, 90]:
        pickle_path.append(f'../../1_Theta_E/{layer}_{atom_type}_f/{theta:>003}_theta/analysis/spinTorque/bulk_spin_torque.pickle\n')
        CoPd_T = jpa.jp_analysis(pickle_path = pickle_path)
        CoPd_T.Writting_parseFile()
    CoPd_T.Making_parsingFile()
    CoPd_T.parsesh()   

    os.chdir('parse_spinTorque')
    os.system('pwd')
    
    if (run == True):
        os.system('./parse.sh SOC_zx_R.txt [:,:,4]')
        os.chdir('../')
        os.system('mv Result_output_Slices.txt AngleTso_LayerResult.txt')
        
        os.chdir('parse_spinTorque')
        os.system('./parse.sh SOC_zx_R.txt [:,:,1]')
        os.chdir('../')
        os.system('mv Result_output_Slices.txt AngleTxc_LayerResult.txt')
        os.system('mv Result_output_SumAll.txt AngleALL_SumAllResult.txt')

    else:
        os.chdir('../')

    MKdir(f'{layer}_{atom_type}_spinTorque', rm=True)
    os.system(f'mv parse_spinTorque *.txt {layer}_{atom_type}_spinTorque')
    # os.system(f'mv parse_spinTorque AngleTxc_LayerResult.txt AngleTso_LayerResult.txt AngleALL_SumAllResult.txt {layer}_{atom_type}_spinTorque')
import numpy as np # type: ignore
import os
import re
#----------------------------------------
import sys
sys.path.append('/home/tangtang89/Example_Lab/nanodcal_input/3_nanodcal_NonEq/')
sys.path.append('/home/tangtang89/Example_Lab/')
import jp_NonEq_analysis as jpa # type: ignore
from Tools import MKdir   # type: ignore
# ========================================================
# ========================================================

## Setting
# run = False
run = True

repeatType, layerNum = ('u4y', 24)
repeatGroup, LeadrepeatType, LeadlayerNum = ('Tex', 'u2y', 12)

startLayer = 24
endLayer   = startLayer+24

for Voltage in [0.00]:
    pickle_path = []
    # -----
    MKdir("parse_spinTorque", rm=True)
    # -----
    for theta in [0, 45]:
        pickle_path.append(f'../../{theta:>003}_theta/vb{Voltage:.2f}/analysis/spinTorque/spin_torque.pickle\n')
        CoPd_T = jpa.jp_analysis(pickle_path = pickle_path)
        CoPd_T.Writting_parseFile()
    CoPd_T.Making_parsingFile()
    CoPd_T.parsesh()   

    os.chdir('parse_spinTorque')
    os.system('pwd')
    
    if (run == True):
        os.system(f'./parse.sh SOC_zx_R.txt [:,:,0]')
        os.chdir('../')
        os.system('mv Result_output_Slices.txt AngleTxc_x_LayerResult.txt')
        # -----
        os.chdir('parse_spinTorque')
        os.system('./parse.sh SOC_zx_R.txt [:,:,1]')
        os.chdir('../')
        os.system('mv Result_output_Slices.txt AngleTxc_y_LayerResult.txt')
        # -----
        os.chdir('parse_spinTorque')
        os.system('./parse.sh SOC_zx_R.txt [:,:,2]')
        os.chdir('../')
        os.system('mv Result_output_Slices.txt AngleTxc_z_LayerResult.txt')
        # ==========
        os.chdir('parse_spinTorque')
        os.system('./parse.sh SOC_zx_R.txt [:,:,3]')
        os.chdir('../')
        os.system('mv Result_output_Slices.txt AngleTso_x_LayerResult.txt')
        # -----
        os.chdir('parse_spinTorque')
        os.system('./parse.sh SOC_zx_R.txt [:,:,4]')
        os.chdir('../')
        os.system('mv Result_output_Slices.txt AngleTso_y_LayerResult.txt')
        # -----
        os.chdir('parse_spinTorque')
        os.system('./parse.sh SOC_zx_R.txt [:,:,5]')
        os.chdir('../')
        os.system('mv Result_output_Slices.txt AngleTso_z_LayerResult.txt')
        # ==========
        os.chdir('parse_spinTorque')
        os.system(f'./parse.sh SOC_zx_R.txt [:,{startLayer}:{endLayer},:]')
        os.chdir('../')
        os.system('rm Result_output_Slices.txt')
        os.system('mv Result_output_SumAll.txt AngleALL_SumAllResult.txt')

    else:
        os.chdir('../')

    MKdir(f'Theta_spinTorque_fixBias_{Voltage:.2f}', rm=True)
    os.system(f'mv parse_spinTorque *.txt Theta_spinTorque_fixBias_{Voltage:.2f}')
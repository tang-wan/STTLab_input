import numpy as np # type: ignore
import os
import re
#----------------------------------------
import sys
sys.path.append('/home/tangtang89/Example_Lab/nanodcal_input/3_nanodcal_NonEq/')
sys.path.append('/home/tangtang89/Example_Lab/')
import jp_NonEq_analysis_current as jpa # type: ignore
from Tools import MKdir   # type: ignore
# ========================================================
# ========================================================

## Setting
# run = False
run = True

for theta in [0]:

    pickle_path = []
    # -----
    MKdir("parse_current", rm=True)
    # -----
    for Voltage in [0.01, 0.02, 0.03, 0.04, 0.05]:
        pickle_path.append(f'../../{theta:>003}_theta/vb{Voltage:.2f}/analysis/current/current.pickle\n')
        CoPd_T = jpa.jp_analysis(pickle_path = pickle_path)
        CoPd_T.Writting_parseFile()
    CoPd_T.Making_parsingFile()
    CoPd_T.parsesh()   

    os.chdir('parse_current')
    os.system('pwd')
    
    if (run == True):
        os.system(f'./parse.sh Current_pickle.txt')
        os.chdir('../')

    else:
        os.chdir('../')

    MKdir(f'Bias_current_fixTheta_{theta:>003}', rm=True)
    os.system(f'mv parse_current *.txt Bias_current_fixTheta_{theta:>003}')
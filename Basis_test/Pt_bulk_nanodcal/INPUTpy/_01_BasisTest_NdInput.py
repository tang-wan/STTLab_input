import numpy as np # type: ignore
import os
import re
#----------------------------------------
import sys
sys.path.append('/home/tangtang89/Example_Lab/Basis_test/')
import Basis_nd_input as ndi # type: ignore
# ========================================================
# ========================================================

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
# ----------
# run      = False
run      = True
# ----------
atom     = 'Pt'

# basis    = 'PBE'
basis    = 'LDA'

SOC      = False
# SOC      = True

if basis == 'PBE':
    run_list = [1, 2, 3, 4, 5]
elif basis == 'LDA':
    run_list = [0, 2, 3, 4, 5]

for i in run_list:
    nd_basis = basis_list[i]
    print(nd_basis)

    spec_atom = ndi.Nd_Basis_Test(
                            nd_basis   = nd_basis,
                            basis_type = basis,
                            atom_type  = atom,
                            SOC        = SOC
                            )
    spec_atom.Read_info(
            # printTrue=False
            )
    spec_atom.atoms_xyz(r=0.5, theta=0, phi=0, 
                type='Cart'
                )
    spec_atom.BASIS()
    spec_atom.scf_input(
                        spinType='GeneralSpin',
                        mixing_rate=0.01, step=200, 
                        precision='High'
                        )
    
    mechine = "dl0x"
    ppn = "16"
    spec_atom.ndpbs(
                    mechine = mechine,
                    ppn = ppn
                    )
    if run:
        spec_atom.QSUB()
    else:
        pass

import numpy as np # type: ignore
import os
import re
#----------------------------------------
import sys
sys.path.append('/home/tangtang89/Example_Lab/Basis_test/')
import Basis_vp_input as vpi # type: ignore
sys.path.append('/home/tangtang89/Example_Lab/')
from Tools import MKdir, Check_out_Word, Process_Word # type: ignore

# ========================================================

basis    = 'LDA'
atom     = 'Pt'
# SOC      = False
SOC      = True

spec_atom = vpi.Vp_Basis_Test(
                        basis_type = basis,
                        atom_type  = atom,
                        SOC        = SOC
                        )
spec_atom.Read_info(
            # printTrue=False
            )
spec_atom.POSCAR(r=0.0, theta=0, phi=0, 
                type='Frac')
spec_atom.POTCAR()
spec_atom.KPOINTS()
spec_atom.INCAR(KPAR=2, NPAR=9, moment=0.0, moment_list=[0, 0])
spec_atom.vasppbs(mechine='i91', ppn=18)
spec_atom.QSUB()
import numpy as np # type:ignore
import os
import re
#----------------------------------------
import sys
sys.path.append('/home/tangtang89/Example_Lab/vasp_input/')
import vp_CAR as cr # type:ignore
import vp_Vasp as vp # type:ignore
import vp_KPOINT as kp # type:ignore

sys.path.append('/home/tangtang89/Example_Lab/')
from Tools import MKdir, Check_out_Word, Process_Word # type: ignore
# ========================================================
MKdir('OUTFILE', rm=True)
#----------------------------------------
init_layer  = 1
total_layer = 1
sep_layer   = total_layer - init_layer + 1
# sep_layer   = 4
layer_array = np.linspace(init_layer, 
                          total_layer, 
                          sep_layer
                          )
#----------------------------------------
## INCAR
KPAR       =  3
NPAR       =  6
moment     = [0.5, 0.5]
#----------------------------------------
for layer_num in layer_array:
    ## POSCAR
    atom_type = f'Pt{int(layer_num)}Te2'
    LC_1st = 1.0       # From Pd6 ThinFilm relax
    LC_2nd = 1.0       # From Pd6 ThinFilm relax

    Dv = 15 # Bilayer
#----------------------------------------
    ## vasp
    name = f"{atom_type}_B_relax1"
    mechine = "i91"
    ppn = "18"

    ## Setting
    run = False
    # run = True

# ========================================================    
# ========================================================
    Struc = cr.AUTOsub(atom_type, (LC_1st, LC_2nd), Dv)
    # Struc.POTCAR(PT_type='PBE', where='STT')
    Struc.POTCAR(PT_type='LDA', where='STT')
    Struc.INCAR(
            KPAR      =  KPAR,
            NPAR      =  NPAR,
            vasp_type = 'relax',
            # relax, relax2, scf

            moment    =  moment,
            moment_list1 = (0, 0),
            moment_list2 = (0, 0),
            # (theta, phi)

            SOC       =  'cl',
            Lattice   =  True,

            constrain_list=(False, 1, 0) ,
            # (constrain or not, direction (1) or both (2), constrain strength [lambda])
            vdw_gap = True
        )
    # KPOINTS
    kp.KPOINT(grid=(15, 15, 9))   
    # .pbs
    vp.vasppbs(
            name = name,
            mechine = mechine,
            ppn = ppn,
            type='std' # available: vasp_gam | vasp_ncl | vasp_std
        )
    # POSCAR
    os.system(f"cp POSCAR OUTFILE/POSCAR")
#----------------------
    file_name = f"{int(layer_num)}_{atom_type}_f"
    MKdir(f"{file_name}", rm=True)
#----------------------
    os.system(f"cp OUTFILE/* {file_name}/.")
    os.system(f"cp ~/vdw_kernel.bindat {file_name}/.")
#----------------------
    os.chdir(f"{file_name}/")
    print()
    os.system('pwd')
    print(f"{atom_type}")
#----------------------
    if (run == True):
        os.system('qsub vasp6.pbs')
        # os.system('sbatch vasp6.sh')
    else:
        pass
#----------------------
    os.chdir('../')
    os.system('pwd')

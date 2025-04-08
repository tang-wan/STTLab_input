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
init_layer  = 6
total_layer = 15
sep_layer   = total_layer - init_layer + 1
# sep_layer   = 4
layer_array = np.linspace(init_layer, 
                          total_layer, 
                          sep_layer
                          )
#----------------------------------------
## INCAR
KPAR       =  7
NPAR       =  8
moment     = [0.5]

vasp_type = 'relax'
# relax, relax2, scf, band

SOCType, SOCnum = "cl", 1
# SOCType, SOCnum = "ncl", 2
# SOCType, SOCnum = "soc", 3
#----------------------------------------
for layer_num in layer_array:
    ## POSCAR
    atom_type = f'Pd{layer_num:.0f}'
    LC_1st = 2.753230221       # From Pd6 ThinFilm relax

    Dv = 15 # Bilayer
#----------------------------------------
    ## vasp
    name = f"{atom_type}_TF_relax1"
    mechine = "ct56"
    ppn = "56"

    ## Setting
    run = False
    # run = True

# ========================================================    
# ========================================================
    Struc = cr.AUTOsub(atom_type, (LC_1st,), Dv)
    
    # POSCAR
    Struc.PureThinfilm(stacking="FCC(111)", 
                       LattCon_Coef_list=(LC_1st,), 
                       Dv=Dv)
    
    # POTCAR
    Struc.POTCAR(PT_type='PBE', where='STT')
    
    # INCAR
    Struc.INCAR(
            KPAR      =  KPAR,
            NPAR      =  NPAR,
            vasp_type = vasp_type,

            moment    =  moment,
            moment_list1 = (0, 0),
            # (theta, phi)

            SOC       =  SOCType,
            Lattice   =  True,

            constrain_list=(False, 1, 0) ,
            # (constrain or not, direction (1) or both (2), constrain strength [lambda])

            vdw_gap   = False
        )
    
    # KPOINTS
    kp.KPOINT(vasp_type=vasp_type, grid=(24, 24, 1))   
    
    # .pbs
    if SOCType == "cl":
        pbs_type = 'std'
    else:
        pbs_type = 'ncl'
    vp.vasppbs(
            name = name,
            mechine = mechine,
            ppn  = ppn,
            type = pbs_type # available: vasp_gam | vasp_ncl | vasp_std
        )
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

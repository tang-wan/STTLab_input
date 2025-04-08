import numpy as np # type: ignore
import os
import re
#----------------------------------------
import sys
sys.path.append('/home/tangtang89/Example_Lab/vasp_input/')
import vp_CAR as cr # type:ignore
import vp_Vasp as vp # type:ignore
import vp_KPOINT as kp # type:ignore
# ========================================================
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
    name = f"{atom_type}_B_relax2"
    mechine = "i91"
    ppn = "18"

    ## Setting
    run = False
    # run = True

# ========================================================    
# ========================================================
    file_name = f"{int(layer_num)}_{atom_type}_f"
    MKdir(file_name, rm=True)
    
    # POTCAR
    os.system(f"cp ../1_relax/{file_name}/POTCAR {file_name}/.")
    # KPOINTS
    os.system(f"cp ../1_relax/{file_name}/KPOINTS {file_name}/.")
    
    os.system(f"cp ../1_relax/{file_name}/vdw_kernel.bindat {file_name}/.")
    # POSCAR
    os.system(f'cp ../1_relax/{file_name}/CONTCAR {file_name}/POSCAR')
    # CHGCAR
    os.system(f'cp ../1_relax/{file_name}/CHGCAR {file_name}/.')
    
    # INCAR & vasp6.pbs
    Struc = cr.AUTOsub(atom_type, (LC_1st, LC_2nd), Dv)
    Struc.INCAR(
            KPAR      =  KPAR,
            NPAR      =  NPAR,
            vasp_type = 'relax2',
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

    # .pbs
    vp.vasppbs(
            name = name,
            mechine = mechine,
            ppn = ppn,
            type='std' # available: vasp_gam | vasp_ncl | vasp_std
        )
    
    os.system(f"cp OUTFILE/* {file_name}/.") # INCAR & vasp6.pbs
#----------------------
    print()
    os.chdir(f"{file_name}")
    os.system('pwd')
    print(f"layer number = {atom_type}")
#----------------------
    if (run == True):
        os.system('qsub vasp6.pbs')
        # os.system('sbatch vasp6.sh')
    else:
        pass
#----------------------
    os.chdir('../')
    os.system('pwd')

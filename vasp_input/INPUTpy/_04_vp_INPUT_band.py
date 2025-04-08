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
## Setting
run = False
# run = True

## INCAR
KPAR    =  3
NPAR    =  6
moment  = [0.5, 0.5]

vasp_type = 'band'
# relax, relax2, scf, band

SOCType, SOCnum = "cl", 1
# SOCType, SOCnum = "ncl", 2
# SOCType, SOCnum = "soc", 3
#----------------------------------------
for layer_num in layer_array:
    ## POSCAR
    atom_type = f'Pt1Te2'*int(layer_num)

#----------------------------------------
    ## vasp
    name = f"Pt{int(layer_num)}Te{int{layer_num*2}_TF_{SOCType}_band"
    mechine = "i91"
    ppn = "18"

# ========================================================    
# ========================================================
    file_name = f"{int(layer_num)}_{atom_type}_f"
    targetPath = f"{file_name}/{SOCnum}_{SOCType}_band"
    MKdir(file_name, rm=False)

    if os.path.isfile(f'{targetPath}/KPATH.in'):
        MKdir(targetPath, rm=False)
    else:
        MKdir(targetPath, rm=True)
    
    # POTCAR
    os.system(f"cp ../3_scf/{file_name}/{SOCnum}_{SOCType}/POTCAR {targetPath}/.")
    # POSCAR
    os.system(f'cp ../3_scf/{file_name}/{SOCnum}_{SOCType}/CONTCAR {targetPath}/POSCAR')
    
    # KPOINTS
    kp.KPOINT(vasp_type=vasp_type, grid=None, target_Path=targetPath)
    # os.system(f"cp ~/Example_Lab/vasp_input/INPUTpy/60_KPOINTS {targetPath}/KPOINTS")
    
    # CHGCAR
    os.system(f'cp ../3_scf/{file_name}/{SOCnum}_{SOCType}/CHGCAR {targetPath}/.')

    # INCAR & vasp6.pbs
    os.system(f"cp ../3_scf/{file_name}/{SOCnum}_{SOCType}/vdw_kernel.bindat {targetPath}/.")
    Struc = cr.AUTOsub(atom_type)
    Struc.INCAR(
            KPAR      = KPAR,
            NPAR      = NPAR,
            vasp_type = vasp_type,

            moment      =  moment,
            moment_list = ((0, 0), (0, 0))*int(layer_num),
            # (theta, phi)

            SOC       =  SOCType,
            Lattice   =  True,

            constrain_list=(False, 1, 0) ,
            # (constrain or not, direction (1) or both (2), constrain strength [lambda])            ,

            vdw_gap   = False
        )

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
    
    os.system(f"cp OUTFILE/* {targetPath}/.") # INCAR & vasp6.pbs

#----------------------
    print()
    os.chdir(f"{targetPath}")
    os.system('pwd')
    print(f"layer number = Pt{int(layer_num)}Te{int{layer_num*2}")
#----------------------
    if (run == True):
        os.system('qsub vasp6.pbs')
        # os.system('sbatch vasp6.sh')
    else:
        pass
#----------------------
    os.chdir('../../')
    os.system('pwd')

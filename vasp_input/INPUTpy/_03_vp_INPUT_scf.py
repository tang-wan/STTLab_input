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
total_layer = 6
sep_layer   = total_layer - init_layer + 1
layer_array = np.linspace(init_layer, 
                          total_layer, 
                          sep_layer
                          )
#----------------------------------------
## Setting
run = False
# run = True

## INCAR   
KPAR      =  4
NPAR      =  5
moment    = [0.5, 0.5]

basis     = 'PBE'
vasp_type = 'scf'
# relax, relax2, scf, band

# SOCType, SOCnum = "cl", 1
# SOCType, SOCnum = "ncl", 2
SOCType, SOCnum = "soc", 3
#----------------------------------------
for layer_num in layer_array:
    ## POSCAR
    atom_type = f'Pt1Te2'*int(layer_num)

#----------------------------------------
    ## vasp
    name = f"Pt{int(layer_num)}Te{2*int(layer_num)}_TF_{basis}_{SOCType}"
    mechine = "dl0x"
    ppn = "20"

# ========================================================    
# ========================================================
    file_name = f"{int(layer_num)}_Pt{int(layer_num)}Te{2*int(layer_num)}_f"
    targetPath = f"{file_name}/{SOCnum}_{SOCType}"
    
    MKdir(file_name, rm=False)
    if os.path.isfile(f'{targetPath}/KPATH.in'):
        MKdir(targetPath, rm=False)
    else:
        MKdir(targetPath, rm=True)
    
    # POTCAR
    os.system(f"cp ../2_relax2/{file_name}/POTCAR {targetPath}/.")
    
    # KPOINTS
    os.system(f"cp ../2_relax2/{file_name}/KPOINTS {targetPath}/.")
    
    os.system(f"cp ../2_relax2/{file_name}/vdw_kernel.bindat {targetPath}/.")
    # POSCAR
    os.system(f'cp ../2_relax2/{file_name}/CONTCAR {targetPath}/POSCAR')
    # CHGCAR
    os.system(f'cp ../2_relax2/{file_name}/CHGCAR {targetPath}/.')
    
    # INCAR & vasp6.pbs
    Struc = cr.AUTOsub(atom_type)
    Struc.INCAR(
            KPAR      =  KPAR,
            NPAR      =  NPAR,
            vasp_type = vasp_type,

            moment      =  moment*int(layer_num),
            moment_list = ((0, 0), (0, 0))*int(layer_num),
            # (theta, phi)

            SOC       =  SOCType,
            Lattice   =  True,
            band_num  =  100,

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
    print("==================================")
    print("==================================")

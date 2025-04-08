import numpy as np # type: ignore
import os
import re
#----------------------------------------
import sys
sys.path.append('/home/tangtang89/Example_Lab/nanodcal_input/3_nanodcal_NonEq/')
import nd_NonEq_input as ndi # type: ignore
# ========================================================
sys.path.append('/home/tangtang89/Example_Lab/')
from Tools import MKdir # type: ignore
# ========================================================

## Setting
# run = False
run = True

# repeatType, layerNum = ('u4x', 24)
# repeatGroup, LeadrepeatType, LeadlayerNum = ('Hex', 'u2x', 12)

# =====

repeatType, layerNum = ('u4y', 24)
repeatGroup, LeadrepeatType, LeadlayerNum = ('Tex', 'u2y', 12)

for Voltage in [
                # 0.01, 
                0.02, 0.03, 0.04,
                # 0.05
                ]:
    MKdir('OUTFILE', rm=True)

    layer = layerNum
    atom_type  = f'Co{layer}'
    # >>>>>
    readPath = f'../../0_PreFile/{repeatGroup}_Co{layer}_POSCAR_{repeatType}'
    MKdir(f"{repeatGroup}_Center_{repeatType}", rm=False)
    # <<<<<

    CoPd_nanod = ndi.Nd_MakingFile(File = readPath, atom_type = atom_type)
    # CoPd_nanod.PBE_BASIS()

    for theta in [
                0, 45
                ]:
        
        # >>>>>
        MKdir(f"{repeatGroup}_Center_{repeatType}/{theta:>003}_theta", rm=False)
        targetPath = f"{repeatGroup}_Center_{repeatType}/{theta:>003}_theta/vb{Voltage:.2f}"
        MKdir(f"{targetPath}", rm=True)
        name = f"{atom_type}TF_{theta:>003}_{repeatGroup}_{repeatType}_Center{Voltage}"
        mechine = "dl1x"
        ppn = "32"
        # <<<<<

        MKdir(targetPath, rm=True)
        # CoPd_nanod.atoms_xyz(r=(0.5,), theta=theta, phi=0) # For Hex
        CoPd_nanod.atoms_xyz(r=(0.5,), theta=theta, phi=90) # For Tex

        CoPd_nanod.scf_input(run_n=1, spinType='GeneralSpin', BasisFile='../../../../../../PBE_BASIS',
                            mixingMethod='realRho', mixing_rate=0.005, step=600, 
                            basis='PBE', 
                            precision='High', convergeVal='1e-5',
                            LeadRun=True, LeadSetup=(repeatType[-1], 
                                                    Voltage, 
                                                    f"../../../../../../1_Lead/{repeatGroup}_Lead_{LeadrepeatType}/{theta:>003}_theta/1run"
                                                    ), 
                            DonatorPath=f'../../vb{Voltage-0.01:.2f}/1run',
                            # DonatorPath=f'../../vb0.01/1run',
                            )
        CoPd_nanod.ndpbs(
                    name = name,
                    mechine = mechine,
                    ppn = ppn
                    )

        os.system(f'mv OUTFILE/* {targetPath}')
        #----------------------
        os.chdir(f"{targetPath}/1run/")
        print()
        os.system('pwd')
        print(f"{atom_type} at {theta:>003}")
        #----------------------
        if (run == True):
            if Voltage==0.01:
                os.system('qsub nanodcal.pbs')
            else:
                os.system('qsub-last nanodcal.pbs')
        else:
            pass
        #----------------------
        os.chdir('../../../../')
        os.system('pwd')
        print()
        #----------------------
os.system("rm -r OUTFILE")
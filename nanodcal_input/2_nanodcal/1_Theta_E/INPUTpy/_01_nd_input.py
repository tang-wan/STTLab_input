import numpy as np # type: ignore
import os
#----------------------------------------
import sys
sys.path.append('/home/tangtang89/Example_Lab/nanodcal_input/2_nanodcal/1_Theta_E/')
import nd_input as ndi # type: ignore
# ========================================================
sys.path.append('/home/tangtang89/Example_Lab/')
from Tools import MKdir # type: ignore
# ========================================================
MKdir('OUTFILE', rm=True)

## Setting
run = False
# run = True

start = 3
end = 15
for layer in range(start, end+1, 1):
    atom_type  = f'Pd{layer}'
    # >>>>>
    readPath = f'../../1_vasp/2_relax2/{layer}_{atom_type}_f/CONTCAR'
    MKdir(f'{layer}_{atom_type}_f', rm=False)
    # <<<<<

    CoPd_nanod = ndi.Nd_MakingFile(File = readPath, atom_type = atom_type)
    CoPd_nanod.PBE_BASIS()

    for theta in [
                0, 10, 20, 30, 45, 60, 70, 80, 90
                ]:
        
        # >>>>>
        targetPath = f"{layer}_{atom_type}_f/{theta:>003}_theta"

        name = f"{atom_type}_TF_{theta:>003}_scf_HIGH"
        mechine = "dl2x"
        ppn = "24"
        # <<<<<

        MKdir(targetPath, rm=True)
        CoPd_nanod.atoms_xyz(r=(0.5,), theta=theta, phi=0)
        CoPd_nanod.scf_input(run_n=1, spinType='GeneralSpin', BasisFile='../../../../PBE_BASIS',
                            mixingMethod='realRho', mixing_rate=0.005, step=600, 
                            basis='PBE', 
                            precision='High', convergeVal='1e-6',
                            LeadRun=False, LeadSetup=('x', 0.00, None), DonatorPath=None,
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
            os.system('qsub nanodcal.pbs')
        else:
            pass
        #----------------------
        os.chdir('../../../')
        os.system('pwd')
        print()
        #----------------------
os.system("rm -r OUTFILE")
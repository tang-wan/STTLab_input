import numpy as np # type: ignore
import os
import re
import sys
# ========================================================
sys.path.append('/home/tangtang89/Example_Lab/')
from Tools import MKdir, Check_out_Word, Process_Word # type: ignore
# ========================================================

def KPOINTS_manual(vasp_type=None, grid=(24, 24, 1), target_Path=None):
    
    Check_out_Word('Making KPOINTS')
    
    if vasp_type == 'band':
        if os.path.isfile(f'{target_Path}/KPATH.in'):
            
            MKdir(f"{target_Path}/preKPOINTS/", rm=True)
            os.system(f"mv {target_Path}/* {target_Path}/preKPOINTS/.")
            os.system(f"cp {target_Path}/preKPOINTS/POSCAR {target_Path}/preKPOINTS/POTCAR {target_Path}/.")

            Process_Word('Coping KPOINTS...')
            print()
            os.system(f'cp {target_Path}/preKPOINTS/KPATH.in {target_Path}/KPOINTS')
        else:
            Process_Word('Please run vaspkit 303 first')
            print()
            os._exit(0)
    
    else:
        Grid = f'{grid[0]}  {grid[1]}  {grid[2]}'
        Process_Word(f'KPOINTS is {grid[0]}  {grid[1]}  {grid[2]}')
        with open('OUTFILE/KPOINTS', 'w') as File:
            lines = [
                'K-Spacing Value to Generate K-Mesh: 0.020\n',
                '0\n',
                'Gamma\n',
            f'{Grid}\n',
                '0.0  0.0  0.0\n'
            ]
            File.writelines(lines)

def KPOINTS(vasp_type=None, target_Path=None):
    if vasp_type == 'band':
        MKdir(f"{target_Path}/preKPOINTS/", rm=True)
        os.system(f"mv {target_Path}/* {target_Path}/preKPOINTS/.")
        os.system(f"cp {target_Path}/preKPOINTS/POSCAR {target_Path}/preKPOINTS/POTCAR {target_Path}/.")
        HomePath = os.getcwd()
        os.chdir(f"{target_Path}/preKPOINTS/")
        os.system("vaspkit -task 303")
        os.chdir(f"{HomePath}")
        os.system(f'cp {target_Path}/preKPOINTS/KPATH.in {target_Path}/KPOINTS')
    
    else:
        os.chdir("OUTFILE/")
        os.system("vaspkit -task 102 -kpr 0.02")
        os.chdir("../")

if __name__ == '__main__':
    
    os.system("rm -r *_f")
    if os.path.isdir("./OUTFILE"):
        pass
    else:
        os.system("mkdir OUTFILE")

    #----------------------------------------
    layer_num = int(2)
    #----------------------------------------
    atom_type = f'Pd6Co{layer_num:.0f}'

# ========================================================    
# ========================================================
    # KPOINTS_manual(type='Bilayer')   # KPOINTS
    KPOINTS()   # KPOINTS
#----------------------
    file_name = f"{int(layer_num)}_{atom_type}_f"
    os.system(f"mkdir {file_name}/")
#----------------------
    os.system(f"cp OUTFILE/* {file_name}/.")
    os.system(f"cp ~/vdw_kernel.bindat {file_name}/.")
#----------------------
    os.chdir(f"{file_name}/")
    print()
    os.system('pwd')
    print(f"{atom_type}")
#----------------------
    os.chdir('../')
    os.system('pwd')

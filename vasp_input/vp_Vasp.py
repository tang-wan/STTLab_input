import numpy as np # type: ignore
import os

def vasppbs(name, mechine, ppn, type='std'):

    if type == 'std':
        vasp = 'vasp_std'
    elif type == 'ncl':
        vasp = 'vasp_ncl'

    with open('OUTFILE/vasp6.pbs', 'w') as File:
        lines = [
            '#!/bin/bash\n',
            '#=============================================#\n',
            '# Job Name\n',
            '\n',
            f'#PBS -N {name}\n',
            '\n',
            '#---------------------------------------------#\n',
            '# Running machine (ppn: process per node)\n',
            '\n',
            f'#PBS -l nodes={mechine}:ppn={ppn}\n',
            '\n',
            '#---------------------------------------------#\n',
            '# Setup environment variable\n',
            '# Use `module avail` to see more\n',
            '\n',
            'module purge\n',
            'module load vasp/6.2.0\n',
            '\n',
            '#=============================================#\n',
            '\n',
            'cd $PBS_O_WORKDIR\n',
            '\n',
            '# available: vasp_gam | vasp_ncl | vasp_std\n',
           f'mpirun {vasp}\n'
        ]
        File.writelines(lines)

def vaspsh(name, mechine, ppn, type='std'):
    if type == 'std':
        vasp = 'vasp_std'
    elif type == 'ncl':
        vasp = 'vasp_ncl'

    with open('OUTFILE/vasp6.sh', 'w') as File:
        lines = [
                '#!/bin/bash\n'
                '#=============================================#\n'
                '# Job Name\n'
                '\n'
               f'#SBATCH -J {name}\n'
                '\n'
                '#---------------------------------------------#\n'
                '# Computing resources\n'
                '\n'
                '#SBATCH -A MST112204\n'
               f'#SBATCH -p {mechine}\n'
                '#SBATCH -o job_%j.out\n'
                '#SBATCH -e job_%j.err\n'
               f'#SBATCH --ntasks={ppn}\n'
                '#SBATCH --cpus-per-task=1\n'
                '\n'
                '#---------------------------------------------#\n'
                '# Setup environment variable\n'
                '# Use `module avail` to see more\n'
                '\n'
                'module purge\n'
                'module load labstt/vasp/6.3.2_intel-2021\n'
                '\n'
                '#=============================================#\n'
                '\n'
                'cd $SLURM_SUBMIT_DIR\n'
                '\n'
                '#--- Run your program here ---#\n'
                '\n'
                '# available: vasp_gam | vasp_ncl | vasp_std\n'
               f'mpirun {vasp}\n'
        ]
        File.writelines(lines)

#----------------------
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

    ## vasp
    name = f"{atom_type}_SL_NonColl_woSOCrelax"
    # for STT
    # mechine = "dl0x"
    # ppn = "20"

    # vasppbs(
    #     name = name,
    #     mechine = mechine,
    #     ppn = ppn,
    #     type='std' # available: vasp_gam | vasp_ncl | vasp_std
    # )

    # for NCHC
    mechine = "ct56"
    ppn = "28"
    vaspsh(
        name = name,
        mechine = mechine,
        ppn = ppn,
        type='std' # available: vasp_gam | vasp_ncl | vasp_std
    )

#----------------------
    file_name = f"{int(layer_num)}_{atom_type}_f"
    os.system(f"mkdir {file_name}/")
#----------------------
    os.system(f"cp OUTFILE/* {file_name}/.")
#----------------------
    os.chdir(f"{file_name}/")
    print()
    os.system('pwd')
    print(f"{atom_type}")
#----------------------
    os.chdir('../')
    os.system('pwd')

import numpy as np # type: ignore
import os

class Nd_analysis():
    def __init__(self, matPath='../../1run/NanodcalStructObject.mat'):
        self.matPath = matPath

    def main(self, analysis_type,
             BiasWin, 
             grid_num,
             ):
        matPath = self.matPath
        self.analysis_type = analysis_type

        match analysis_type: # type: ignore
            case 'charge':
                lines = [
                    '# Calculate charge\n',
                   f'system.object = {matPath}\n',
                    'calculation.name = charge\n',
                    'calculation.charge.whatProjected = \'Atom\'\n',
                    ]
                with open('OUTFILE/main.input', 'w') as W_File:
                    W_File.writelines(lines)          
            case 'totalEnergy':
                lines = [
                    f'system.object = {matPath}\n',
                        '#calculation.control.energyUnit = eV\n',
                        'calculation.name = totalEnergy\n',
                        '#calculation.totalEnergy.decomposed = true\n',
                        ]
                with open('OUTFILE/main.input', 'w') as W_File:
                    W_File.writelines(lines)
            case 'spinTorque':
                lines=[
                        'import numpy as np\n',
                        'import junpy as jp\n',
                        'from junpy.factory import nanodcal\n',
                        'from junpy.experiment.extend_center_2 import extend_center\n',
                        '\n',
                        '#==============================================================================\n',
                        '\n',
                       f'filename = {matPath}\n',
                        'device0 = nanodcal.load_nanodcal_device(filename)\n',
                        'device = extend_center(device0, 1, 1)\n',
                        '\n',
                        '#==============================================================================\n',
                        '\n',
                        'calc = jp.calculation.SpinTorque(\n',
                        '    device=device,\n',
                        '    kpoints=jp.UniformKspaceSampling(\n',
                       f'        gridNumber={grid_num},\n',
                        '        isTimeReversalSymmetry=False,\n',
                        '    ),\n',
                       f'    nonequilibriumEnergies=jp.BiasWindow(interval={BiasWin}),\n',
                        '    equilibriumEnergies=dict(\n',
                        '        circlePoints=30,\n',
                        '        lowestEnergy=-30,\n',
                        '    ),\n',
                        '    etaSigma=1e-2,\n',
                        '    etaGF=1e-2,\n',
                        '    spinAccumulationDetail=True,\n',
                        ')\n',
                        'jp.run(calc)\n',
                        '\n',
                        '#==============================================================================\n',
                    ]
                with open('OUTFILE/main.py', 'w') as W_File:
                    W_File.writelines(lines)    
            case 'current':
                lines=[
                        'import numpy as np\n',
                        'import junpy as jp\n',
                        'from junpy.factory import nanodcal\n',
                        '\n'
                        '#==============================================================================\n',
                        '\n'
                       f'filename = {matPath}\n',
                        'device = nanodcal.load_nanodcal_device(filename)\n',
                        '\n'
                        '#==============================================================================\n',
                        '\n'
                        'calc = jp.calculation.Current(\n',
                        '    device=device,\n',
                        '    kpoints=jp.UniformKspaceSampling(\n',
                       f'        gridNumber={grid_num},\n',
                        '        isTimeReversalSymmetry=False,\n',
                        '       ),\n',
                       f'   energies=jp.BiasWindow(interval={BiasWin}),\n',
                        '   etaSigma=1e-3,\n',
                        '   etaGF=1e-3,\n',
                        ')\n',
                        'jp.run(calc)\n',
                        '\n'
                        '#==============================================================================\n',
                    ]
                with open('OUTFILE/main.py', 'w') as W_File:
                    W_File.writelines(lines) 
            case _:
                print('No this analysis method')

    def ndpbs(self, name, mechine='i5x', ppn=1):
        analysis_type = self.analysis_type
        if analysis_type=='spinTorque' or analysis_type=='current':
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
                    '#PBS -j oe\n',
                    '\n',
                    '#---------------------------------------------#\n',
                    '# Setup environment variable\n',
                    '# Use `module avail` to see more\n',
                    '\n',
                    'module purge\n',
                    '#--- Load the module you want ---#\n',
                    'module load junpy/0.16\n',
                    '\n',
                    '#=============================================#\n',
                    '\n',
                    'cd $PBS_O_WORKDIR\n',
                    '\n',
                    '#--- Run your program here ---#\n',
                    '\n',
                    'export OMP_NUM_THREADS=1\n',
                    'mpirun python3 main.py > main.log\n',
                    ]
            with open('OUTFILE/junpy.pbs', 'w') as W_File:
                W_File.writelines(lines)

        else:
            lines = [
                    '#!/bin/bash\n',
                    '#=============================================#\n',
                    '# Job information\n',
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
                    'module load nanodcal/2020B\n',
                    '#---------------------------------------------#\n',
                    '\n',
                    '# input and output filename\n',
                    'inputFile="main.input"\n',
                    'outputFile="main.output"\n',
                    '\n',
                    '# store temporarydata to memory\n',
                    'temporarydata_at_tmp=true\n',
                    '\n',
                    '#=============================================#\n',
                    '\n',
                    'cd $PBS_O_WORKDIR\n',
                    '\n',
                    '#--- Run your program here ---#\n',
                    '\n',
                    '# link temporarydata to TMPDIR if needed\n',
                    'if $temporarydata_at_tmp; then\n',
                        'rm -rf ./temporarydata\n',
                        'ln -s $TMPDIR ./temporarydata\n',
                    'fi\n',
                    '\n',
                    '# run nanodcal\n',
                    'mpirun nanodcal -parallel $inputFile > $outputFile\n',
                    '\n',
                    '# remove ./temporarydata if it is a symbolic link\n',
                    'if [ -L "./temporarydata" ]; then\n',
                        'unlink "./temporarydata"\n',
                    'fi\n',
                    ]
            with open('OUTFILE/nanodcal.pbs', 'w') as W_File:
                W_File.writelines(lines)

    def ndsh(self, name, mechine='ctest', ppn=1):
        analysis_type = self.analysis_type
        if analysis_type=='spinTorque' or analysis_type=='current':
            lines = [
                    '#!/bin/bash\n',
                    '#=============================================#\n',
                    '# Job Name\n',
                    '\n',
                    f'#SBATCH -J \'{name}\' \n',
                    '\n',
                    '#---------------------------------------------#\n',
                    '# Computing resources\n',
                    '\n',
                    '#SBATCH -A MST112204\n',
                    f'#SBATCH -p {mechine}\n',
                    '#SBATCH -o job_%j.out\n',
                    '#SBATCH -e job_%j.err\n',
                    f'#SBATCH --ntasks={ppn}\n',
                    '#SBATCH --cpus-per-task=1\n',
                    '\n',
                    '#---------------------------------------------#\n',
                    '# Setup environment variable\n',
                    '# Use `module avail` to see more\n',
                    '\n',
                    'module purge\n',
                    'module load labstt/nanodcal/2020B_matlab-R2020b_gcc-9.4.0_openmpi-4.1.1_singleThread\n',
                    '\n',
                    '#=============================================#\n',
                    '\n',
                    'cd $SLURM_SUBMIT_DIR\n',
                    '\n',
                    '#--- Run your program here ---#\n',
                    '\n'
                    'export OMP_NUM_THREADS=1\n',
                    'mpirun nanodcal -parallel main.py > main.log\n',
                    ]
            with open('OUTFILE/junpy.sh', 'w') as W_File:
                W_File.writelines(lines)

        else:
            lines = [
                    '#!/bin/bash\n',
                    '#=============================================#\n',
                    '# Job Name\n',
                    '\n',
                    f'#SBATCH -J \'{name}\' \n',
                    '\n',
                    '#---------------------------------------------#\n',
                    '# Computing resources\n',
                    '\n',
                    '#SBATCH -A MST112204\n',
                    f'#SBATCH -p {mechine}\n',
                    '#SBATCH -o job_%j.out\n',
                    '#SBATCH -e job_%j.err\n',
                    f'#SBATCH --ntasks={ppn}\n',
                    '#SBATCH --cpus-per-task=1\n',
                    '\n',
                    '#---------------------------------------------#\n',
                    '# Setup environment variable\n',
                    '# Use `module avail` to see more\n',
                    '\n',
                    'module purge\n',
                    'module load labstt/nanodcal/2020B_matlab-R2020b_gcc-9.4.0_openmpi-4.1.1_singleThread\n',
                    '\n',
                    '#=============================================#\n',
                    '\n',
                    'cd $SLURM_SUBMIT_DIR\n',
                    '\n',
                    '#--- Run your program here ---#\n',
                    '\n'
                    'export OMP_NUM_THREADS=1\n',
                    'mpirun nanodcal -parallel main.input > main.output\n',
                    ]
            with open('OUTFILE/nanodcal.sh', 'w') as W_File:
                W_File.writelines(lines)

if __name__ == '__main__':

    # os.system('rm -r *_f')
    os.system('rm -r OUTFILE')
    os.system('mkdir OUTFILE')

    layer      = 2
    atom_type  = f'Pd6Co{layer}'
    
    ana_list = [('charge', 'i5x', '1'),
                ('totalEnergy', 'i5x', '1'),
                ('spinTorque', 'dl0x', '10'),
                ('band', 'i91', '18')]
    ana_type = ana_list[-1][0]

    test_nanod = Nd_analysis(matPath = '../../1run/NanodcalStructObject.mat')
    # ==========================================
    test_nanod.main(analysis_type = ana_type,
                    grid_num=(64,64,1), # Only for JunPy
                    symmetryKPoints="{'G','M','K','G'}", # Only for Band
                    Coor_symmetryKPoints="[0 0 0; 1/2 1/2 0; 1/3 1/3 2/3; 0 0 0]" # Only for Band
             )
    # ==========================================
    for theta in [0, 45, 90]:
        if not(os.path.isdir(f'{layer}_{atom_type}_f/{theta:>003}_theta/analysis')):
            os.system(f'mkdir {layer}_{atom_type}_f/{theta:>003}_theta/analysis')

        if not(os.path.isdir(f'{layer}_{atom_type}_f/{theta:>003}_theta/analysis/{ana_type}')):
            os.system(f'mkdir {layer}_{atom_type}_f/{theta:>003}_theta/analysis/{ana_type}')
    # ==========================================
        name = f"{atom_type}_{theta:>003}_SL_wSOC_{ana_type}"
        mechine = ana_list[0][1]
        ppn = ana_list[0][2]
        test_nanod.ndpbs(
                    name = name,
                    mechine = mechine,
                    ppn = ppn
                    )
    # ==========================================
        os.system(f'mv OUTFILE/* {layer}_{atom_type}_f/{theta:>003}_theta/analysis/{ana_type}')

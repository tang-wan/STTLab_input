import numpy as np # type: ignore
import os
import glob
from colorama import init, Fore, Back # type: ignore
# ========================================================
import sys
sys.path.append('/home/tangtang89/Example_Lab/')
from Tools import MKdir, Check_out_Word, Process_Word # type: ignore
# ========================================================

def Basis_Content(nd_basis, basis_type, atom_type):
    match nd_basis:
        # LDA only
        case '1_nanodcalbasis_DZP':
            if basis_type=='LDA':
                pre_basis_path = glob.glob(f'/home/share/nanodcal_basis/{nd_basis[0:-4]}/{atom_type}/LDA/{atom_type}_*')
                basis_path = pre_basis_path[0] + f'/{atom_type}_DZP.nad'
            elif basis_type=='PBE':
                pre_basis_path = glob.glob(f'/home/share/nanodcal_basis/{nd_basis[0:-4]}/{atom_type}/LDA/{atom_type}_*')
                basis_path = pre_basis_path[0] + f'/{atom_type}_DZP.nad'
                print(f'>>>>> There is NO PBE basis in {nd_basis}, only LDA <<<<<')
            tail_name = 'DZP'
        # ====
        # PBE only
        case '2_PBE-Basis-beta_DZP':
            if basis_type=='PBE':
                pre_basis_path = glob.glob(f'/home/share/nanodcal_basis/{nd_basis[0:-4]}/database/{atom_type}/PBE/{atom_type}_*/')
                basis_path = pre_basis_path[0] + f'/{atom_type}_DZP_{basis_type.upper()}.nad'
            elif basis_type=='LDA':
                pre_basis_path = glob.glob(f'/home/share/nanodcal_basis/{nd_basis[0:-4]}/database/{atom_type}/PBE/{atom_type}_*/')
                basis_path = pre_basis_path[0] + f'/{atom_type}_DZP_{basis_type.upper()}.nad'
                print(f'>>>>> There is NO LDA basis in {nd_basis}, only PBE <<<<<')
            tail_name = f'DZP_{basis_type.upper()}'
        # ====
        # NOT to USE
        case '3_basis_APL2016':
            print(f'>>>>> {nd_basis} is NOT used <<<<<')
        # ====
        # Both
        case '4_neutralatomdatabase_DZP':
            basis_path = f'/home/share/nanodcal_basis/{nd_basis[0:-4]}_DeviceStudio2022A/general/{atom_type}_{basis_type.upper()}-DZP.nad'
            tail_name = f'{basis_type.upper()}-DZP'
        # ====
        # Both (5_nano_tm_lda & 5_nano_tm_pbe)
        case '5_nano_tm_DZP':
            basis_path = f'/home/share/nanodcal_basis/5_nano_tm_{basis_type.lower()}/{atom_type}_TM_{basis_type.upper()}_DZP/{atom_type}_TM_{basis_type.upper()}_DZP.mat'
            tail_name = f'TM_{basis_type.upper()}_DZP'
        # ====
        # Both (6_psdojo_lda_v0.4 & 6_psdojo_pbe_v0.4)
        case '6_psdojo_TZP':
            basis_path = f'/home/share/nanodcal_basis/6_psdojo_{basis_type.lower()}_v0.4/{atom_type}_{basis_type.upper()}_TZP/{atom_type}_{basis_type.upper()}_TZP.mat'
            tail_name = f'{basis_type.upper()}_TZP'
        # ====
        # Both (7_Nano_TM_LDA-34e93a78-3611-4228-9a1c-48b0c2b33f5b & 7_Nano_TM_PBE-811bc05f-31ee-46b8-ad3f-8392c2d639cf)
        case '7_Nano_TM_DZP':
            if basis_type=='LDA':
                basis_path = f'/home/share/nanodcal_basis/7_Nano_TM_{basis_type.upper()}-34e93a78-3611-4228-9a1c-48b0c2b33f5b/{atom_type}_LDA_TM/{atom_type}_LDA_TM_DZP.mat'
            elif basis_type=='PBE':
                basis_path = f'/home/share/nanodcal_basis/7_Nano_TM_{basis_type.upper()}-811bc05f-31ee-46b8-ad3f-8392c2d639cf/{atom_type}_PBE_TM/{atom_type}_PBE_TM_DZP.mat'
            tail_name = f'{basis_type.upper()}_TM_DZP'
        # ====
        # Both (8_psdojo_lda_v0.4-a7838b48-1601-4c83-80f1-01068c97438f.4 & 8_psdojo_pbe_v0.4-8e3a045d-9172-4c1d-96c2-41506a953312.4)
        case '8_psdojo_TZP':
            if basis_type=='LDA':
                basis_path = f'/home/share/nanodcal_basis/8_psdojo_{basis_type.lower()}_v0.4-a7838b48-1601-4c83-80f1-01068c97438f.4/{atom_type}_{basis_type.upper()}_OV/{atom_type}_{basis_type.upper()}_OV_TZP.mat'
            elif basis_type=='PBE':
                basis_path = f'/home/share/nanodcal_basis/8_psdojo_{basis_type.lower()}_v0.4-8e3a045d-9172-4c1d-96c2-41506a953312.4/{atom_type}_{basis_type.upper()}_OV/{atom_type}_{basis_type.upper()}_OV_TZP.mat'
            tail_name = f'{basis_type.upper()}_OV_TZP'
        # PBE only
        case '8_psdojo_DZP':
            if basis_type=='LDA':
                basis_path = f'/home/share/nanodcal_basis/8_psdojo_{basis_type.lower()}_v0.4-8e3a045d-9172-4c1d-96c2-41506a953312.4/{atom_type}_PBE_OV/{atom_type}_PBE_OV_DZP.mat'
                print(f'>>>>> There is NO LDA basis in {nd_basis}, only PBE <<<<<')
            elif basis_type=='PBE':
                basis_path = f'/home/share/nanodcal_basis/8_psdojo_{basis_type.lower()}_v0.4-8e3a045d-9172-4c1d-96c2-41506a953312.4/{atom_type}_PBE_OV/{atom_type}_PBE_OV_DZP.mat'
            tail_name = 'PBE_OV_DZP'
        # PBE only
        case '8_psdojo_SZP':
            if basis_type=='LDA':
                basis_path = f'/home/share/nanodcal_basis/8_psdojo_{basis_type.lower()}_v0.4-8e3a045d-9172-4c1d-96c2-41506a953312.4/{atom_type}_PBE_OV/{atom_type}_PBE_OV_SZP.mat'
                print(f'>>>>> There is NO LDA basis in {nd_basis}, only PBE <<<<<')
            elif basis_type=='PBE':
                basis_path = f'/home/share/nanodcal_basis/8_psdojo_{basis_type.lower()}_v0.4-8e3a045d-9172-4c1d-96c2-41506a953312.4/{atom_type}_PBE_OV/{atom_type}_PBE_OV_SZP.mat'
            tail_name = 'PBE_OV_SZP'
    
    return basis_path, tail_name

# ========================================================
class Nd_Basis_Test():
    def __init__(self, nd_basis, basis_type,
                 atom_type, SOC):
        self.nd_basis   = nd_basis
        self.basis_type = basis_type
        self.atom_type  = atom_type
        self.basis_path, self.tail_name = Basis_Content(nd_basis, basis_type, atom_type)
        self.info_Path  = f'/home/share/nanodcal_basis/5_nano_tm_{basis_type.lower()}/{atom_type}_TM_{basis_type.upper()}_DZP/dzp'
        self.SOC = SOC
        
        print()
        Check_out_Word('Inital')
        # ====
        MKdir(f'{atom_type}', rm=False)
        print()

    def Read_info(self, printTrue=True):
        atom_type = self.atom_type
        info_Path = self.info_Path
        # ====
        with open(f'{info_Path}/{atom_type}.fxyz', 'r') as R_File:
            content = R_File.readlines()
            self.atomLabel = content[0:2]
            self.atomPosition = content[2:]
        
        Check_out_Word("Reading Information")

        Process_Word('atoms.xyz')

        if printTrue:
            for i in range(len(self.atomLabel)):
                print(self.atomLabel[i][:-1:])
            for i in range(len(self.atomPosition)):
                print(self.atomPosition[i][:-1:])
        else:
            print('NOT OUTPUT')
        
        # ====
        with open(f'{info_Path}/{atom_type}.xyz', 'r') as R_File:
            content = R_File.readlines()
        Latt_vec = content[1].split()[0:9]
        Process_Word('Lattice vector')
        a_vec = [float(Latt_vec[0][9:]), float(Latt_vec[1]), float(Latt_vec[2])]
        b_vec = [float(Latt_vec[3]), float(Latt_vec[4]), float(Latt_vec[5])]
        c_vec = [float(Latt_vec[6]), float(Latt_vec[7]), float(Latt_vec[8][:-1:])]
        
        if printTrue:
            print(a_vec)
            print(b_vec)
            print(c_vec)
        else:
            print('NOT OUTPUT')

        self.a_vec = a_vec
        self.b_vec = b_vec
        self.c_vec = c_vec
        print()

    def atoms_xyz(self, r, theta, phi, type='Cart'):

        SOC = self.SOC
        nd_basis = self.nd_basis
        basis_type = self.basis_type
        atom_type = self.atom_type
        a_vec = np.array(self.a_vec)
        b_vec = np.array(self.b_vec)
        c_vec = np.array(self.c_vec)
        
        # ====
        
        if SOC:
            target_Path = f'{atom_type}/{nd_basis}_{basis_type}_soc_xz{theta}_mz{r}'
        else:
            target_Path = f'{atom_type}/{nd_basis}_{basis_type}_ncl_xz{theta}_mz{r}'
        self.target_Path = target_Path
        
        Check_out_Word(f'Making subfolder')
        MKdir(f'{target_Path}', rm=True)
        print()
        
        # ====
        
        atomPosition = self.atomPosition
        atomLabel = self.atomLabel
        
        atom_num = atomLabel[0][0:-1]
        title = atomLabel[1][0:-1] + '  SpinPolarization_r  SpinPolarization_theta  SpinPolarization_phi'
        
        content_list = []
        content_list.append(atom_num)
        content_list.append(title)
        for atom_cont in atomPosition:
            sp_atomPosition = atom_cont[:-1:].split()

            label = sp_atomPosition[0]
            Position_frac_list = sp_atomPosition[1:]
            Position_Cart_list = list(float(Position_frac_list[0])*a_vec + 
                                        float(Position_frac_list[1])*b_vec + 
                                        float(Position_frac_list[2])*c_vec)
            new_atom_list = []
            new_atom_list.append(label)
            if type=='Cart':
                new_atom_list.extend(Position_Cart_list)
            elif type=='Frac':
                new_atom_list.extend(Position_frac_list)

            new_atom_str = f"{new_atom_list[0]:>8}  {new_atom_list[1]:<021}  {new_atom_list[2]:<021}  {new_atom_list[3]:<021}"

            atom_cont = new_atom_str + f'  {float(r):<018}  {float(theta):<022}  {float(phi):<020}'
            content_list.append(atom_cont)

        # ====
        
        Check_out_Word('Atoms file')
        Process_Word(f'Making {target_Path}/atoms.xyz ({type})')
        print()
        with open(f'{target_Path}/atoms.xyz', 'w') as W_File:
            for line in content_list:
                W_File.writelines(line + '\n')
        return target_Path

    def BASIS(self):

        basis_type = self.basis_type
        basis_path = self.basis_path
        target_Path = self.target_Path
        
        Check_out_Word('BASIS')
        # ====
        if os.path.isdir(f'{target_Path}/{basis_type}_BASIS'):
            Process_Word(f'{target_Path}/{basis_type}_BASIS is exist. Removing...')
            os.system(f'rm -r {target_Path}/{basis_type}_BASIS')
            Process_Word(f'Making new {target_Path}/{basis_type}_BASIS')
            print(f'From {basis_path}')
            os.system(f'mkdir {target_Path}/{basis_type}_BASIS')
        else:
            Process_Word(f'{target_Path}/{basis_type}_BASIS is NOT exist.')
            Process_Word(f'Making new {target_Path}/{basis_type}_BASIS')
            print(f'From {basis_path}')
            os.system(f'mkdir {target_Path}/{basis_type}_BASIS')

        os.system(f'cp {basis_path} {target_Path}/{basis_type}_BASIS')
        print()

    def scf_input(self, spinType='GeneralSpin',
                mixing_rate=0.005, step=200, 
                precision='Double'):
        
        basis       = self.basis_type
        target_Path = self.target_Path
        atom_type   = self.atom_type
        tail_name   = self.tail_name
        SOC         = self.SOC
        
        if basis=='PBE':
            Excorre = 'GGA_PBE96'
        elif basis=='LDA':
            Excorre = 'LDA_PZ81'
        
        if precision=='Double':
            pre_list='calculation.realspacegrids.E_cutoff = 300 Hartree\n' +  'calculation.k_spacegrids.L_cutoff = 160 Bohr\n'
        elif precision=='High':
            pre_list='#calculation.realspacegrids.E_cutoff = 300 Hartree\n' +  '#calculation.k_spacegrids.L_cutoff = 160 Bohr\n'
        
        if SOC:
            SOC_list = 'calculation.spinOrbitInteraction.isIncluded = true'
        else:
            SOC_list = 'calculation.spinOrbitInteraction.isIncluded = false'

        # LattCont
        a_vec, b_vec, c_vec = self.a_vec, self.b_vec, self.c_vec
        
        Check_out_Word(f'Input file')
        Process_Word(f'Making {target_Path}/scf.input')

        with open(f'{target_Path}/scf.input', 'w') as W_File:
            lines=[
                    '# Descriptive name for the system\n',
                   f'system.name = {atom_type}\n',
                    '\n',
                    '# Format for input and output of information\n',
                    'calculation.control.energyUnit = eV\n',
                    'calculation.control.lengthUnit = angstrom\n',
                    '\n',
                    '# Quantum mechanical description\n',
                   f'system.spinType = {spinType}\n',
                   f'system.orbitalType = {tail_name}\n',
                   f'system.neutralAtomDataDirectory = ./{basis}_BASIS\n',
                    '\n',
                    '# Positions and chemical species of the atoms\n',
                   f'system.centralCellVector1 = [{np.round(a_vec[0], 15):<019},  {np.round(a_vec[1], 15):<019},  {np.round(a_vec[2], 15):<019}]\n',
                   f'system.centralCellVector2 = [{np.round(b_vec[0], 15):<019},  {np.round(b_vec[1], 15):<019},  {np.round(b_vec[2], 15):<019}]\n',
                   f'system.centralCellVector3 = [{np.round(c_vec[0], 15):<019},  {np.round(c_vec[1], 15):<019},  {np.round(c_vec[2], 15):<019}]\n',
                    'system.atomCoordinateFormat = cartesian\n',
                    'system.atomFile = ./atoms.xyz\n',
                    '\n',
                    '# Control parameters\n',
                   f'calculation.xcFunctional.Type = {Excorre}\n',
                   f'{SOC_list}\n',
                    '\n',
                    '# What quantities should be calculated\n',
                    'calculation.name = scf\n',
                    '\n',
                    '# Accuracy of the calculation\n',
                    'calculation.control.precision = high\n',
                     pre_list,
                    '#calculation.occupationFunction.temperature = 0\n',
                    '\n',
                    '## Speed of convergence of the algorithms\n',
                    'calculation.SCF.startingMode = realRho\n',
                    'calculation.SCF.mixingMode = realRho\n',
                    'calculation.SCF.mixMethod = Pulay\n',
                   f'calculation.SCF.mixRate = {mixing_rate}\n',
                   f'calculation.SCF.maximumSteps = {step}\n',
                    'calculation.SCF.monitoredVariableName = {\'realSpaceRho\',\'hMatrix\',\'rhoMatrix\',\'totalEnergy\',\'bandEnergy\',\'gridCharge\',\'orbitalCharge\',\'spinPolar\'}\n',
                    'calculation.SCF.convergenceCriteria = {1e-6, 1e-6, 1e-6, 1e-6, [],[],[],[]}\n',
                    'calculation.SCF.donatorObject = ./NanodcalObject.mat\n'
            ]
            W_File.writelines(lines)
        print()
    
    def ndpbs(self, mechine, ppn):
        target_Path = self.target_Path
        SOC = self.SOC
        Check_out_Word(f'PBS File')
        Process_Word(f'Making {target_Path}/nanodcal.pbs')
        print()

        nd_basis = self.nd_basis
        atom = self.atom_type

        if SOC:
            name = f"{atom}_{nd_basis[:-4:]}_SOC_basisTest"
        else:
            name = f"{atom}_{nd_basis[:-4:]}_ncl_basisTest"

        with open(f'{target_Path}/nanodcal.pbs', 'w') as W_File:
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
                '\n',
                '#---------------------------------------------#\n',
                '\n',
                '# input and output filename\n',
                'inputFile="scf.input"\n',
                'outputFile="scf.output"\n',
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
                '    rm -rf ./temporarydata\n',
                '    ln -s $TMPDIR ./temporarydata\n',
                'fi\n',
                '\n',
                '# run nanodcal\n',
                'mpirun nanodcal -parallel $inputFile > $outputFile\n',
                '\n',
                '# remove ./temporarydata if it is a symbolic link\n',
                'if [ -L "./temporarydata" ]; then\n',
                '    unlink "./temporarydata"\n',
                'fi\n',
                '\n'
            ]

            W_File.writelines(lines)

    def ndsh(self, mechine, ppn):
        
        nd_basis = self.nd_basis
        atom     = self.atom_type
        SOC      = self.SOC
        
        if SOC:
            name = f"{atom}_{nd_basis[:-4:]}_SOC_basisTest"
        else:
            name = f"{atom}_{nd_basis[:-4:]}_ncl_basisTest"

        with open(f'OUTFILE/{self.run_n}run/nanodcal.sh', 'w') as W_File:
            lines = [
                '#!/bin/bash\n'
                '#=============================================#\n'
                '# Job Name\n'
                '\n'
               f'#SBATCH -J  {name}\n'
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
                'module load labstt/nanodcal/2020B_matlab-R2020b_gcc-9.4.0_openmpi-4.1.1_singleThread\n'
                '\n'
                '#=============================================#\n'
                '\n'
                'cd $SLURM_SUBMIT_DIR\n'
                '\n'
                '#--- Run your program here ---#\n'
                '\n'
                'export OMP_NUM_THREADS=1\n'
                'mpirun nanodcal -parallel scf.input > scf.output\n'
            ]

            W_File.writelines(lines)

    def QSUB(self):

        target_Path = self.target_Path

        Check_out_Word('Submit the Job')
        os.chdir(f'{target_Path}')

        judge = 0
        for file in ['atoms.xyz', 'nanodcal.pbs', 'scf.input']:
            if os.path.isfile(f'{file}'):
                Process_Word(f'{file:^12} is exit !!')
                judge = judge + 1
            else:
                Process_Word(f'{file:^12} is NOT exit !!')
        
        if judge==3:
            os.system('qsub nanodcal.pbs')
        else:
            Process_Word('REFUSE THIS SUCK JOB')
        os.chdir('../../')
        print()

if __name__ == '__main__':
    basis_list = [
        '1_nanodcalbasis_DZP',          # 0, LDA
        '2_PBE-Basis-beta_DZP',         # 1, PBE
        '4_neutralatomdatabase_DZP',    # 2, BOTH
        '5_nano_tm_DZP',                # 3, BOTH
        '6_psdojo_TZP',                 # 4, BOTH
        '7_Nano_TM_DZP',                # 5, BOTH
        '8_psdojo_TZP',                 # 6, BOTH (not SOC)
        '8_psdojo_DZP',                 # 7, PBE  (not SOC)
        '8_psdojo_SZP'                  # 8, PBE  (not SOC)
    ]
# ----------
    run      = False
    # run      = True
# ----------
    basis    = 'PBE'
    atom     = 'Pt'
    # SOC      = False
    SOC      = True
    
    if basis == 'PBE':
        run_list = range(1, 6, 1)
    elif basis == 'LDA':
        run_list = [0, 2, 3, 4, 5]
    
    for i in run_list:
        nd_basis = basis_list[i]
        print(nd_basis)

        spec_atom = Nd_Basis_Test(
                                nd_basis   = nd_basis,
                                basis_type = basis,
                                atom_type  = atom,
                                SOC        = SOC
                                )
        spec_atom.Read_info(
                # printTrue=False
                )
        spec_atom.atoms_xyz(r=0.0, theta=0, phi=0, 
                    type='Cart'
                    )
        spec_atom.BASIS()
        spec_atom.scf_input(
                            spinType='GeneralSpin',
                            mixing_rate=0.01, step=200, 
                            precision='High'
                            )
        
        mechine = "i91"
        ppn = "14"
        spec_atom.ndpbs(
                        mechine = mechine,
                        ppn = ppn
                        )
        if run:
            spec_atom.QSUB()
        else:
            pass

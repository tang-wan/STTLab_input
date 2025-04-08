import numpy as np # type: ignore
import os
import re
import sys
# ========================
sys.path.append('/home/tangtang89/Example_Lab/')
from Tools import MKdir, POSCARConvert # type: ignore
# ========================

class Nd_MakingFile():

    def __init__(self, File, atom_type):
        self.File = File
        self.type = atom_type

        # atom type in str
        self.atom_st          = re.sub(u'([^\u0041-\u007a])', ' ', atom_type)
        # atom type in lsit
        self.atom             = self.atom_st.split()
        
        # atom number in str
        self.atom_num_st      = re.sub(u'([^\u0030-\u0039])', ' ', atom_type).replace(" ", "", 1)
        # atom number in list
        self.atom_num         = list(map(int, self.atom_num_st.split()))
        self.m                = sum(self.atom_num)

        self.NdFile = POSCARConvert(File, atom_type)

        parse = self.NdFile.ReadPOSCAR()   
        # print(parse)   
        self.atom_array = parse[0]
        self.a_vec, self.b_vec, self.c_vec = parse[1][0], parse[1][1], parse[1][2]
        self.LatticeConstant = parse[2]
        self.atom_array_dir  = parse[3]
        self.atom_array_car  = parse[4]

    def atoms_xyz(self, r, theta, phi):
        self.NdFile.atoms_xyz(r, theta, phi)
        os.system("mv atoms.xyz OUTFILE/")

    def scf_input(self, run_n=1, spinType='GeneralSpin', BasisFile="../../../../PBE_BASIS",
                       mixingMethod='realRho', mixing_rate=0.005, step=200, 
                       basis='PBE', precision='Double', convergeVal='1e-6',
                       LeadRun=False, LeadSetup=('x', 0.00, None), DonatorPath='../run2'):
        
        MKdir("OUTFILE/1run", rm=True)
        self.run_n = run_n

        def General():
            with open('OUTFILE/1run/scf.input', 'w') as W_File:
                lines=[
                '## Descriptive name for the system\n',
               f'system.name = {self.type}\n',
                '\n',
                '## Format for input and output of information\n',
                'calculation.control.energyUnit = eV\n',
                'calculation.control.lengthUnit = angstrom\n',
                'calculation.name = scf\n',
                '\n'
                ]
                W_File.writelines(lines)

        def QuantimMechanics(basis, spinType, BasisFile):
            if basis=='PBE':
                Excorre = 'GGA_PBE96'
            elif basis=='LDA':
                Excorre = 'LDA_PZ81'

            with open('OUTFILE/1run/scf.input', 'a') as A_File:
                lines=[
                    '## Quantum mechanical description\n',
                    f'system.spinType = {spinType}\n',
                    f'system.orbitalType = TM_{basis}_DZP\n',
                    # f'system.orbitalType = {basis}-DZP\n',
                    # f'system.orbitalType = {basis}-DZP_new\n',
                    f'calculation.xcFunctional.Type = {Excorre}\n',
                    f'system.neutralAtomDataDirectory = {BasisFile}\n',
                    'calculation.spinOrbitInteraction.isIncluded = true\n',
                    '\n' 
                ]
                A_File.writelines(lines)

        def LatticeConstant():
            a_vec, b_vec, c_vec = self.a_vec, self.b_vec, self.c_vec
            with open('OUTFILE/1run/scf.input', 'a') as A_File:
                lines=[
                    '# Positions and chemical species of the atoms\n',
                    f'system.centralCellVector1 = [{np.round(a_vec[0], 15):<019}, {np.round(a_vec[1], 15):<020},  {np.round(a_vec[2], 15):<019}]\n',
                    f'system.centralCellVector2 = [{np.round(b_vec[0], 15):<019},  {np.round(b_vec[1], 15):<019},  {np.round(b_vec[2], 15):<019}]\n',
                    f'system.centralCellVector3 = [{np.round(c_vec[0], 15):<019},  {np.round(c_vec[1], 15):<019}, {np.round(c_vec[2], 15):<020}]\n',
                    'system.atomCoordinateFormat = cartesian\n',
                    'system.atomFile = ../atoms.xyz\n',
                    '\n',
                ]
                A_File.writelines(lines)

        def LeadImport(direction, Voltage, Path):
            if direction=='x':
                Lead1='front'
                Lead2='back'
            elif direction=='z':
                Lead1='left'
                Lead2='Right'
            elif direction=='y':
                Lead1='bottom'
                Lead2='top'

            with open("OUTFILE/1run/scf.input", 'a') as A_File:
                lines=[
                    '# Description of leads\n',
                    'system.numberOfLeads = 2\n',
                   f'system.typeOfLead1 = {Lead1}\n',
                   f'system.voltageOfLead1 = {Voltage/2:.3f}\n',
                   f'system.objectOfLead1 = {Path}/NanodcalObject.mat\n',
                   f'system.typeOfLead2 = {Lead2}\n',
                   f'system.voltageOfLead2 = {-Voltage/2:.3f}\n',
                   f'system.objectOfLead2 = {Path}/NanodcalObject.mat\n',
                   '\n'
                ]
                A_File.writelines(lines)

        def Accuracy(precision):
            if precision=='Double':
                pre_list='calculation.realspacegrids.E_cutoff = 300 Hartree\n' +  'calculation.k_spacegrids.L_cutoff = 160 Bohr\n'
            if precision=='High':
                pre_list='#calculation.realspacegrids.E_cutoff = 300 Hartree\n' +  '#calculation.k_spacegrids.L_cutoff = 160 Bohr\n'
            with open('OUTFILE/1run/scf.input', 'a') as A_File:
                lines=[
                    '## Accuracy of the calculation\n',
                    'calculation.control.precision = high\n',
                    pre_list,
                    '#calculation.occupationFunction.temperature = 0\n',
                    '\n',
                ]
                A_File.writelines(lines)

        def ForRunn(run_n):
            with open('OUTFILE/1run/scf.input', 'w') as W_File:
                lines=[
                    '# Include information from original file\n'
                   f'&includefile = ../{run_n-1}run/scf.input\n'
                    '\n'
                ]
                W_File.writelines(lines)

        def ConvergeAlgor(mixingMethod, mixing_rate, step, convergeVal):
            with open('OUTFILE/1run/scf.input', 'a') as A_File:
                lines=[    
                     '## Speed of convergence of the algorithms\n',
                    f'calculation.SCF.startingMode = {mixingMethod}\n',
                    f'calculation.SCF.mixingMode = {mixingMethod}\n',
                     'calculation.SCF.mixMethod = Pulay\n',
                    f'calculation.SCF.mixRate = {mixing_rate}\n',
                    f'calculation.SCF.maximumSteps = {step}\n',
                     'calculation.SCF.monitoredVariableName = {\'realSpaceRho\',\'hMatrix\',\'rhoMatrix\',\'totalEnergy\',\'bandEnergy\',\'gridCharge\',\'orbitalCharge\',\'spinPolar\'}\n',
                    f'calculation.SCF.convergenceCriteria = {{{convergeVal}, {convergeVal}, {convergeVal}, {convergeVal}, [],[],[],[]}}\n',
                ]
                A_File.writelines(lines)

        def Donator(Path):
            with open('OUTFILE/1run/scf.input', 'a') as A_File:
                lines=[    
                    f'calculation.SCF.donatorObject = {Path}/NanodcalObject.mat\n'
                ]
                A_File.writelines(lines)
    # ==============================================
        if run_n == 1:
            General()
            QuantimMechanics(basis, spinType, BasisFile)
            LatticeConstant()
            
            if LeadRun:
                LeadImport(LeadSetup[0], LeadSetup[1], LeadSetup[2])
            else:
                pass
            Accuracy(precision)
            ConvergeAlgor(mixingMethod, mixing_rate, step, convergeVal)
            
            if LeadRun:
                if DonatorPath==None:
                    pass
                else:
                    Donator(Path=DonatorPath)
            else:
                pass

        else:
            ForRunn(run_n)
            ConvergeAlgor(mixingMethod, mixing_rate, step, convergeVal)
            if LeadRun:
                Donator(Path=DonatorPath)
            else:
                Donator(Path=f"../{int(run_n-1)}run")
        
        with open('OUTFILE/1run/scf.input', 'a') as A_File:
            lines=[    
                '\n'
            ]
            A_File.writelines(lines)

    def scf_input_bulk(self):
        pass
    
    def LDA_BASIS(self):
        os.system('rm -r ../LDA_BASIS')
        os.system('mkdir ../LDA_BASIS')
        for atom in self.atom:
            if os.path.isdir("/home/lise1020"):
                os.system(f'cp /home/lise1020/labstt/share/nanodcal_basis/5_nano_tm_lda/{atom}_TM_LDA_DZP/{atom}_TM_LDA_DZP.mat ../LDA_BASIS')
            else:
                os.system(f'cp /home/share/nanodcal_basis/5_nano_tm_lda/{atom}_TM_LDA_DZP/{atom}_TM_LDA_DZP.mat ../LDA_BASIS')
    
    def PBE_BASIS(self):
        os.system('rm -r ../PBE_BASIS')
        os.system('mkdir ../PBE_BASIS')
        for atom in self.atom:
            if os.path.isdir("/home/lise1020"):
                os.system(f'cp /home/lise1020/labstt/share/nanodcal_basis/5_nano_tm_pbe/{atom}_TM_PBE_DZP/{atom}_TM_PBE_DZP.mat ../PBE_BASIS')
            else:
                os.system(f'cp /home/share/nanodcal_basis/5_nano_tm_pbe/{atom}_TM_PBE_DZP/{atom}_TM_PBE_DZP.mat ../PBE_BASIS')

    def ndpbs(self, name, mechine, ppn):
        with open(f'OUTFILE/{self.run_n}run/nanodcal.pbs', 'w') as W_File:
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

    def ndsh(self, name, mechine, ppn):
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

if __name__ == '__main__':

    MKdir('OUTFILE', rm=True)

    layer      = 2
    atom_type  = f'Pd6Co{layer}'
    readPath = f'../../1_relax_examp/2_relax2/{layer}_{atom_type}_f/POSCAR'
    
    test_nanod = Nd_MakingFile(File = readPath, atom_type = atom_type)

    # PBE_BASIS
    test_nanod.PBE_BASIS()

    MKdir(f'{layer}_{atom_type}_f', rm='False')
    for theta in [0, 45, 90]:
        
        MKdir(f'{layer}_{atom_type}_f/{theta:>003}_theta', rm='True')
        
        # atom.xyz
        test_nanod.atoms_xyz(r=(1, 3), theta=theta, phi=0)

        # scf.input
        test_nanod.scf_input(run_n=1, spinType='GeneralSpin', BasisFile='../../../../PBE_BASIS',
                            mixingMethod='realRho', mixing_rate=0.005, step=600, 
                            basis='PBE', 
                            precision='High',
                            convergeVal='1e-6',
                            LeadRun=False, LeadSetup=('x', 0.00, None), DonatorPath='../run2',
                            )
        
        # nanodcal.pbs
        name = f"{atom_type}_{theta:>003}_SL_wSOC_scf"
        mechine = "dl0x"
        ppn = "20"
        test_nanod.ndpbs(
                    name = name,
                    mechine = mechine,
                    ppn = ppn
                    )

        os.system(f'mv OUTFILE/* {layer}_{atom_type}_f/{theta:>003}_theta')

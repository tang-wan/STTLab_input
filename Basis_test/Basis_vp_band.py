import numpy as np # type: ignore
import os
import sys
# ========================================================
sys.path.append('/home/tangtang89/Example_Lab/')
from Tools import MKdir, Check_out_Word, Process_Word # type: ignore
# ========================================================
class Vp_Basis_Test():
    def __init__(self, basis_type, atom_type, SOC):
        self.basis_type = basis_type
        self.atom_type  = atom_type
        self.info_Path  = f'/home/share/nanodcal_basis/5_nano_tm_{basis_type.lower()}/{atom_type}_TM_{basis_type.upper()}_DZP/dzp'
        self.SOC = SOC

        print()
        Check_out_Word('Inital')
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

    def POSCAR(self, r, theta, phi):
        SOC = self.SOC
        basis_type = self.basis_type
        atom_type  = self.atom_type

        Check_out_Word(f'Making subfolder')
        if SOC:
            o_target_Path = f'{atom_type}_bulk/{basis_type}_soc_xz{theta}_mz{r:.1f}'
            target_Path = f'{atom_type}_bulk/{basis_type}_soc_xz{theta}_mz{r:.1f}_band'
        else:
            o_target_Path = f'{atom_type}_bulk/{basis_type}_ncl_xz{theta}_mz{r:.1f}'
            target_Path = f'{atom_type}_bulk/{basis_type}_ncl_xz{theta}_mz{r:.1f}_band'
        MKdir(f'{target_Path}', rm=False)
        print()
        
        self.target_Path = target_Path
        self.o_target_Path = o_target_Path
        
        Check_out_Word(f'Making POSCAR')
        MKdir(f'{target_Path}/preKPOINTS', rm=False)
        print()
        os.system(f'cp {o_target_Path}/CONTCAR {target_Path}/POSCAR')
        os.system(f'cp {o_target_Path}/CONTCAR {target_Path}/preKPOINTS/POSCAR')

    def POTCAR(self):
        target_Path = self.target_Path
        o_target_Path = self.o_target_Path
        Check_out_Word(f'Making POTCAR')
        print()
        os.system(f'cp {o_target_Path}/POTCAR {target_Path}/POTCAR')
        os.system(f'cp {o_target_Path}/POTCAR {target_Path}/preKPOINTS/POTCAR')
    
    def CHGCAR(self):
        target_Path = self.target_Path
        o_target_Path = self.o_target_Path
        Check_out_Word(f'Making CHGCAR')
        print()
        os.system(f'cp {o_target_Path}/CHGCAR {target_Path}/CHGCAR')

    def INCAR(self, KPAR, NPAR, moment, moment_list):
        SOC = self.SOC
        atomLabel   = self.atomLabel
        basis_type  = self.basis_type
        atom_type   = self.atom_type
        atom_num    = int(atomLabel[0][0:-1])
        target_Path = self.target_Path
        Check_out_Word(f'Making INCAR')

        if SOC == True:
            Process_Word('With SOC')
            com = ''
        elif SOC == False:
            Process_Word('Without SOC')
            com = '#'
            # MAG_str = ""
            # for i, j in [[atom_num, moment]]:
            #     MAG_str = MAG_str + f'{int(i)}*{j} '
        print()
        theta  = moment_list[0]
        phi    = moment_list[1]
        mx1    = moment*np.sin(theta*np.pi/180)*np.cos(phi)
        my1    = moment*np.sin(theta*np.pi/180)*np.sin(phi)
        mz1    = moment*np.cos(theta*np.pi/180)

        MAG_str = ""
        for i in range(atom_num):
            if i == 0:
                MAG_str = MAG_str + f'{mx1:.3f} {my1:.3f} {mz1:.3f} \\' + '\n'
            else:
                MAG_str = MAG_str + '\t'*1 + f'{mx1:.3f} {my1:.3f} {mz1:.3f} \\' + '\n'
        
        #-------------------------------------------------------             
        lines = [
            f"System = {atom_type} bulk\n",
            '\n',
            "#--------------------------------------\n",
            "# Parallelization\n",
            f"KPAR     = {KPAR}        # Number of workers for k-points parallelization\n",
            f"NPAR     = {NPAR}        # Number of workers for bands parallelization\n",
            '\n',
            "# Start parameters for this Run\n",
            "ISTART   = 0        # Job: 0-new 1-WAVECAR 2-samecut\n",
            "ICHARG   = 11       # Initial charge density: 1-CHGCAR 2-atom 11-band/DOS\n",
            '\n',
            "# Output files\n",
            "LWAVE    = .FALSE.  # Write WAVECAR\n",
            "LORBIT   = 11       # Write DOSCAR and lm-decomposed PROCAR\n",
            '\n',
            "# Magnetism\n",
            "ISPIN    = 2        # Spin polarize: 1-No 2-Yes\n",
            f"MAGMOM   = {MAG_str}\n",
            '\n',
            "#--------------------------------------\n",
            "# Electronic relaxation (ESC)\n",
            "NELM     = 200      # Max number of ESC steps\n",
            "EDIFF    = 1e-8     # Stopping criteria for ESC in eV (1e-6 or 1e-8)\n",
            "ENCUT    = 500      # Kinetic energy cutoff in eV (>500)\n",
            "PREC     = Accurate # Precision: Normal or Accurate\n",
            "ISMEAR   = 0        # Partial occupancies f_nk (0 for others or -5 for DOS)\n",
            "SIGMA    = 0.03     # Width of the smearing in eV (0.03~0.05)\n",
            '\n',
            "#--------------------------------------\n",
            "# Spin-orbit coupling\n",
            f"{com}LSORBIT  = .TRUE.\n",
            f"{com}LMAXMIX  = 4\n",
            f"{com}NBANDS   = 100\n",
            f"{com}ISYM     = 0\n",
            '\n',
            "#--------------------------------------\n",
            "# Mixer\n",
            "AMIX     = 0.2\n",
            "BMIX     = 0.00001\n",
            "AMIX_MAG = 0.8\n",
            "BMIX_MAG = 0.00001\n",
            "\n",
            "LNONCOLLINEAR = T\n",
        ]
        with open(f'{target_Path}/INCAR', 'w') as W_File:
            W_File.writelines(lines)

    def OLD_KPOINTS(self):
        Check_out_Word('Making KPOINTS')
        target_Path = self.target_Path
        if os.path.isfile(f'{target_Path}/preKPOINTS/KPATH.in'):
            Process_Word('Coping KPOINTS...')
            print()
            os.system(f'cp {target_Path}/preKPOINTS/KPATH.in {target_Path}/KPOINTS')
        else:
            Process_Word('Please run vaspkit 303 first')
            print()
            os._exit(0)
    
    def KPOINTS(self):
        target_Path = self.target_Path
        MKdir(f"{target_Path}/preKPOINTS/", rm=True)
        os.system(f"mv {target_Path}/* {target_Path}/preKPOINTS/.")
        os.system(f"cp {target_Path}/preKPOINTS/POSCAR {target_Path}/preKPOINTS/POTCAR {target_Path}/.")
        HomePath = os.getcwd()
        os.chdir(f"{target_Path}/preKPOINTS/")
        os.system("vaspkit -task 303")
        os.chdir(f"{HomePath}")
        os.system(f'cp {target_Path}/preKPOINTS/KPATH.in {target_Path}/KPOINTS')
        
    def vasppbs(self, mechine, ppn):
        Check_out_Word('Making vasp6.pbs')
        atom_type = self.atom_type
        SOC = self.SOC
        target_Path = self.target_Path

        if SOC:
            name = f"{atom_type}_socBand_basisTest"
        else:
            name = f"{atom_type}_nclBand_basisTest"

        print()

        with open(f'{target_Path}/vasp6.pbs', 'w') as File:
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
            f'mpirun vasp_ncl\n'
            ]
            File.writelines(lines)
    
    def QSUB(self):

        target_Path = self.target_Path

        Check_out_Word('Submit the Job')
        os.chdir(f'{target_Path}')

        judge = 0
        for file in ['POSCAR', 'POTCAR', 'INCAR', 'KPOINTS', 'vasp6.pbs']:
            if os.path.isfile(f'{file}'):
                Process_Word(f'{file:^10} is exit !!')
                judge = judge + 1
            else:
                Process_Word(f'{file:^10} is NOT exit !!')
        
        if judge==5:
            os.system('qsub vasp6.pbs')
        else:
            Process_Word('REFUSE THIS SUCK JOB')
        os.chdir('../../')
        print()

if __name__ == '__main__':
    # ----------
    basis    = 'PBE'
    atom     = 'Pt'
    SOC      = False

    spec_atom = Vp_Basis_Test(
                            basis_type = basis,
                            atom_type  = atom,
                            SOC        = SOC
                            )
    spec_atom.Read_info(
                # printTrue=False
                )
    spec_atom.POSCAR(r=0.0, theta=0, phi=0, 
                    type='Frac')
    spec_atom.POTCAR()
    spec_atom.KPOINTS()
    spec_atom.INCAR(KPAR=2, NPAR=5, moment=0.5, moment_list=[0, 0])
    spec_atom.vasppbs(mechine='dl1x', ppn=20)
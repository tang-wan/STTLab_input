import numpy as np # type: ignore
import os
import glob
from colorama import init, Fore, Back # type: ignore
# ========================================================
def Check_out_Word(word: str):
    print(Back.RED + word + Back.RESET)

def Process_Word(word: str):
    print(Fore.YELLOW, word , Fore.RESET)

def MKdir(path, rm):
    if os.path.isdir(path) and rm:
        Process_Word(f'{path} is exist, Removing')
        os.system(f'rm -r {path}')
        Process_Word(f'Making {path}')
        os.mkdir(path)
    elif os.path.isdir(path) and not(rm):
        Process_Word(f'{path} is exist')
        pass
    else:
        Process_Word(f'{path} is NOT exist')
        Process_Word(f'Making {path}')
        os.mkdir(path)
# ========================================================
class Vp_Basis_Test():
    def __init__(self, basis_type, atom_type, SOC):
        self.basis_type = basis_type
        self.atom_type  = atom_type
        self.info_Path  = f'/home/share/nanodcal_basis/5_nano_tm_{basis_type.lower()}/{atom_type}_TM_{basis_type.upper()}_DZP/dzp'
        self.SOC = SOC

        print()
        Check_out_Word('Inital')
        MKdir(f'{atom_type}_bulk', rm=False)
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

    def POSCAR(self, r, theta, phi, type='Frac'):
        SOC = self.SOC
        basis_type = self.basis_type
        atom_type  = self.atom_type
        
        a_vec = np.array(self.a_vec)
        b_vec = np.array(self.b_vec)
        c_vec = np.array(self.c_vec)

        Check_out_Word(f'Making subfolder')
        if SOC:
            target_Path = f'{atom_type}_bulk/{basis_type}_soc_xz{theta}_mz{r}'
        else:
            target_Path = f'{atom_type}_bulk/{basis_type}_ncl_xz{theta}_mz{r}'
        MKdir(f'{target_Path}', rm=True)
        print()
        self.target_Path = target_Path

        atomPosition = self.atomPosition
        atomLabel = self.atomLabel
        atom_num = atomLabel[0][0:-1]

        Check_out_Word(f'Making POSCAR')
        content_list = []
        content_list.append(f'{atom_type} bulk')
        content_list.append(f"{'1.000':>8}")
        content_list.append(f'     {a_vec[0]:<07}   {a_vec[1]:<07}   {a_vec[2]:<07}')
        content_list.append(f'     {b_vec[0]:<07}   {b_vec[1]:<07}   {b_vec[2]:<07}')
        content_list.append(f'     {c_vec[0]:<07}   {c_vec[1]:<07}   {c_vec[2]:<07}')
        content_list.append(f'   {atom_type}')
        content_list.append(f'   {atom_num}')
        content_list.append('Direct')
        for atom_cont in atomPosition:
            sp_atomPosition = atom_cont[:-1:].split()

            label = sp_atomPosition[0]
            Position_frac_list = sp_atomPosition[1:]
            Position_Cart_list = list(float(Position_frac_list[0])*a_vec + 
                                        float(Position_frac_list[1])*b_vec + 
                                        float(Position_frac_list[2])*c_vec)
            Position_frac_list = list(float(Position_frac_list[0])*np.array([1, 0, 0]) + 
                                        float(Position_frac_list[1])*np.array([0, 1, 0]) + 
                                        float(Position_frac_list[2])*np.array([0, 0, 1]))
            new_atom_list = []
            new_atom_list.append(label)
            if type=='Cart':
                new_atom_list.extend(Position_Cart_list)
            elif type=='Frac':
                new_atom_list.extend(Position_frac_list)

            # new_atom_str = f"{new_atom_list[0]:>8}  {new_atom_list[1]:<021}  {new_atom_list[2]:<021}  {new_atom_list[3]:<021}"
            new_atom_str = f"  {new_atom_list[1]:<08}  {new_atom_list[2]:<08}  {new_atom_list[3]:<08}"

            atom_cont = new_atom_str
            content_list.append(atom_cont)
        
        Process_Word(f'Making {target_Path}/POSCAR ({type})')
        print()
        with open(f'{target_Path}/POSCAR', 'w') as W_File:
            for line in content_list:
                W_File.writelines(line + '\n')

    def POTCAR(self):
        target_Path = self.target_Path
        basis_type = self.basis_type
        Check_out_Word(f'Making POTCAR')
        if os.path.isdir('/home/lise1020/labstt/share/vasp_potentials/'):
            Process_Word('At T3, coping...')
            type = self.atom_type
            os.system(f"cat /home/lise1020/labstt/share/vasp_potentials/potpaw_{basis_type}.54/{type}/POTCAR >> {target_Path}/POTCAR")
        elif os.path.isdir('/home/share/vasp_potentials'):
            Process_Word('At STT, coping...')
            type = self.atom_type
            os.system(f"cat /home/share/vasp_potentials/potpaw_{basis_type}.54/{type}/POTCAR >> {target_Path}/POTCAR")
            
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
            # MAG_str = ""
            # for i, j in [[atom_num, moment]]:
            #     MAG_str = MAG_str + f'{int(i)}*{j} '
            com = '#'
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
            "ICHARG   = 2       # Initial charge density: 1-CHGCAR 2-atom 11-band/DOS\n",
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

    def KPOINTS(self):
        Check_out_Word('Making KPOINTS')
        print()
        target_Path = self.target_Path
        lines = [
            "K-Spacing Value to Generate K-Mesh: 0.020\n",
            "0\n",
            "Monkhorst-Pack\n",
            "  13  13  13\n",
            "0.0  0.0  0.0\n",
        ]
        with open(f'{target_Path}/KPOINTS', 'w') as W_File:
            W_File.writelines(lines)
        
    def vasppbs(self, mechine, ppn):
        Check_out_Word('Making vasp6.pbs')
        atom_type = self.atom_type
        SOC = self.SOC
        target_Path = self.target_Path
        basis_type = self.basis_type

        if SOC:
            name = f"{atom_type}_{basis_type}_SOC_basisTest"
        else:
            name = f"{atom_type}_{basis_type}_ncl_basisTest"

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
    spec_atom.vasppbs(mechine='dl1x', ppn=40)
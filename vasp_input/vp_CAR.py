import numpy as np # type: ignore
import os
import re
import sys
# ========================================================
sys.path.append('/home/tangtang89/Example_Lab/')
from Tools import MKdir, Check_out_Word, Process_Word # type: ignore
# ========================================================

class AUTOsub():
    def __init__(self, atom_type):
        self.type    = atom_type
        
        # atom type in str
        self.atom_st          = re.sub(u'([^\u0041-\u007a])', ' ', atom_type)
        # atom type in lsit
        self.atom             = self.atom_st.split()
        
        # atom number in str
        self.atom_num_st      = re.sub(u'([^\u0030-\u0039])', ' ', atom_type).replace(" ", "", 1)
        # atom number in list
        self.atom_num         = list(map(int, self.atom_num_st.split()))
        # Total atom number
        self.m                = sum(self.atom_num)
    
    def PdCoPd_Stacking(self):
        pass
    
    def PureThinfilm(self, stacking, LattCon_Coef_list, Dv):
        atom_type   = self.type
        LC_list     = LattCon_Coef_list
        atom_st     = self.atom_st 
        atom        = self.atom    
        atom_num_st = self.atom_num_st 
        atom_num    = self.atom_num    
        m           = self.m
        
        print(atom_type)
        print(m)
        print(atom, atom_num)
        print(LC_list)
        
        match stacking: # type: ignore
            case "FCC(111)":
                
                print("\nNow is FCCtoHCP")

                Substrate_LattiCon_c = (np.sqrt(6)/3)*(m-1) + Dv/LC_list[0]
                # print(Substrate_LattiCon_c)
                # print(Substrate_LattiCon_c*LC_list[0])
                a1x = str(np.sqrt(3)/2)
                a1y = str(-1/2)
                a2x = str(np.sqrt(3)/2)
                a2y = str(1/2)
                with open('OUTFILE/POSCAR', 'w') as ini_POSCAR:
                    lines = [
                        f'{atom_type}\n',
                        f'{LC_list[0]}\n',
                        f'    {a1x:<019}  { a1y:<020}  {0.0:<019}\n',
                        f'    {a2x:<019}   {a2y:<019}  {0.0:<019}\n',
                        f'    {0.0:<019}   {0.0:<019}  {Substrate_LattiCon_c:<019}\n',
                        f'{atom_st}\n',
                        f'{atom_num_st}\n',
                        'Direct\n'
                    ]
                    ini_POSCAR.writelines(lines)

                
                # making atom type and lattice constant list
                LC_for_array = np.array([])
                ## [2.753230221, 2.753230221... , 2.467884734, 2.467884734...]
                atom_array   = np.array([])
                ## ['Pd', 'Pd', 'Pd', 'Pd', 'Pd', 'Pd', 'Co', 'Co'...]
                
                for i, a in enumerate(atom_num):
                    repeat_num = a
                    for _ in range(repeat_num):
                        LC_for_array = np.append(LC_for_array, LC_list[i])
                        atom_array   = np.append(atom_array, atom[i])

                # print(LC_for_array)
                # print(atom_array)

                tot_c = 0
                tot_c_array = np.array([])
                for LC_ in LC_for_array:
                    LattiCon_c = (np.sqrt(6)/3)*(m-1) + Dv/LC_
                    delta_c = np.sqrt(6)/(3*LattiCon_c)
                    
                    # Cartesian coord. layer gap
                    delta = delta_c*(LattiCon_c*LC_) # LattCon by using different a (Pd/Pt or Co)
                    #---------
                    # Fractional coord. layer gap
                    delta_c = delta/(Substrate_LattiCon_c*LC_list[0]) # LattCon by using basis a (Pd/Pt)
                    #==========
                    tot_c = tot_c + delta_c
                    tot_c_array = np.append(tot_c_array, tot_c)
                tot_c_array_shifted = 0.5-np.mean(tot_c_array)
                
                A = f'    {0.0:<019}    {0.0:<019}    '
                B = f'    {2/3:<019}    {2/3:<019}    '
                C = f'    {1/3:<019}    {1/3:<019}    '

                for m_index, tot_c in np.c_[range(m), tot_c_array]:
                    
                    m_index = int(m_index)
                    a3_ampli = str(round(tot_c + tot_c_array_shifted, 18))
                    
                    if (m_index%3 == 0):
                        print('C', end=' ')
                        site = [A + f'{a3_ampli:<019}    {atom_array[m_index]}\n']
                    elif (m_index%3 == 1):
                        print('B', end=' ')
                        site = [B + f'{a3_ampli:<019}    {atom_array[m_index]}\n']
                    elif (m_index%3 == 2):
                        print('A', end=' ')
                        site = [C + f'{a3_ampli:<019}    {atom_array[m_index]}\n']
                    else:
                        print('ERROR')

                    with open('OUTFILE/POSCAR', 'a') as a_POSCAR:
                        a_POSCAR.write(site[0])
        
            case "HCP":
                print("\nNow is HCP")

                Substrate_LattiCon_c = (np.sqrt(6)/3)*(m-1) + Dv/LC_list[0]
                # print(Substrate_LattiCon_c)
                # print(Substrate_LattiCon_c*LC_list[0])
                a1x = str(np.sqrt(3)/2)
                a1y = str(-1/2)
                a2x = str(np.sqrt(3)/2)
                a2y = str(1/2)
                with open('OUTFILE/POSCAR', 'w') as ini_POSCAR:
                    lines = [
                        f'{atom_type}\n',
                        f'{LC_list[0]}\n',
                        f'    {a1x:<019}  { a1y:<020}  {0.0:<019}\n',
                        f'    {a2x:<019}   {a2y:<019}  {0.0:<019}\n',
                        f'    {0.0:<019}   {0.0:<019}  {Substrate_LattiCon_c:<019}\n',
                        f'{atom_st}\n',
                        f'{atom_num_st}\n',
                        'Direct\n'
                    ]
                    ini_POSCAR.writelines(lines)

                
                # making atom type and lattice constant list
                LC_for_array = np.array([])
                ## [2.753230221, 2.753230221... , 2.467884734, 2.467884734...]
                atom_array   = np.array([])
                ## ['Pd', 'Pd', 'Pd', 'Pd', 'Pd', 'Pd', 'Co', 'Co'...]
                
                for i, a in enumerate(atom_num):
                    repeat_num = a
                    for _ in range(repeat_num):
                        LC_for_array = np.append(LC_for_array, LC_list[i])
                        atom_array   = np.append(atom_array, atom[i])

                # print(LC_for_array)
                # print(atom_array)

                tot_c = 0
                tot_c_array = np.array([])
                for LC_ in LC_for_array:
                    LattiCon_c = (np.sqrt(6)/3)*(m-1) + Dv/LC_
                    delta_c = np.sqrt(6)/(3*LattiCon_c)
                    
                    # Cartesian coord. layer gap
                    delta = delta_c*(LattiCon_c*LC_) # LattCon by using different a (Pd/Pt or Co)
                    #---------
                    # Fractional coord. layer gap
                    delta_c = delta/(Substrate_LattiCon_c*LC_list[0]) # LattCon by using basis a (Pd/Pt)
                    #==========
                    tot_c = tot_c + delta_c
                    tot_c_array = np.append(tot_c_array, tot_c)
                tot_c_array_shifted = 0.5-np.mean(tot_c_array)
                
                A = f'    {0.0:<019}    {0.0:<019}    '
                B = f'    {2/3:<019}    {2/3:<019}    '
                C = f'    {1/3:<019}    {1/3:<019}    '

                for m_index, tot_c in np.c_[range(m), tot_c_array]:
                    
                    m_index = int(m_index)
                    a3_ampli = str(round(tot_c + tot_c_array_shifted, 18))

                    if m_index%2 == 0:
                        print('A', end=' ')
                        site = [A + f'{a3_ampli:<019}    {atom_array[m_index]}\n']
                    elif m_index%2 == 1:
                        print('B', end=' ')
                        site = [B + f'{a3_ampli:<019}    {atom_array[m_index]}\n']
                    else:
                        print('ERROR')

                    with open('OUTFILE/POSCAR', 'a') as a_POSCAR:
                        a_POSCAR.write(site[0])

            case "BCC(001)":
                
                print("\nNow is BCC")

                Substrate_LattiCon_c = Dv/LC_list[0] + (m-1)

                a1x = str(1.0)
                a2y = str(1.0)
                with open('OUTFILE/POSCAR', 'w') as ini_POSCAR:
                    lines = [
                        f'{atom_type}\n',
                        f'{LC_list[0]}\n',
                        f'    {a1x:<019}   {0.0:<019}  {0.0:<019}\n',
                        f'    {0.0:<019}   {a2y:<019}  {0.0:<019}\n',
                        f'    {0.0:<019}   {0.0:<019}  {Substrate_LattiCon_c:<019}\n',
                        f'{atom_st}\n',
                        f'{atom_num_st}\n',
                        'Direct\n'
                    ]
                    ini_POSCAR.writelines(lines)

                
                # making atom type and lattice constant list
                LC_for_array = np.array([])
                ## [2.753230221, 2.753230221... , 2.467884734, 2.467884734...]
                atom_array   = np.array([])
                ## ['Pd', 'Pd', 'Pd', 'Pd', 'Pd', 'Pd', 'Co', 'Co'...]
                
                for i, a in enumerate(atom_num):
                    repeat_num = a
                    for _ in range(repeat_num):
                        LC_for_array = np.append(LC_for_array, LC_list[i])
                        atom_array   = np.append(atom_array, atom[i])

                # print(LC_for_array)
                # print(atom_array)

                tot_c = 0
                tot_c_array = np.array([])
                for LC_ in LC_for_array:
                    LattiCon_c = (m-1) + Dv/LC_
                    delta_c = 1/(2*LattiCon_c)
                    
                    # Cartesian coord. layer gap
                    delta = delta_c*(LattiCon_c*LC_) # LattCon by using different a (Pd/Pt or Co)
                    #---------
                    # Fractional coord. layer gap
                    delta_c = delta/(Substrate_LattiCon_c*LC_list[0]) # LattCon by using basis a (Pd/Pt)
                    #==========
                    tot_c = tot_c + delta_c
                    tot_c_array = np.append(tot_c_array, tot_c)
                tot_c_array_shifted = 0.5-np.mean(tot_c_array)
                
                A   = f'    {0.0:<019}    {0.0:<019}    '
                Cen = f'    {0.5:<019}    {0.5:<019}    '

                for m_index, tot_c in np.c_[range(m), tot_c_array]:
                    
                    m_index = int(m_index)
                    a3_ampli = str(round(tot_c + tot_c_array_shifted, 18))
                    
                    if (m_index%2 == 0):
                        print('A', end=' ')
                        site = [A + f'{a3_ampli:<019}    {atom_array[m_index]}\n']
                    elif (m_index%2 == 1):
                        print('Cen', end=' ')
                        site = [Cen + f'{a3_ampli:<019}    {atom_array[m_index]}\n']
                    else:
                        print('ERROR')

                    with open('OUTFILE/POSCAR', 'a') as a_POSCAR:
                        a_POSCAR.write(site[0])

        print()
        
    def POTCAR(self, PT_type='PBE', where='STT'):
        if os.path.isfile("./OUTFILE/POTCAR"):
            # print('yes')
            os.system("rm ./OUTFILE/POTCAR")
        else:
            # print('No')
            pass
        
        Check_out_Word('Making POTCAR')
        Process_Word(f'POTCAR configuration: {PT_type}   {where}')
        
        match where: # type: ignore
            case 'STT':
                for type in self.atom:
                    os.system(f"cat /home/share/vasp_potentials/potpaw_{PT_type}.54/{type}/POTCAR >> OUTFILE/POTCAR")
            case 'T3':
                for type in self.atom:
                    os.system(f"cat  /home/lise1020/labstt/share/vasp_potentials/potpaw_{PT_type}.54/{type}/POTCAR >> OUTFILE/POTCAR")

    def INCAR(self, KPAR, NPAR, moment,
              vasp_type='relax', Lattice=True, VeryFast=False,
              SOC=False, band_num=100, constrain_list=None,
              moment_list=None,
              vdw_gap=False
              ):
        
        type = self.type
        atom_num = self.atom_num
        constrain_con = constrain_list[0]
        constrain_num = constrain_list[1]
        constrain_lam = constrain_list[2]
        
        if VeryFast:
            VeryFast_str = '  ALGO     = VeryFast\n'
        else:
            VeryFast_str = '\n'

        def General(ICHARG):
            with open('OUTFILE/INCAR', 'w') as File:
                lines = [f'System = {type}\n',
                        '\n',
                        '# Parallelization\n',
                    f'  KPAR     = {KPAR}\n',
                    f'  NPAR     = {NPAR}\n',
                        '\n',
                        '# General\n',
                        '  ISTART   = 0        # Job: 0-new  1-cont  2-samecut\n',
                        # '  ISYM     = 0        # Symmetry 0-turn off\n',
                    
                       f'  ICHARG   = {ICHARG}        # initial charge density: 1-file 2-atom 10-cons 11-DOS\n',
                        '  LWAVE    = FALSE.   # write WAVECAR\n',
                        '  LORBIT   = 11       # Write DOSCAR and lm-decomposed PROCAR\n',
                        '  LORBMOM  = TRUE.    # Orbital Moment\n',
                        VeryFast_str,
                        '\n',]
                File.writelines(lines)

        def Magnetism(SOC, band_num):
            if SOC == "soc" or SOC == "ncl" :
                MAG_str = ""
                for ind in range(len(moment)):
                    theta  = moment_list[ind][0]
                    phi    = moment_list[ind][1]
                    mx1    = moment[ind]*np.sin(theta*np.pi/180)*np.cos(phi)
                    my1    = moment[ind]*np.sin(theta*np.pi/180)*np.sin(phi)
                    mz1    = moment[ind]*np.cos(theta*np.pi/180)

                    for _ in range(atom_num[ind]):
                        if ind == 0:
                            MAG_str = MAG_str + f'{mx1:.3f} {my1:.3f} {mz1:.3f} \\' + '\n'
                        else:
                            MAG_str = MAG_str + '\t'*2 + f'{mx1:.3f} {my1:.3f} {mz1:.3f} \\' + '\n'

                    if constrain_con:
                        con_str = f"  I_CONSTRAINED_M = {constrain_num}  # Desired direction of the magnetic moment: 1-direction 2-direction & amplitude\n" + f"  LAMBDA    = {constrain_lam}\n" + f"  M_CONSTR  = {MAG_str}"
                    else:
                        con_str = ""
                    
            #-------------------------------------------------------
                match SOC:
                    # ==============================================
                    case "soc":
                        with open('OUTFILE/INCAR', 'a') as File:
                            lines = [
                                '# Magnetism\n',
                                '  ISPIN    = 2        # Spin polarize: 1-No 2-Yes\n',
                            f'  MAGMOM   = {MAG_str}\n',
                                '# Constraining\n',
                                '  LNONCOLLINEAR = T\n'
                            f'{con_str}'
                                '\n',
                                '# Mixing\n',
                                # '  AMIX      = 0.2\n',
                                '  AMIX      = 0.1\n',
                                '  BMIX      = 0.00001\n',
                                # '  AMIX_MAG  = 0.8\n',
                                '  AMIX_MAG  = 0.2\n',
                                '  BMIX_MAG  = 0.00001\n',
                                '\n',
                                '# Spin-orbit coupling\n',
                                '  LSORBIT  = .TRUE.\n',
                                '  LMAXMIX  = 4\n',
                               f'  NBANDS   = {band_num}\n',
                                '  ISYM     = 0\n',
                                '\n'
                                ]
                            File.writelines(lines)
                    # ==============================================
                    case "ncl":
                        with open('OUTFILE/INCAR', 'a') as File:
                            lines = [
                                '# Magnetism\n',
                                '  ISPIN    = 2        # Spin polarize: 1-No 2-Yes\n',
                            f'  MAGMOM   = {MAG_str}\n',
                                '# Constraining\n',
                                '  LNONCOLLINEAR = T\n'
                            f'{con_str}'
                                '\n',
                                '# Mixing\n',
                                # '  AMIX      = 0.2\n',
                                '  AMIX      = 0.1\n',
                                '  BMIX      = 0.00001\n',
                                # '  AMIX_MAG  = 0.8\n',
                                '  AMIX_MAG  = 0.2\n',
                                '  BMIX_MAG  = 0.00001\n',
                                '\n',
                                '# Spin-orbit coupling\n',
                                '#  LSORBIT  = .TRUE.\n',
                                '#  LMAXMIX  = 4\n',
                               f'#  NBANDS   = {band_num}\n',
                                '#  ISYM     = 0\n',
                                '\n'
                                ]
                            File.writelines(lines)
                    # ==============================================
                    case _:
                        pass          
            #-------------------------------------------------------
                
            elif SOC == "cl":
                MAG_str = ""
                print(atom_num)
                print(moment)
                for i, j in np.c_[atom_num, moment]:
                    MAG_str = MAG_str + f'{int(i)}*{j} '
            #-------------------------------------------------------
                with open('OUTFILE/INCAR', 'a') as File:
                    lines = [
                            '# Magnetism\n',
                            '  ISPIN    = 2        # Spin polarize: 1-No 2-Yes\n',
                           f'  MAGMOM   = {MAG_str}\n',
                            '\n'
                            ]
                    File.writelines(lines)


        def Precision():
            with open('OUTFILE/INCAR', 'a') as File:
                lines = [
                    '# Precision\n',
                    '  PREC     = Accurate # Options: Normal or Accurate\n',
                    '  ENCUT    = 500      # Kinetic energy cutoff in eV (default = max(ENMAX))\n',
                    '  ISMEAR   = 0        # Partial occupancies for each orbital (check doc to use!)\n',
                    '  SIGMA    = 0.03     # Width of the smearing in eV (0.03~0.05)\n',
                    '\n',
                ]
                File.writelines(lines)

        def EleSC(EDIFF='1e-6', NELM=200):
            with open('OUTFILE/INCAR', 'a') as File:
                lines=[
                    '# Electronic relaxation (ESC)\n',
                   f'  NELM     = {NELM}      # Max number of ESC steps\n',
                   f'  EDIFF    = {EDIFF}     # Stopping criteria for ESC in eV (default = 1e-4)\n',
                    '\n'
                    ]
                File.writelines(lines)

        def IonSC(Lattice, EDIFFG):
            with open('OUTFILE/INCAR', 'a') as File:
                if Lattice:
                    isif = 3
                else:
                    isif = 2 # fix lattice constant
                

                lines=[
                    '# Ionic relaxation (ISC)\n',
                    '  NSW      = 200      # Max number of ISC steps: 0- Single Point\n',
                   f'  EDIFFG   = {EDIFFG}    # Stopping criteria for ISC (default = EDIFF*10)\n',
                    '  IBRION   = 2        # Ionic relaxation method: 1-RMMDISS 2-CG\n',
                   f'  ISIF     = {isif}        # Stress and relaxation: 2-ions 3-all (default = 2)\n',
                    '\n'
                        ]
                File.writelines(lines)

        def Fixing_tensor():
            with open('OUTFILE/INCAR', 'a') as File:
                lines=[
                    '# Fixing specific stress tensor element (xx yx zx xy yy zy xz yz zz)\n',
                    '#  IOPTCELL = 1 1 0 1 1 0 0 0 0 # 0 for vacuumn part\n',
                    '\n',
                    '#  Nonlocal vdW-DF functionals (optB86b-vdW)\n',
                    '   GGA      = MK \n',
                    '   PARAM1   = 0.1234 \n',
                    '   PARAM2   = 1.0\n',
                    '   AGGAC    = 0.0\n',
                    '   LUSE_VDW = .TRUE.\n',
                    '   LASPH    = .TRUE.\n',
                    '\n'
                    ]
                File.writelines(lines)
    
    # ============================================================
        Check_out_Word('Making INCAR')
        Process_Word(f'INCAR configuration: {vasp_type}   {SOC}')

        if vasp_type == 'relax':
            General(ICHARG=2)
            Magnetism(SOC, band_num)
            Precision()
            EleSC(EDIFF='1e-6')
            IonSC(Lattice, EDIFFG='-1e-2')

        elif vasp_type == 'relax2':
            General(ICHARG=1)
            Magnetism(SOC, band_num)
            Precision()
            EleSC(EDIFF='1e-8')
            IonSC(Lattice, EDIFFG='-5e-3')

        elif vasp_type =='scf':
            General(ICHARG=1)
            Magnetism(SOC, band_num)
            Precision()
            EleSC(EDIFF='1e-8', NELM=400)
        
        elif vasp_type == 'band':
            General(ICHARG=11)
            Magnetism(SOC, band_num)
            Precision()
            EleSC(EDIFF='1e-8', NELM=400)
        
        if vdw_gap:
            Fixing_tensor()
        else:
            pass
#----------------------
if __name__ == '__main__':

    # os.system("rm -r *_f")
    if os.path.isdir("./OUTFILE"):
        pass
    else:
        os.system("mkdir OUTFILE")
        
    #----------------------------------------
    ## POSCAR
    layer_num = int(12)
    # atom_type = f'Pd{layer_num:.0f}'
    # LC_1st = 2.753230221       # From Pd6 ThinFilm relax
    # LC_2nd = 2.467884734       # From Co6 ThinFilm relax
    
    atom_type = f"Fe{layer_num:.0f}"
    LC_1st = 2.84

    # Dv = np.sqrt(6)*LC_1st/3.8 # SupperLattice
    Dv = 15 # Bilayer
# ========================================================    
# ========================================================
    Struc = AUTOsub(atom_type, (LC_1st,), Dv)
    # Struc.PureThinfilm(stacking="FCC(111)") # POSCAR
    Struc.PureThinfilm(stacking="BCC(001)") # POSCAR
    Struc.POTCAR(PT_type='PBE', where='STT')

#----------------------
    # file_name = f"{int(layer_num)}_{atom_type}_f"

    # os.mkdir(f"{file_name}/")
# #----------------------
#     os.system(f"cp OUTFILE/* {file_name}/.")
# #----------------------
#     os.chdir(f"{file_name}/")
#     print()
#     os.system('pwd')
#     print(f"{atom_type}")
# #----------------------
#     os.chdir('../')
#     os.system('pwd')

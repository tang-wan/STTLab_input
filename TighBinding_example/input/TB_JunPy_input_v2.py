import numpy as np # type: ignore
import os
import sys
# ========================
sys.path.append('/home/tangtang89/Example_Lab/')
from Tools import MKdir # type: ignore
# ========================

def RemoveTuple(a_str):
    a_str = a_str.replace("(", "")
    a_str = a_str.replace(")", "")
    a_str = a_str.replace(",", "")
    a_str = a_str.replace(" ", "")
    # a_str = a_str.replace("\'", "")
    return a_str

class TB_JPinput():

    def __init__(self, 
                 angleTuple,
                 NL_group,
                 NL_set):
        
        self.NL_set = NL_set

        RLLnum = f"{len(NL_set)}_RLL{len(NL_set)}"

        NL_group_str = RemoveTuple(str(NL_group))
        RLLgroup_sub = f"RLL{len(NL_group)}_NL{sum(NL_group)}_{NL_group_str}"

        NL_set_str = RemoveTuple(str(NL_set))
        RLLnum_sub = f"RLL{len(NL_set)}_NL{sum(NL_set)}_{NL_set_str}"
        
        RLLnum_angle_sub = f"{angleTuple[1]}_{angleTuple[2]}"
        RLLnum_angle     = f"{angleTuple[0]}_{angleTuple[1]}_{angleTuple[2]}"

        MKdir(f"{RLLnum}/", rm=False)
        MKdir(f"{RLLnum}/{RLLgroup_sub}/", rm=False)
        MKdir(f"{RLLnum}/{RLLgroup_sub}/{RLLnum_sub}/", rm=False)
        MKdir(f"{RLLnum}/{RLLgroup_sub}/{RLLnum_sub}/{RLLnum_angle_sub}/", rm=False)
        MKdir(f"{RLLnum}/{RLLgroup_sub}/{RLLnum_sub}/{RLLnum_angle_sub}/{RLLnum_angle}", rm=True)

        self.targetPath = f"{RLLnum}/{RLLgroup_sub}/{RLLnum_sub}/{RLLnum_angle_sub}/{RLLnum_angle}"

    def MK_main_BD(self, HoppingE,
                   NL, eL,
                   NB, PhiB, dB,
                   γB,       # Use for NI
                   γBL, γBR, # Use for AFM
                   NR, eR,
                   AFM
                ):
        
        targetPath = self.targetPath
        def Initial():
            with open(f"{targetPath}/main.py", 'w') as W_File:
                lines=[
                    'import numpy as np\n',
                    'import junpy as jp\n',
                    'from junpy.factory import stack\n',
                    '\n',
                    '#==============================================================================\n',
                    '\n'
                ]
                W_File.writelines(lines)

        def BD_Initial():
            with open(f"{targetPath}/main.py", 'a') as A_File:
                lines=[
                        '    #   μL,μR     => Bias setting\n',
                        '    # γL, γLI, γR => Angle of Bottom, Central, Top\n',
                        'def build_device(μL, μR, γL, γLI, γR, NL_set):\n',
                        '\n',
                        '# ___________ Intial ___________\n',
                        '    builder = stack.TwoProbeDeviceBuilder()\n',
                        ' \n',
                        '    ## Hopping/Coupling Energy Parameters\n',
                       f'    t = {HoppingE}\n',
                        '    tt = (-t, -t)\n',
                        '\n'
                ]
                A_File.writelines(lines)

        def BD_L_Lead():
            with open(f"{targetPath}/main.py", 'a') as A_File:
                lines=[
                        '# _______________________________________\n',
                        '# _______________________________________\n',
                        '# ___________ Lead (L/Bottom) ___________\n',
                        '\n',
                        '    ## Number of L-lead\n',
                       f'    NL = {NL}\n',
                        '    ## Onsite Energy of Lead\n',
                       f'    eL = {eL}\n',
                        '\n',
                        '    ## Two-probe Device setting\n',
                        '    ### Lead (L/Bottom)\n',
                        '    builder.L.set(chemicalPotential=μL, temperature=0)\n',
                        '    builder.L.add(eL, tt, nsites=1, spin=γL, bias=μL)\n',
                        '    ### Lead in Central part (L/Bottom)\n',
                        '    builder.C.add(eL, tt, nsites=NL, spin=γL, bias=μL)\n',
                        '\n'
                ]
                A_File.writelines(lines)
        
        def BD_Central():
            with open(f"{targetPath}/main.py", 'a') as A_File:
                lines=[
                        '# ___________ FM Region setting ___________\n',
                        '\n',
                        '    ## Define Region of FM Layers\n',
                        '    RLL = len(NL_set)\n',
                        '\n',
                        '    dγ = (γLI-γL)/(RLL+1)\n',
                        '\n',
                        '    ## Two-probe Device setting\n',
                        '    ### Central part (B-to-T)\n',
                        '    for i, NLN in enumerate(NL_set):\n',
                        '        builder.C.add(eL, tt, \n',
                        '                    nsites = NLN, \n',
                        '                    spin   = γL + dγ*(i+1), \n',
                        '                    bias   = μL)\n',
                        '\n',
                        '    builder.C.add(eL, tt, nsites=1, spin=γLI, bias=μL)\n',
                        '\n'
                ]
                A_File.writelines(lines)
        
        def BD_Barrier():
            if AFM:
                lines=[
                        '# ___________ Barrier setting ___________\n',
                        '\n',
                        '    ## AFM Barrier\n',
                       f'    NB = {NB}\n',
                        '    NBL = int(NB/2)\n',
                        '    NBR = int(NB/2)\n',
                       f'    γBL = {γBL}\n',
                       f'    γBR = {γBR}\n',
                       f'    PhiB = {PhiB}\n',
                       f'    dB = {dB}\n',
                        '\n',
                        '    ## Onsite Energy of Barrier\n',
                        '    eB = (PhiB-dB/2+6*t, PhiB+dB/2+6*t)\n',
                        '\n',
                        '    ## Shift of Bias\n',
                        '    dV = (μR-μL)/(NB-1)\n',
                        '    bshift = np.arange(NB)*dV\n',
                        '\n',
                        '    ## Two-probe Device setting\n',
                        '    builder.C.add(eB, tt, nsites=NBL, spin=γBL, bias=bshift[0: NBL])\n',
                        '    builder.C.add(eB, tt, nsites=NBR, spin=γBR, bias=bshift[NBL: NB])\n',
                        '\n'
                    ]
            else:
                lines=[
                        '# ___________ Barrier setting ___________\n',
                        '\n',
                        '    ## NI Barrier\n',
                       f'    NB = {NB}\n',
                       f'    PhiB = {PhiB}\n',
                       f'    γB = {γB} \n',
                       f'    dB = {dB}\n',
                        '\n',
                        '    ## Onsite Energy of Barrier\n',
                        '    eB = (PhiB-dB/2+6*t, PhiB+dB/2+6*t)\n',
                        '\n',
                        '    ## Shift of Bias\n',
                        '    dV = (μR-μL)/(NB-1)\n',
                        '    bshift = np.arange(NB)*dV\n',
                        '\n',
                        '    ## Two-probe Device setting\n',
                        '    builder.C.add(eB, tt, nsites=NB, spin=γB, bias=bshift[0: NB])\n',
                        '\n'
                    ]
            with open(f"{targetPath}/main.py", 'a') as A_File:
                A_File.writelines(lines)

        def BD_R_Lead():
            with open(f"{targetPath}/main.py", 'a') as A_File:
                lines=[
                        '# ___________ Lead (R/Top) ___________\n',
                        '\n',
                        '    ## Number of L-lead\n',
                       f'    NR = {NR}\n',
                        '    ## Onsite Energy of Lead\n',
                       f'    eR = {eR}\n',
                        '\n',
                        '    ## Two-probe Device setting\n',
                        '    ### Lead in Central part (R/Top)\n',
                        '    builder.C.add(eR, tt, nsites=NR, spin=γR, bias=μR)\n',
                        '    ### Lead (R/Top)\n',
                        '    builder.R.add(eR, tt, nsites=1, spin=γR, bias=μR)\n',
                        '    builder.R.set(chemicalPotential=μR, temperature=0)\n',
                        '\n'
                ]
                A_File.writelines(lines)

        def BD_Secondary():
            with open(f"{targetPath}/main.py", 'a') as A_File:
                lines=[
                        '# __________________________________________________________\n',
                        '# __________________________________________________________\n',
                        '# ___________ Two-probe Device Secondary setting ___________\n',
                        '\n',
                        '    ## define coupling between layers\n',
                        '    builder.set_layer_coupling(all=tt)\n',
                        '\n',
                        '    ## define translation symmetry\n',
                        '    builder.set_translationSymmetry(x=True, y=True)\n',
                        '\n',
                        '    ## create device\n',
                        '    return builder.create_device()\n',
                        '\n'
                ]
                A_File.writelines(lines)
     
    # ==============================================
        Initial()
        BD_Initial()
        BD_L_Lead()
        BD_Central()
        BD_Barrier()
        BD_R_Lead()
        BD_Secondary()

        with open(f'{targetPath}/main.py', 'a') as A_File:
            lines=[    
                '\n'
            ]
            A_File.writelines(lines)
    # ==============================================
    def MK_main_BC(self, μL, μR_bias,
            γL, γLI, γR
            ):
        
        γL  = '(np.pi/180)*' + str(γL)
        γLI = '(np.pi/180)*' + str(γLI) 
        γR  = '(np.pi/180)*' + str(γR) 

        # γL  = 'np.pi/180*90'
        # γLI = 'np.pi/180*' + str(γLI), 

        targetPath = self.targetPath
        NL_set     = self.NL_set
        def BC_Fun():
            with open(f"{targetPath}/main.py", 'a') as A_File:
                lines=[
                        '#==============================================================================\n',
                        '\n',
                        'def build_calcr(bias):\n',
                       f'    device = build_device(μL   = {μL}, \n'
                        '                          μR   = bias, \n',
                       f'                          γL   = {γL}, \n'
                       f'                          γLI  = {γLI},\n' 
                       f'                          γR   = {γR}, \n'
                       f'                          NL_set = {NL_set}\n',
                        '                           )\n',
                        '    return jp.Current(\n',
                        '        device=device,\n',
                        '        kpoints=jp.UniformKspaceSampling(\n',
                        '            gridNumber=(51,51,1),\n',
                        '            isTimeReversalSymmetry=True,\n',
                        '        ),\n',
                        '        energies=jp.BiasWindow(interval=1e-4),\n',
                        '        etaSigma=1e-4,\n',
                        '    )\n',
                        '\n'
                ]
                A_File.writelines(lines)   
                
        def Run_Set():
            with open(f"{targetPath}/main.py", 'a') as A_File:
                lines=[
                        '#==============================================================================\n',
                        '\n',
                        # 'biases = np.linspace(0.01, 0.05, 5)\n',
                       f'biases = {μR_bias}\n',
                        'calcr = jp.BiasBatchRunner(biases, build_calcr)\n',
                        'jp.run(calcr)\n',
                        '\n'
                ]
                A_File.writelines(lines)  
        
        BC_Fun()
        Run_Set()

        with open(f'{targetPath}/main.py', 'a') as A_File:
                lines=[    
                    '\n'
                ]
                A_File.writelines(lines)

    def MK_parse(self):
        targetPath = self.targetPath
        os.system(f"cp /home/tangtang89/Example_Lab/TighBinding_example/output/parse.py {targetPath}")
        os.system(f"cp /home/tangtang89/Example_Lab/TighBinding_example/output/parse.sh {targetPath}")

    def MK_JPpbs(self, name='current', machine='i91', ppn=18):
        targetPath = self.targetPath
        lines = [
                '#!/bin/bash\n',
                '#=============================================#\n',
                '# Job Name\n',
                '\n',
                f'#PBS -N {name}\n',
                '\n',
                '#---------------------------------------------#\n',
                '# Running machine (ppn: process per node)\n',

                f'#PBS -l nodes={machine}:ppn={ppn} \n',
                '#PBS -j oe\n',
                '\n',
                '#---------------------------------------------#\n',
                '# Setup environment variable\n',
                '# Use `module avail` to see more\n',

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
                # 'python3 parse.py\n',
                './parse.sh'
                '\n'
                ]
        with open(f'{targetPath}/junpy.pbs', 'w') as W_File:
            W_File.writelines(lines)

    def RunCode(self, Path):
        targetPath = self.targetPath
        HomePath = os.getcwd()
        if Path:
            print(HomePath)
        os.chdir(targetPath)
        if Path:
            os.system('pwd')
        os.system("qsub junpy.pbs")
        os.chdir(HomePath)
        if Path:
            os.system('pwd')
        

if __name__ == '__main__':

    biases = 'np.linspace(0.01, 0.05, 5)'
    angle  = (90, 180, 0)
    NL_set = (5, 4)

    run = True

    TB_test = TB_JPinput(angleTuple = angle, 
                         NL_group   = NL_set,
                         NL_set     = NL_set)
    TB_test.MK_main_BD(HoppingE=0.83,
                       NL=2, eL=(2.6, 6.0),
                       NB=2, PhiB = 0.6, γB = 0.2, dB = 0.0,
                       NR=2, eR=(2.6, 6.0),
                       AFM=False
                       )
    TB_test.MK_main_BC(μL      = 0,
                       μR_bias = biases,
                       γL      = angle[0], 
                       γLI     = angle[1],
                       γR      = angle[2]
                       )
    TB_test.MK_JPpbs(name='current',
                     machine='i91',
                     ppn=18)
    TB_test.MK_parse()
    
    if run:
        TB_test.RunCode()
    else:
        pass


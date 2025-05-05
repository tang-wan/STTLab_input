import numpy as np # type: ignore
import itertools
import os
#----------------------------------------
import sys
sys.path.append('/home/tangtang89/Example_Lab/TighBinding_example/input_v4/')
import TB_JunPy_input_v4 as TBi # type: ignore
# ========================================================
sys.path.append('/home/tangtang89/Example_Lab/')
from Tools import Sum_Combination, Process_Word, Check_out_Word # type: ignore
# ================= Don't need to change =================
# ========================================================

run  = 1
## False (0): Just create the film, don't auto submit the job
## True  (1): Create the film and auto submit the job

Path = 0
## False (0): Don't print the detail of the path
## True  (1): Print the detail of the path

HoppingE = 0.83
biases   = 'np.linspace(0.01, 0.05, 5)'

Ntot = 9    # The maximum region number (So for, don't need to change)
NLL_list  = [7, 8, 9]    # The number of the region

spec_NL_set = "ALL"                     # Run all the NLL set
spec_NL = "ALL"                     # Run all the combination of this NLL


init_Angle = 0   # The initial angle of γL iteration (unit: degree)
finl_Angle = 90  # The final angle of γL iteration (unit: degree)
sep_Angle  = 45  # The angle interval of γL iteration (unit: degree)
## If init_Angle and finl_Angle are the same, which mean running the specific angle of γL

γLI_Angle, γR_Angle = (180, 0)  # Setting the γLI and γR

# ========================================================
# >>>>> Setting left lead <<<<<
NL, eL = 2, (2.6, 6.0)

# >>>>> Setting for barrier <<<<<
AFM = True
## False: Turn off AFM => NI
##  True: Turn on AFM  => AFM
NB, PhiB, dB = 2, 0.6, 0.2
γB = 0.0                    # Only use for NI
γBL, γBR = 180, 0           # Only use for AFM

# >>>>> Setting for right lead <<<<<
NR, eR = 2, (2.6, 6.0)
# ========================================================

jobMach = 'dl2x'
jobPPN  = '14'
# ========================================================
# ================= Don't need to change =================
HomePath = os.getcwd()
for NLL in NLL_list:
    NLL_Combination = Sum_Combination(NLL, Ntot)
    jobName = f'current_RLL{NLL}'
    for i, NL_set in enumerate(NLL_Combination):
        if (NL_set == spec_NL_set) or (spec_NL_set == "ALL"):
            print()
            Process_Word("# ==========")
            Process_Word(f"NLL = {NLL}")
            Process_Word(NL_set)
            Process_Word(f"AFM is {AFM}")
            Process_Word("# ==========")
            for j, sub_NL_set in enumerate(list(set(itertools.permutations(NL_set)))):
                if (sub_NL_set == spec_NL) or (spec_NL == "ALL"):
                    print(sub_NL_set)
                    for k, an in enumerate(range(init_Angle, finl_Angle+1, sep_Angle)):
                        
                        angle    = (an, γLI_Angle, γR_Angle)
                        # (γL, γLI, γR)

                        print("Angle = ", angle)
                        TB_test = TBi.TB_JPinput(angleTuple = angle,
                                                 NL_group   = NL_set,
                                                 NL_set     = sub_NL_set
                                                )
                        TB_test.MK_main_BD(HoppingE=HoppingE,
                                           NL=NL, eL=eL,
                                           NB=NB, PhiB=PhiB, dB=dB,
                                           γB=γB,
                                           γBL=γBL, γBR=γBR,
                                           NR=NR, eR=eR,
                                           AFM=AFM
                                           )
                        TB_test.MK_main_BC(μL   = 0,
                                           μR_bias = biases,
                                           γL      = angle[0],
                                           γLI     = angle[1],
                                           γR      = angle[2]
                                           )
                        
                        TB_test.MK_parse()

                        # TB_test.MK_JPpbs(name=jobName, machine=jobMach, ppn=jobPPN)

                        # print(i)
                        if i==0 and j==0 and k==0:
                            # Check_out_Word("start")
                            TB_test.MK_JPpbsALL(init    = True,
                                                name    = jobName,
                                                machine = jobMach,
                                                ppn     = jobPPN
                                                )
                        else:
                            # pass
                            TB_test.MK_JPpbsALL(init    = False,
                                                name    = jobName,
                                                machine = jobMach,
                                                ppn     = jobPPN
                                                )

                        

                    print("# ----------")
            print("# ==========")
        else:
            print("We DON'T have this composition")
    if run:
        TB_test.RunCodeALL(Path=Path)
    else:
        pass
    
    print()

    


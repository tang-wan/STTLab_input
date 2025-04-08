import os
import itertools
import numpy as np # type: ignore
import globals     # type: ignore
#----------------------------------------
import sys
sys.path.append('/home/tangtang89/Example_Lab/TighBinding_example/input/')
from TB_JunPy_input_v2 import RemoveTuple # type: ignore
# ========================================================
sys.path.append('/home/tangtang89/Example_Lab/')
from Tools import Sum_Combination, MKdir, Process_Word, Check_out_Word # type: ignore
# ================= Don't need to change =================
# ========================================================

globals.initialize()

run  = globals.run
Path = globals.Path

Ntot = globals.Ntot
NLL_list  = globals.NLL_list

spec_NL_set = globals.spec_NL_set
spec_NL     = globals.spec_NL

init_Angle = globals.init_Angle
finl_Angle = globals.finl_Angle
sep_Angle  = globals.sep_Angle

γLI_Angle, γR_Angle = (globals.γLI_Angle, globals.γR_Angle)

# ========================================================
# ================= Don't need to change =================
for i, an in enumerate(range(init_Angle, finl_Angle+1, sep_Angle)):
    angle = (an, γLI_Angle, γR_Angle)
    # (γL, γLI, γR)        

    targetPath = f"Temperature_Rparse/"
    
    print(angle[0])
    
    with open(f"{targetPath}/{angle[0]}_{angle[1]}_{angle[2]}.dat", "w") as W_File:
        W_File.write("")
    
    print()
    Check_out_Word(f"Angle = {an} ")
    print("# ==========\n")

    for NLL in NLL_list:
        
        # ========================================================
        NL_Combination = Sum_Combination(NLL, Ntot)
        
        for or_NL_set in NL_Combination:
            
            if (or_NL_set == spec_NL_set) or (spec_NL_set == "ALL"):
                NL_set = RemoveTuple(str(or_NL_set))
                Process_Word(f"angle = {an}, ({NLL}, {NL_set})")
                parsePath  = f"Temperature_Rparse/{NLL}_RLL{NLL}/RLL{NLL}_NL{Ntot}_{NL_set}/RLL{NLL}_NL{Ntot}_{NL_set}_{angle[0]}_{angle[1]}_{angle[2]}_Rparse"
            # ==================================================================   
                R_data = np.loadtxt(f"{parsePath}/Rparse_R.dat", skiprows=1)

                # for d in R_data:
                #     NL_set_str = f"({NL_set})"
                #     title = f"R{NLL} {NL_set_str:>11}" + "    "
                #     word  = f"{d:.7f}" + "    "
                #     with open(f"{targetPath}/{angle[0]}_{angle[1]}_{angle[2]}.dat", "a") as A_File:
                #         if d == R_data[0]:
                #             A_File.write(title)
                #             A_File.write(word)
                #         elif d == R_data[-1]:
                #             A_File.write(word + '\n')
                #         else:
                #             A_File.write(word)
                for i, d in enumerate(R_data):
            
                    NL_set_str = f"({NL_set})"
                    title = f"R{NLL} {NL_set_str:>11}" + "    "
                    word  = f"{d:.7f}" + "    "
                    with open(f"{targetPath}/{angle[0]}_{angle[1]}_{angle[2]}.dat", "a") as A_File:
                        
                        if i == 0:
                            A_File.write(title)
                            A_File.write(word)

                        elif i == (len(R_data)-1):
                            A_File.write(word + '\n')
                        
                        else:
                            A_File.write(word)

                print(R_data)
                print("# -----")
    print("# ==========\n")

                


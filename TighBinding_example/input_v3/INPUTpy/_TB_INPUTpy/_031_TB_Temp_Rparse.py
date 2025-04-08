import os
import itertools
import globals  # type: ignore
#----------------------------------------
import sys
sys.path.append('/home/tangtang89/Example_Lab/TighBinding_example/input_v3/')
from TB_JunPy_input_v3 import RemoveTuple # type: ignore
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
for NLL in NLL_list:                   
    Check_out_Word(f"NLL = {NLL}")
    for an in range(init_Angle, finl_Angle+1, sep_Angle):
        angle    = (an, γLI_Angle, γR_Angle)
        # (γL, γLI, γR)
        Check_out_Word(f"Angle = {an}")
        print("# ==========\n")
        # MKdir(f"{NLL}_RLL{NLL}/", rm=False)
        MKdir(f"Temperature_Rparse/", rm=False)
        MKdir(f"Temperature_Rparse/{NLL}_RLL{NLL}", rm=False)
        
        NL_Combination = Sum_Combination(NLL, Ntot)
        for or_NL_set in NL_Combination:
            if (or_NL_set == spec_NL_set) or (spec_NL_set == "ALL"):
                NL_set = RemoveTuple(str(or_NL_set))
                Process_Word(f"{NL_set}")

                MKdir(f"Temperature_Rparse/{NLL}_RLL{NLL}/RLL{NLL}_NL{Ntot}_{NL_set}", rm=False)
                parsePath  = f"Temperature_Rparse/{NLL}_RLL{NLL}/RLL{NLL}_NL{Ntot}_{NL_set}/RLL{NLL}_NL{Ntot}_{NL_set}_{angle[0]}_{angle[1]}_{angle[2]}_Rparse"
                MKdir(parsePath, rm=True)
                os.system(f"cp -r /home/tangtang89/Example_Lab/TighBinding_example/output/R_parse/* {parsePath}/.")

                with open(f"{parsePath}/Rparse_input.txt", "w") as W_File:
                    W_File.writelines([""])
                
                for i, sub_NL_set in enumerate(list(set(itertools.permutations(or_NL_set)))):
                    if (sub_NL_set == spec_NL) or (spec_NL == "ALL"):
                        sub_NL_set = RemoveTuple(str(sub_NL_set))
                        
                        if (i+1)%5 == 0:
                            print(sub_NL_set)
                        elif (i+1) == 1:
                            print("# vvvvv")
                            print(sub_NL_set, end=" ")
                        else:
                            print(sub_NL_set, end=" ")

                        targetPath = f"{NLL}_RLL{NLL}/RLL{NLL}_NL{Ntot}_{NL_set}/RLL{NLL}_NL{Ntot}_{sub_NL_set}/{angle[1]}_{angle[2]}"
                        
                    # ==================================================================        
                        lines = [
                            "../../../../{}/{}_{}_{}/Bias_totI.dat\n".format(targetPath, *angle)
                        ]
                        
                        with open(f"{parsePath}/Rparse_input.txt", "a") as A_File:
                            A_File.writelines(lines)
                if i == 0:
                    with open(f"{parsePath}/Rparse_input.txt", "a") as A_File:
                            A_File.writelines(lines)
                else:
                    pass
                
                print("\n# ^^^^^")
                    
                if run:
                    HomePath = os.getcwd()
                    if Path:
                        print(HomePath)
                    os.chdir(parsePath)
                    if Path:
                        os.system('pwd')
                    os.system("./Rparse.sh False")
                    os.chdir(HomePath)
                    if Path:
                        os.system('pwd')

            print("# >>>>>>>>>>>>>>>>>>>>\n")

                        


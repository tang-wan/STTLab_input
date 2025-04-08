import os
import itertools
import globals # type: ignore
#----------------------------------------
import sys
sys.path.append('/home/tangtang89/Example_Lab/TighBinding_example/input/')
from TB_JunPy_input_v2 import RemoveTuple # type: ignore
# ========================================================
sys.path.append('/home/tangtang89/Example_Lab/')
from Tools import Sum_Combination, MKdir, Process_Word, Check_out_Word # type: ignore
# ================= Don't need to change =================
# run  = 1
# Path = 0

# Ntot = 9
# NLL_list  = [8, 7]

# spec_NL_set = "ALL"
# # spec_NL_set = (2, 2, 1, 1, 1, 1, 1)
# spec_NL     = "ALL"                     # Run all the combination of this NLL
# # spec_NL     = (2, 1, 1, 1, 1, 1, 1, 1)     # Run the specific combination of this NLL

# init_Angle = 0  # The initial angle of γL iteration (unit: degree)
# finl_Angle = 90  # The final angle of γL iteration (unit: degree)
# sep_Angle  = 45  # The angle interval of γL iteration (unit: degree)
# ## If init_Angle and finl_Angle are the same, which mean running the specific angle of γL

# γLI_Angle, γR_Angle = (180, 0)
# # γLI_Angle, γR_Angle = (0, 180)
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
    NL_Combination = Sum_Combination(NLL, Ntot)
    Check_out_Word(f"NLL = {NLL}")
    for or_NL_set in NL_Combination:
        if (or_NL_set == spec_NL_set) or (spec_NL_set == "ALL"):
            NL_set = RemoveTuple(str(or_NL_set))
            Check_out_Word(NL_set)
            print("# ==========")
            MKdir(f"{NLL}_RLL{NLL}/", rm=False)
            MKdir(f"{NLL}_RLL{NLL}/Field_Rparse/", rm=False)
            MKdir(f"{NLL}_RLL{NLL}/Field_Rparse/RLL{NLL}_NL{Ntot}_{NL_set}", rm=False)
            for sub_NL_set in list(set(itertools.permutations(or_NL_set))):
                if (sub_NL_set == spec_NL) or (spec_NL == "ALL"):
                    sub_NL_set = RemoveTuple(str(sub_NL_set))
                    print()
                    print("# -----")
                    Process_Word(sub_NL_set)
                    targetPath = f"RLL{NLL}_NL{Ntot}_{NL_set}/RLL{NLL}_NL{Ntot}_{sub_NL_set}/{γLI_Angle}_{γR_Angle}"
                    parsePath  = f"{NLL}_RLL{NLL}/Field_Rparse/RLL{NLL}_NL{Ntot}_{NL_set}/RLL{NLL}_NL{Ntot}_{sub_NL_set}_Rparse"
                    MKdir(parsePath, rm=True)
                    os.system(f"cp -r /home/tangtang89/Example_Lab/TighBinding_example/output/R_parse/* {parsePath}/.")
                # ==================================================================        
                    
                    for i, an in enumerate(range(init_Angle, finl_Angle+1, sep_Angle)):
                        angle    = (an, γLI_Angle, γR_Angle)
                        # (γL, γLI, γR)

                        lines = [
                            "../../../{}/{}_{}_{}/Bias_totI.dat\n".format(targetPath, *angle)
                        ]
                        if i==0:
                            with open(f"{parsePath}/Rparse_input.txt", "w") as W_File:
                                W_File.writelines(lines)
                        else:
                            with open(f"{parsePath}/Rparse_input.txt", "a") as A_File:
                                A_File.writelines(lines)
                    
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
        print("# ==========\n")

                        


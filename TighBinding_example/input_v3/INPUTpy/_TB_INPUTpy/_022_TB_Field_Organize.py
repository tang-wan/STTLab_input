import os
import itertools
import numpy as np # type: ignore
import globals     # type: ignore
#----------------------------------------
import sys
sys.path.append('/home/tangtang89/Example_Lab/TighBinding_example/input_v3/')
from TB_JunPy_input_v3 import RemoveTuple # type: ignore
# ========================================================
sys.path.append('/home/tangtang89/Example_Lab/')
from Tools import Sum_Combination, Process_Word, Check_out_Word # type: ignore
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
angle_array = np.array([i for i in range(init_Angle, finl_Angle+1, sep_Angle)])
angle_array = np.insert(angle_array, 0, 0)

# ========================================================
for NLL in NLL_list: 
    NL_Combination = Sum_Combination(NLL, Ntot)
    Data_ALL_array = angle_array
    print()
    Check_out_Word(f"NLL={NLL}")

    for or_NL_set in NL_Combination:
        if (or_NL_set == spec_NL_set) or (spec_NL_set == "ALL"):
            NL_set = RemoveTuple(str(or_NL_set))
            print("# -----")        
            Process_Word(NL_set)
            for i, sub_NL_set in enumerate(list(set(itertools.permutations(or_NL_set)))):
                if (sub_NL_set == spec_NL) or (spec_NL == "ALL"):
                    sub_NL_set = RemoveTuple(str(sub_NL_set))

                    if (i+1)%5 == 0:
                        print(sub_NL_set)
                    else:
                        print(sub_NL_set, end=" ")
                    
                    parsePath  = f"{NLL}_RLL{NLL}/Field_Rparse/RLL{NLL}_NL{Ntot}_{NL_set}/RLL{NLL}_NL{Ntot}_{sub_NL_set}_Rparse"
                    
                # ==================================================================   
                    R_data = np.loadtxt(f"{parsePath}/Rparse_R.dat", skiprows=1)
                    R_data = np.insert(R_data, 0, int(sub_NL_set))
                    Data_ALL_array = np.append(Data_ALL_array, R_data)
            print()
    print("# ==========")
    Data_ALL_array = Data_ALL_array.reshape(int(len(Data_ALL_array)/len(angle_array)), len(angle_array))
    print()
    Process_Word(f"Field Result of NLL={NLL} ")
    print(Data_ALL_array)

    head = "case" + "                   # R (angle)" + "              # R (angle)"*int(len(angle_array)-2)
    np.savetxt(f"Field_R_parse.dat", Data_ALL_array, header=head)
    targetPath = f"{NLL}_RLL{NLL}/Field_Rparse/"
    os.system(f"mv Field_R_parse.dat {targetPath}/.")
    print("# ==========\n")

                    


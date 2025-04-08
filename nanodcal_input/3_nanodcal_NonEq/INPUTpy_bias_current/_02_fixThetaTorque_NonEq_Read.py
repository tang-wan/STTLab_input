import os
import numpy as np # type: ignore
import matplotlib.pyplot as plt # type: ignore

bias_array = np.array([0.01, 0.02, 0.03, 0.04, 0.05])

for angle in [0]:
    print(bias_array)    
    targetPath = f'./Bias_current_fixTheta_{angle:>003}'
    current = np.loadtxt(f"{targetPath}/Result_output_Current.txt", skiprows=1)

    bias_current = np.c_[bias_array, current]

    np.savetxt(f"{targetPath}/Bias_Current.txt", bias_current, header='bias (V), current (A)')



    
    
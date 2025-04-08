import sys
import os
import numpy as np                    # type: ignore
from scipy.optimize import curve_fit  # type:ignore
import matplotlib.pyplot as plt       # type: ignore

def linearF(x, a, b):
    return a*x+b

def LinearCurve(px, py, name, plot=True):
    fitt   = ((py[-1]-py[0])/(px[-1]-px[0]), 0)
    popt, pcov = curve_fit(linearF, px, py, p0=fitt)
    # print(popt)
    
    if plot:
        fit_x = np.linspace(px[0], px[-1], 1000)
        fit_y = linearF(fit_x, *popt)
        plt.figure()
        ax = plt.subplot(111)
        ax.scatter(px, py)
        ax.plot(fit_x, fit_y, label='y={}x+{}'.format(*popt, ))
        ax.legend(loc='upper left')

        plt.savefig(f'FittingResult/{name}.png')
    else:
        pass

    return popt[0], popt[1]
#==============================================================================

if len(sys.argv) == 1:
    Print = True
elif len(sys.argv) == 2:
    if sys.argv[1]=='True':
        Print = True
    elif sys.argv[1]=='False':
        Print = False
else:
    raise RuntimeError('Usage: filename interface')
print()
print("Print the detail of each case >> ", Print)
print()
# read data
print('Loading files...')
print()
parsePath_array = np.loadtxt('Rparse_input.txt', dtype='str')
R_list = []

if os.path.isdir("FittingResult"):
    os.system("rm -r FittingResult")
    os.mkdir('FittingResult')
else:
    os.system("rm -r FittingResult")
    os.mkdir('FittingResult')

for i, FileName in enumerate(parsePath_array):
    if FileName.endswith('Bias_totI.dat'):
        print(i," " ,FileName)
    else:
        print("!!!! Please Load bias_totI.dat file !!!!")
        break
    VI_data = np.loadtxt(FileName, dtype='str')
    V_data_label, V_data = np.transpose(VI_data)[0][0], np.float64(np.transpose(VI_data)[0][1:])
    I_data_label, I_data = np.transpose(VI_data)[1][0], np.float64(np.transpose(VI_data)[1][1:])
    if Print:
        print(Print)
        print(f'{V_data_label:>7}', V_data)
        print(f'{I_data_label:>7}', I_data) 
    
    slope, shift = LinearCurve(px=I_data, py=V_data, name=f"{i}_Bias_totI")
    if Print:
        print(f"dV/dI = {slope}")
        print()
    R_list.append(slope)
    
    if i==0:
        with open("Rparse_R_dat", 'w') as W_File:
            print("dV/dI = R", file=W_File)
            print(f"{slope}" , file=W_File)
    else:
        with open("Rparse_R_dat", 'a') as A_File:
            print(f"{slope}", file=A_File)
    
print()
print("# =========")
print("The Resistance of Each Case")
for i, R in enumerate(R_list):
    print(i," " ,R)
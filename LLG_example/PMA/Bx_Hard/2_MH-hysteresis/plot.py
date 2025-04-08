#!/usr/bin/env python3
import matplotlib.pyplot as plt
import numpy as np

#==============================================================================

xArr = np.loadtxt('results/all_xArr.txt')
M1Arr = np.loadtxt('results/all_M1.txt')
M2Arr = np.loadtxt('results/all_M2.txt')

plt.figure()
plt.plot(xArr, M2Arr[:,0], '.-', label='M2x')
plt.plot(xArr, M2Arr[:,1], '.-', label='M2y')
plt.plot(xArr, M2Arr[:,2], '.-', label='M2z')
plt.legend()
plt.xlabel('B_ext (T)')
plt.ylabel('M')
plt.grid()

plt.savefig('fig_hysteresis', dpi=150)
#plt.show()

## 2-PMA-Bx_Hard
import os
import llgsolver
import llgsolver.twofree
import numpy as np
from llgsolver.utils import CONST_hbar, CONST_kB, CONST_mub, CONST_u0

import sys
sys.path.append('../1_time-resolved/')
import globals
constant, anisotropy, sot_eff, h_therm, timeParams, initPositions = globals.initialize()
gamma, alpha = constant
h_ani_x, h_ani_z = anisotropy
eFL, eDL = sot_eff
# tmin, tmax, dt = timeParams
init_θ, [r1, θ1, φ1], [r2, θ2, φ2] = initPositions
#==============================================================================
tmin, tmax, dt = 0, 5e-7, 1e-12
#==============================================================================
print(f'h_ani_x = {h_ani_x} T')
print(f'h_ani_z = {h_ani_z} T')
print(f'h_therm = {h_therm} T')
#==============================================================================
# external field
#xbound1, xbound2, N = -10, 10, 50
xbound1, xbound2, N = -200e-4, 200e-4, 100

xArr1 = np.linspace(xbound1, xbound2, N, endpoint=False)
xArr2 = np.linspace(xbound2, xbound1, N+1)
xArr = np.hstack([xArr1,xArr2])

#==============================================================================

def system_of_x(x):

    #h_ext_x, h_ext_z, jc = 0, x, 0
    h_ext_x, h_ext_z, jc = x, 0, 0

    # fixed layer
    mag1 = llgsolver.twofree.Magnetization(
        fixed   = True,
        gamma   = gamma,
        alpha   = alpha,
        h_ani_x = 1,
    )
    # free layer
    mag2 = llgsolver.twofree.Magnetization(
        gamma   = gamma,
        alpha   = alpha,
        h_ani_x = h_ani_x,
        h_ani_z = h_ani_z,
        h_ext_x = h_ext_x,
        h_ext_z = h_ext_z,
        h_therm = h_therm,
        #eDL     = eDL*jc,
        #aFL     = eFL*jc,
    )

    return [mag1, mag2]

#==============================================================================
# start calculation

results = llgsolver.twofree.solve_hysteresis(
    system_of_x=system_of_x,
    xPoints=xArr,
    timeParams=[tmin, tmax, dt],
    initPositions=[[r1, θ1, φ1], [r2, θ2, φ2]],
    sixAxisSmallestAngle=init_θ,
    method='RungeKutta4'
)
M1Arr, M2Arr = results['xyz1'], results['xyz2']

#==============================================================================

os.makedirs('results', exist_ok=True)
np.savetxt('results/all_xArr.txt', xArr)
np.savetxt('results/all_M1.txt', M1Arr)
np.savetxt('results/all_M2.txt', M2Arr)
np.savetxt('results/loop1_xArr.txt', xArr[:N+1])
np.savetxt('results/loop1_M1.txt', M1Arr[:N+1])
np.savetxt('results/loop1_M2.txt', M2Arr[:N+1])
np.savetxt('results/loop2_xArr.txt', xArr[N:])
np.savetxt('results/loop2_M1.txt', M1Arr[N:])
np.savetxt('results/loop2_M2.txt', M2Arr[N:])

# 1-IMA-Bz_hard
import llgsolver
import llgsolver.twofree
import numpy as np
from llgsolver.utils import CONST_hbar, CONST_kB, CONST_mub, CONST_u0
#==============================================================================
import globals

constant, anisotropy, sot_eff, h_therm, timeParams, initPositions = globals.initialize()
gamma, alpha = constant
h_ani_x, h_ani_z = anisotropy
eFL, eDL = sot_eff
tmin, tmax, dt = timeParams
init_θ, [r1, θ1, φ1], [r2, θ2, φ2] = initPositions

print(f'h_ani_x = {h_ani_x} T')
print(f'h_ani_z = {h_ani_z} T')
print(f'h_therm = {h_therm} T')
#==============================================================================

def system():

    #h_ext_x, h_ext_z, jc =  200*1e-4, 0, 0 # x-dir external field
    h_ext_x, h_ext_z, jc =  0, 10, 0 # z-dir external field

    # fixed layer
    mag1 = llgsolver.twofree.Magnetization(
        fixed   = True,
        gamma   = gamma,
        alpha   = alpha,
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


results = llgsolver.twofree.solve_dmdt_double(
    system(),
    timeParams=[tmin, tmax, dt],
    initPositions=[[r1, θ1, φ1], [r2, θ2, φ2]],
    returnPolicy='all',
    method='RungeKutta4'
)
tArr, M1, M2 = results['time'], results['xyz1'], results['xyz2']

print('finised')

#==============================================================================

#data = np.c_[results['time'], results['xyz1'], results['xyz2']]
XX = 20
data = np.c_[results['time'][::XX], results['xyz1'][::XX], results['xyz2'][::XX]]
np.savetxt('results_time.txt', data)

# 1-PMA-Bx_Hard
import llgsolver
import llgsolver.twofree
import numpy as np
from llgsolver.utils import CONST_hbar, CONST_kB, CONST_mub, CONST_u0

def initialize(): 

    print(f'llgsolver.__version__: {llgsolver.__version__}')

    #==============================================================================
    # parameters
    tmin, tmax, dt = 0, 5e-7, 1e-12

    init_θ = 0.01
    r1, θ1, φ1 = [1, 0, 0] # no need to change
    r2, θ2, φ2 = [1, np.pi/2, init_θ+np.pi] # -x
    # r2, θ2, φ2 = [1, -np.pi+init_θ, 0] # -z

    # gyromagnetic ratio [rad/(s*T)]
    gamma = 2.2*CONST_mub/CONST_hbar
    # damping constant
    alpha = 0.01

    #--------------------------------------
    # magnetic anisotropy_Setting parameter

    #----magnetization [A/m]----
    Ms = 720*1e3
    ##total moment[J/T]/vloume[m^3]

    #----Uniaxial(Easy-axis)----
    # magnetocrystalline anisotropy [T]
    Hk = 100*1e-4

    #----Hard-axis----
    # Shape anisotropy [T]
    u0Ms = Ms*CONST_u0
    # H_shape = -u0Ms
    H_shape = 0

    # surface anisotropy (two sides) [T]
    # H_surface = -6.76
    H_surface = 0
    ##Torque[eV]/total moment[eV/T]

    #--------------------------------------
    # magnetic anisotropy_Setting easy/hard sxis

    #h_ani_x = Hk                        #IMA => Choose x-axis as easy-axis
    #h_ani_z = H_surface + H_shape       #IMA => z-axis only is hard-axis
    h_ani_x = 0                          #PMA => Choose z-axis as easy-axis
    h_ani_z = Hk + (H_surface + H_shape) #PMA => Choose z-axis as easy-axis, and this value is 
    ## Hk is uniaxial anisotropy, which will competes with surface anisotropy and shape anisotropy
    ## positive => easy axis
    ## negative => hard axis

    print(f'u0Ms = {u0Ms} T')

    #==============================================================================
    #--------------------------------------
    # SOT efficiency [T/(A/cm^2)]

    # [HfTe2]
    #eFL = -7.8e-9 * 1e-3
    #eDL = -2.6e-8 * 1e-3
    # [PtTe2]
    eFL = 2.6e-7 * 1e-3
    eDL = 8.1e-8 * 1e-3

    #--------------------------------------
    # thermal effect

    # thickness [m]
    lm = 0.93e-9
    # volume [m^3]
    Vp = lm*230e-9*170e-9

    # temperature [K]
    #Te = 300
    Te = 0

    # thermal field [T]
    h_therm = np.sqrt( (2*alpha*CONST_kB*Te)/(gamma*Ms*Vp*dt) )
    # random seed
    llgsolver.twofree.set_random_seed(920)
    #==============================================================================

    constant = [gamma, alpha]
    anisotropy = [h_ani_x, h_ani_z]
    sot_eff = [eFL, eDL]
    timeParams = [tmin, tmax, dt]
    initPositions = [init_θ, [r1, θ1, φ1], [r2, θ2, φ2]]

    return constant, anisotropy, sot_eff, h_therm, timeParams, initPositions

import numpy as np
import junpy as jp
from junpy.factory import stack

#==============================================================================

def build_device(μL, μR, γL, γLI, γR):

    # hopping/coupling energy parameters
    t = 0.83
    tt = (-t, -t)

    # Number of L-lead and R-lead
    NL, NR = (2, 2)

    ## Top FM/I interface is NLL+1 and γLI 
    ## Bottom FM layer is 0 and γL
    ## Define Region of FM layers
    RLL = 2
    ## Total number of FM layers are Sum(NLi).
    ## Define number of sites in each region (B-to-T)
    
    NL1, NL2 = (5, 4)
    # NL1, NL2, NL3, NL4, NL5, NL6, NL7, NL8, NL9 = (1, 1, 1, 1, 1, 1, 1, 1, 1)

    ## Define angle in each Region (B-to-T)
    dγ = (γLI-γL)/(RLL+1) 
    γL1 = γL + dγ*1
    γL2 = γL + dγ*2
#    γL3 = γL + dγ*3
#    γL4 = γL + dγ*4
#    γL5 = γL + dγ*5
#    γL6 = γL + dγ*6
#    γL7 = γL + dγ*7
#    γL8 = γL + dγ*8
#    γL9 = γL + dγ*9

    # NI barrier
    NB = 2
    PhiB = 0.6
    γB = 0 
    dB = 0.0

#    # AFM barrier
#    NBL = 1
#    NBR = 1
#    NB = NBL+NBR
#    γBL = γLI
#    γBR = γR
#    PhiB = 0.6
#    dB = 0.0

    # onsite energy parameters
    eL = (2.6, 6.0)
    eB = (PhiB-dB/2+6*t, PhiB+dB/2+6*t)
    eR = (2.6, 6.0)

    # shift of bias
    dV = (μR-μL)/(NB-1)
    bshift = np.arange(NB)*dV

    # define two-probe device
    builder = stack.TwoProbeDeviceBuilder()
    builder.L.set(chemicalPotential=μL, temperature=0)
    builder.L.add(eL, tt, nsites=1, spin=γL, bias=μL)
    
    builder.C.add(eL, tt, nsites=NL, spin=γL, bias=μL) # Lead out in to central part
    #==========
    ## Define angle of sites in each region (B-to-T)
    builder.C.add(eL, tt, nsites=NL1, spin=γL1, bias=μL)
    builder.C.add(eL, tt, nsites=NL2, spin=γL2, bias=μL)
#    builder.C.add(eL, tt, nsites=NL3, spin=γL3, bias=μL)
#    builder.C.add(eL, tt, nsites=NL4, spin=γL4, bias=μL)
#    builder.C.add(eL, tt, nsites=NL5, spin=γL5, bias=μL)
#    builder.C.add(eL, tt, nsites=NL6, spin=γL6, bias=μL)
#    builder.C.add(eL, tt, nsites=NL7, spin=γL7, bias=μL)
#    builder.C.add(eL, tt, nsites=NL8, spin=γL8, bias=μL)
#    builder.C.add(eL, tt, nsites=NL9, spin=γL9, bias=μL)
    #==========
    ## Define angle and bias of Barrier
    builder.C.add(eB, tt, nsites=NB, spin=γB, bias=bshift[0: NB])
    ## Define angle and bias of AFM Barrier
#    builder.C.add(eB, tt, nsites=NBL, spin=γBL, bias=bshift[0: NBL])
#    builder.C.add(eB, tt, nsites=NBR, spin=γBR, bias=bshift[NBL: NB])
    #==========
    builder.C.add(eR, tt, nsites=NR, spin=γR, bias=μR)

    builder.R.add(eR, tt, nsites=1, spin=γR, bias=μR)
    builder.R.set(chemicalPotential=μR, temperature=0)

    # define coupling between layers
    builder.set_layer_coupling(all=tt)

    # define translation symmetry
    builder.set_translationSymmetry(x=True, y=True)

    # create device
    return builder.create_device()

#==============================================================================

def build_calcr(bias):
    device = build_device(μL=0, μR=bias, γL=np.pi/18*9, γLI=np.pi, γR=0)
#    device = build_device(μL=0, μR=bias, γL=np.pi/6*3, γLI=0, γR=np.pi)
    return jp.Current(
        device=device,
        kpoints=jp.UniformKspaceSampling(
            gridNumber=(51,51,1),
            isTimeReversalSymmetry=True,
        ),
        energies=jp.BiasWindow(interval=1e-4),
        etaSigma=1e-4,
    )

#==============================================================================

biases = np.linspace(0.01, 0.05, 5)
#biases = np.linspace(-0.05, -0.01, 5)
calcr = jp.BiasBatchRunner(biases, build_calcr)
jp.run(calcr)

import numpy as np
import junpy as jp
from junpy.factory import stack

#==============================================================================

    #   μL,μR     => Bias setting
    # γL, γLI, γR => Angle of Bottom, Central, Top
def build_device(μL, μR, γL, γLI, γR):

# ___________ Intial ___________
    ## Hopping/Coupling Energy Parameters
    t = 0.83
    tt = (-t, -t)

    ## Number of L-lead and R-lead
    NL, NR = (2, 2)

    ## Onsite Energy of Lead
    eL = (2.6, 6.0)
    eR = (2.6, 6.0)

# ___________ FM Region setting ___________
    ## Define Region of FM Layers
    RLL = 2
    
    ## Define Number of Sites in Each Region (B-to-T)
    NL1, NL2 = (5, 4)
    # NL1, NL2, NL3, NL4, NL5, NL6, NL7, NL8, NL9 = (1, 1, 1, 1, 1, 1, 1, 1, 1)

    ## Define Angle in Each Region (B-to-T)
    dγ = (γLI-γL)/(RLL+1) 
    γL1 = γL + dγ*1
    γL2 = γL + dγ*2
    # γL3 = γL + dγ*3
    # γL4 = γL + dγ*4
    # γL5 = γL + dγ*5
    # γL6 = γL + dγ*6
    # γL7 = γL + dγ*7
    # γL8 = γL + dγ*8
    # γL9 = γL + dγ*9

# ___________ Barrier setting ___________
    ## NI Barrier
    NB = 2
    PhiB = 0.6
    γB = 0 
    dB = 0.0

    ## AFM Barrier
    # NBL = 1
    # NBR = 1
    # NB = NBL+NBR
    # γBL = γLI
    # γBR = γR
    # PhiB = 0.6
    # dB = 0.2

    ## Onsite Energy of Barrier
    eB = (PhiB-dB/2+6*t, PhiB+dB/2+6*t)
    
    ## Shift of Bias
    dV = (μR-μL)/(NB-1)
    bshift = np.arange(NB)*dV

# ___________ Two-probe Device main setting ___________
    builder = stack.TwoProbeDeviceBuilder()

    ## Lead (L/Bottom)
    builder.L.set(chemicalPotential=μL, temperature=0)
    builder.L.add(eL, tt, nsites=1, spin=γL, bias=μL)
    ## Lead in Central part (L/Bottom)
    builder.C.add(eL, tt, nsites=NL, spin=γL, bias=μL)
    
    ## Central part (B-to-T)
    builder.C.add(eL, tt, nsites=NL1, spin=γL1, bias=μL)
    builder.C.add(eL, tt, nsites=NL2, spin=γL2, bias=μL)
    # builder.C.add(eL, tt, nsites=NL3, spin=γL3, bias=μL)
    # builder.C.add(eL, tt, nsites=NL4, spin=γL4, bias=μL)
    # builder.C.add(eL, tt, nsites=NL5, spin=γL5, bias=μL)
    # builder.C.add(eL, tt, nsites=NL6, spin=γL6, bias=μL)
    # builder.C.add(eL, tt, nsites=NL7, spin=γL7, bias=μL)
    # builder.C.add(eL, tt, nsites=NL8, spin=γL8, bias=μL)
    # builder.C.add(eL, tt, nsites=NL9, spin=γL9, bias=μL)
    
    builder.C.add(eL, tt, nsites=1, spin=γLI, bias=μL)
    ## Barrier
    builder.C.add(eB, tt, nsites=NB, spin=γB, bias=bshift[0: NB])
    ## Define angle and bias of AFM Barrier
    # builder.C.add(eB, tt, nsites=NBL, spin=γBL, bias=bshift[0: NBL])
    # builder.C.add(eB, tt, nsites=NBR, spin=γBR, bias=bshift[NBL: NB])
    
    ## Lead in Central part (R/Top)
    builder.C.add(eR, tt, nsites=NR, spin=γR, bias=μR)
    ## Lead (R/Top)
    builder.R.add(eR, tt, nsites=1, spin=γR, bias=μR)
    builder.R.set(chemicalPotential=μR, temperature=0)

# ___________ Two-probe Device Secondary setting ___________
    ## define coupling between layers
    builder.set_layer_coupling(all=tt)

    ## define translation symmetry
    builder.set_translationSymmetry(x=True, y=True)

    ## create device
    return builder.create_device()

#==============================================================================

def build_calcr(bias):
    device = build_device(μL=0, μR=bias, γL=np.pi/18*9, γLI=np.pi, γR=0)
    # device = build_device(μL=0, μR=bias, γL=np.pi/6*3, γLI=0, γR=np.pi)
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

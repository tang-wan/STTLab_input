import numpy as np
import junpy as jp
from junpy.factory import stack

#==============================================================================

    #   μL,μR     => Bias setting
    # γL, γLI, γR => Angle of Bottom, Central, Top
def build_device(μL, μR, γL, γLI, γR, NL_set):

# ___________ Intial ___________
    builder = stack.TwoProbeDeviceBuilder()
    
    ## Hopping/Coupling Energy Parameters
    t = 0.83
    tt = (-t, -t)
# _______________________________________
# _______________________________________
# ___________ Lead (L/Bottom) ___________
    
    ## Number of L-lead
    NL = 2
    ## Onsite Energy of Lead
    eL = (2.6, 6.0)
    
    ## Two-probe Device setting
    ### Lead (L/Bottom)
    builder.L.set(chemicalPotential=μL, temperature=0)
    builder.L.add(eL, tt, nsites=1, spin=γL, bias=μL)
    ### Lead in Central part (L/Bottom)
    builder.C.add(eL, tt, nsites=NL, spin=γL, bias=μL)

# ___________ FM Region setting ___________
    ## Define Region of FM Layers
    RLL = len(NL_set)
    
    dγ = (γLI-γL)/(RLL+1)
    
    ## Two-probe Device setting
    ### Central part (B-to-T)
    for i, NLN in enumerate(NL_set):
        builder.C.add(eL, tt, 
                      nsites = NLN, 
                      spin   = γL + dγ*(i+1), 
                      bias   = μL)

# ___________ Barrier setting ___________
    
    ## Onsite Energy of Barrier
    eB = (PhiB-dB/2+6*t, PhiB+dB/2+6*t)
    
    ## Shift of Bias
    dV = (μR-μL)/(NB-1)
    bshift = np.arange(NB)*dV
    
    ## NI Barrier
    NB = 2
    PhiB = 0.6
    γB = 0 
    dB = 0.0

    ## Two-probe Device setting
    builder.C.add(eB, tt, nsites=NB, spin=γB, bias=bshift[0: NB])

    ## AFM Barrier
    # NBL = 1
    # NBR = 1
    # NB = NBL+NBR
    # γBL = γLI
    # γBR = γR
    # PhiB = 0.6
    # dB = 0.0
    ## Two-probe Device setting
    # builder.C.add(eB, tt, nsites=NBL, spin=γBL, bias=bshift[0: NBL])
    # builder.C.add(eB, tt, nsites=NBR, spin=γBR, bias=bshift[NBL: NB])

# ___________ Lead (R/Top) ___________
    
    ## Number of L-lead
    NR = 2
    ## Onsite Energy of Lead
    eR = (2.6, 6.0)

    ## Two-probe Device setting
    ### Lead in Central part (R/Top)
    builder.C.add(eR, tt, nsites=NR, spin=γR, bias=μR)
    ### Lead (R/Top)
    builder.R.add(eR, tt, nsites=1, spin=γR, bias=μR)
    builder.R.set(chemicalPotential=μR, temperature=0)

# __________________________________________________________
# __________________________________________________________
# ___________ Two-probe Device Secondary setting ___________
    ## define coupling between layers
    builder.set_layer_coupling(all=tt)

    ## define translation symmetry
    builder.set_translationSymmetry(x=True, y=True)

    ## create device
    return builder.create_device()

#==============================================================================

def build_calcr(bias):
    device = build_device(μL=0, μR=bias, γL=np.pi/18*9, γLI=np.pi, γR=0, NL_set=(5, 4))
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

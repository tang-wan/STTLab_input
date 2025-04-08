import numpy as np
import junpy as jp
from junpy.factory import stack

#==============================================================================

def build_device(μL, μR, γL, γR, γSF1, γLL):

    t = 0.83

    # number of sites of each region
    NL  = 2
    NL1 = 6
    NL2 = 6
#    NL3 = 1
#    NL4 = 1
#    NL5 = 1
#    NL6 = 1
    NB1 = 3
    NR  = 2

    PhiSF = 0.6
    dSF = 0.0

    # Angle of AP-SRO/I
    # Devide 2-Region
    RL = 2
    dγ = (γLL-γL)/RL
    ## Region 1
    γL1 = γL+dγ
    ## Region 2
    γL2 = γL+2*dγ

    # onsite energy parameters
    eL  = ( 2.6, 6.0)
    eB1 = ( PhiSF-dSF/2+6*t, PhiSF+dSF/2+6*t)
    eR  = ( 2.6, 6.0)

    # hopping/coupling energy parameters
    tt   = (-t, -t)

    # shift of bias
    dV = (μR-μL)/(NB1-1)
    bshift = np.arange(NB1)*dV

    # define two-probe device
    builder = stack.TwoProbeDeviceBuilder()
    builder.L.set(chemicalPotential=μL, temperature=0)
    builder.L.add(eL, tt, nsites=1, spin=γL, bias=μL)
    builder.C.add(eL, tt, nsites=NL, spin=γL, bias=μL)
    builder.C.add(eL, tt, nsites=NL1, spin=γL1, bias=μL)
    builder.C.add(eL, tt, nsites=NL2, spin=γL2, bias=μL)
#    builder.C.add(eL, tt, nsites=NL3, spin=γL3, bias=μL)
#    builder.C.add(eL, tt, nsites=NL4, spin=γL4, bias=μL)
#    builder.C.add(eL, tt, nsites=NL5, spin=γL5, bias=μL)
#    builder.C.add(eL, tt, nsites=NL6, spin=γL6, bias=μL)
    builder.C.add(eB1, tt, nsites=NB1, spin=γSF1, bias=bshift[0: NB1])
#    builder.C.add(eB2, tt, nsites=NB2, spin=γSF2, bias=bshift[NB1: NB1+NB2])
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
    device = build_device(μL=0, μR=bias, γL=np.pi/3*2, γR=np.pi, γSF1=0, γLL=0)
#    device = build_device(μL=0, μR=bias, γL=0, γR=0, γSF1=0, γL1=np.pi/2, γL2=np.pi/2, γL3=np.pi/2, γL4=np.pi/2, γL5=np.pi/2, γL6=np.pi/2, γL7=np.pi, γL8=np.pi, γL9=np.pi, γL10=np.pi, γL11=np.pi, γL12=np.pi)
#    device = build_device(μL=0, μR=bias, γL=0, γR=0, γSF1=0, γL1=0, γL2=0, γL3=0, γL4=np.pi )
#    device = build_device(μL=0, μR=bias, γL=0, γR=0, γSF1=0, γL1=np.pi/4*2, γL2=np.pi/4*2, γL3=np.pi, γL4=np.pi )
#    device = build_device(μL=0, μR=bias, γL=0, γR=0, γSF1=0, γL1=np.pi/4, γL2=np.pi/4*2, γL3=np.pi/4*3, γL4=np.pi )
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

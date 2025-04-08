#!/bin/bash
#=============================================#
# Job Name

#SBATCH -J Pd6Co2_SupperLattice_NonColl_woSOCrelax

#---------------------------------------------#
# Computing resources

#SBATCH -A MST112204
#SBATCH -p ct56
#SBATCH -o job_%j.out
#SBATCH -e job_%j.err
#SBATCH --ntasks=28
#SBATCH --cpus-per-task=1

#---------------------------------------------#
# Setup environment variable
# Use `module avail` to see more

module purge
module load labstt/vasp/6.3.2_intel-2021

#=============================================#

cd $SLURM_SUBMIT_DIR

#--- Run your program here ---#

# available: vasp_gam | vasp_ncl | vasp_std
mpirun vasp_std

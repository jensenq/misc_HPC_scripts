#!/bin/bash
#SBATCH --qos=debug
#SBATCH --time=5
#SBATCH --nodes=1
#SBATCH --tasks-per-node=2
#SBATCH --cpus-per-task=16
#SBATCH --constraint=haswell

export OMP_PROC_BIND=true
export OMP_PLACES=cores
export OMP_NUM_THREADS=32

export PDUMP_EVENTS=PAPI_L1_DCM

module unload darshan
module load papi/5.6.0.6
module load hdf5-parallel/1.10.2
module load openmpi

mpirun ./warpx.exe inputs.3d

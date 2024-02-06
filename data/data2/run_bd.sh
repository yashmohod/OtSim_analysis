#!/bin/bash
#SBATCH --job-name="sph_test"
#SBATCH --output=sph_test.out
#SBATCH -t 8:00:00
#SBATCH --partition=shared
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --mem=2G
#SBATCH --export=ALL
#SBATCH --no-requeue
#SBATCH --account=ith101


source ./start
python3 pythonScript.py
python3 data_resize.py $1



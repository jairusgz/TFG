#!/bin/bash
#
#SBATCH --job-name=dqn
#SBATCH --output=dqn.out
#SBATCH --ntasks=1
#SBATCH --time=01:00

echo 'Running DQN'
python3 GUI.py

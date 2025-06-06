#!/bin/bash

#$ -P CRUISE
#$ -N xrl_g1_alignment
#$ -j y
#$ -m ea
#$ -M shuang.ao@unsw.edu.au
#$ -e /srv/scratch/CRUISE/shuang/results/$JOB_ID_$JOB_NAME.err
#$ -o /srv/scratch/CRUISE/shuang/results/$JOB_ID_$JOB_NAME.out
#$ -cwd
#$ -l walltime=30:00:00
#$ -l mem=80G
#$ -l jobfs=200G
#$ -l tmpfree=12G
#$ -l ngpus=1
#$ -pe smp 2
#$ -l gpu_model=H100_NVL
source ~/.bashrc

# ## setup conda environment
# __conda_setup="$('/srv/scratch/CRUISE/shuang/miniconda3/bin/conda' 'shell.bash' 'hook' 2> /dev/null)"
# if [ $? -eq 0 ]; then
#     eval "$__conda_setup"
# else
#     if [ -f "/srv/scratch/CRUISE/shuang/miniconda3/etc/profile.d/conda.sh" ]; then
#         . "/srv/scratch/CRUISE/shuang/miniconda3/etc/profile.d/conda.sh"
#     else
#         export PATH="/srv/scratch/CRUISE/shuang/miniconda3/bin:$PATH"
#     fi
# fi
# unset __conda_setup
#
cd /srv/scratch/CRUISE/shuang/code/emac
rm test.log
conda activate emac

python -c "import torch; print(torch.cuda.device_count())" >> test_gpu_1.log 2>&1
# python -c "import torch; print(torch.version.cuda)" >> test_gpu_cuda.log 2>&1

python -m torch.distributed.run --nproc_per_node=1 train.py --cfg-path ./lavis/projects/instructblip/finetuning/alfworld_ft.yaml >> train_eva_true.log 2>&1

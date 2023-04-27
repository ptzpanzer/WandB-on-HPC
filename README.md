# WandB-on-HPC
Run your wandb sweep on HPC-clusters using slurm

# Quick start:
1. set custom configs in myconfig.py
2. put training code in train() under test_solve.py (script name changeable by setting train_script_name in myconfig.py) the training result that you want wandb to log to its server should be saved in a JSON file as I did in the example.
3. run newstart.py and have a cup of coffee

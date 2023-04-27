# WandB-on-HPC
Run your W&B Sweep on HPC using Slurm

Some HPCs don't give their calculation nodes access to the Internet. Therefore setting a sweep could be painful. 

Here is a simple solution, separating the W&B Sweep control and the Slurm task submission.


# Quick start:
1. set custom configs in 'myconfig.py'

2. put training code in train() under 'test_solve.py' (script name changeable by setting 'train_script_name' in 'myconfig.py') 
     - the training result that you want W&B to log to its server should be saved in a JSON file as I did in the example.
     
3. set Slurm script template in 'slurm_wrapper.py'

4. run newstart.py on your HPC and have a cup of coffee

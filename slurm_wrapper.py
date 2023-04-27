import wandb
import subprocess
import os
import json
import time
import myconfig


# check echo from 'sacct' to tell the job status
def check_status(status):
    rtn = 'RUNNING'
    
    lines = status.split('\n')
    for line in lines:
        line = line.strip()
        if line == '':
            continue
        if 'FAILED' in line:
            rtn = 'FAILED'
            break
        elif 'COMPLETED' not in line:
            rtn = 'PENDING'
            break
    else:
        rtn = 'COMPLETED'
        
    return rtn


def wrap_task(config=None):
    # recieve config for this run from Sweep Controller
    with wandb.init(config=config):
        config = dict(wandb.config)
        
        # then build up the slurm script
        job_script = \
f"""#!/bin/bash
#SBATCH --job-name={myconfig.project_name}
#SBATCH --partition=dev_single
#SBATCH --error={myconfig.log_path}%x.%j.err
#SBATCH --output={myconfig.log_path}%x.%j.out
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user={myconfig.e_mail}
#SBATCH --export=ALL

eval \"$(conda shell.bash hook)\"
conda activate {myconfig.conda_env}

job_id=$SLURM_JOB_ID
python {myconfig.train_script_name} $job_id '{json.dumps(config)}'
"""
        
        # Write job submission script to a file
        with open(myconfig.slurm_scripts_path + f"{wandb.run.name}.sbatch", "w") as f:
            f.write(job_script)
        
        # Submit job to Slurm system and get job ID
        cmd = "sbatch " + myconfig.slurm_scripts_path + f"{wandb.run.name}.sbatch"
        output = subprocess.check_output(cmd, shell=True).decode().strip()
        job_id = output.split()[-1]
        
        # Wait for job to finish
        while True:
            time.sleep(20)
            cmd = f"sacct -n --format=state -j {job_id}"
            status = subprocess.check_output(cmd, shell=True).decode()
            check_byte = check_status(status)
            print(f'{job_id}: {check_byte}')
            if check_byte == "COMPLETED" or status == "FAILED":
                break
    
        # Read calculation result from the output file
        output_file = os.path.join(os.getcwd(), myconfig.log_path + f'{job_id}.rtn')
        with open(output_file, "r") as f:
            result = f.read()
            rtn_dict = json.loads(result)
            
        # Print calculation result
        print(f"Calculation result: {rtn_dict['best_err']}")
        # sync to wandb
        wandb.log({"best_err": rtn_dict['best_err']})
        wandb.finish()
            
if __name__ == '__main__':
    wrap_task()

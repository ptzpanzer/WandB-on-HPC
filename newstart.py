import wandb
import yaml
import os
from multiprocessing import Pool
import myconfig


def build_folder_and_clean(path):
    check = os.path.exists(path)
    if check:
        for root, dirs, files in os.walk(path, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
    else:
        os.makedirs(path)


# define & save the yaml file for wandb sweep
def make_para_yaml(project_name, slurm_wrapper, scripts_path, sweep_config):
    # make the yaml file
    with open(scripts_path + 'sweep_params.yaml', 'w') as outfile:
        yaml.dump(sweep_config, outfile, default_flow_style=False)
        

def agent_wrapper(arg):
    return wandb.agent(**arg)


if __name__ == "__main__":
    # login to wandb
    wandb.login(key=myconfig.api_key)
    
    # prepare working folders
    build_folder_and_clean(myconfig.slurm_scripts_path)
    build_folder_and_clean(myconfig.log_path)

    # generate & load sweep config
    make_para_yaml(myconfig.project_name, myconfig.slurm_wrapper_name, myconfig.slurm_scripts_path, myconfig.sweep_config)
    with open(myconfig.slurm_scripts_path + 'sweep_params.yaml') as file:
        config_dict = yaml.load(file, Loader=yaml.FullLoader)

    # start sweep
    sweep_id = wandb.sweep(sweep=config_dict)
    pool = Pool(myconfig.pool_size)
    kwarg = {'sweep_id': sweep_id, 'count': 1}
    arg = [kwarg for i in range(myconfig.total_sweep)]
    pool.map(agent_wrapper, arg)
    pool.close()
    pool.join()

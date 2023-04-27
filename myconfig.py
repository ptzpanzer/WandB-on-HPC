# wandb api key
api_key = 'CUSTOMIZE_YOUR_KEY_HERE'


# where should the intermedia generated scripts be saved (automatically cleaned at the start of each run)
slurm_scripts_path = './slurm_scripts/'
# where should the outputs & logs be saved (automatically cleaned at the start of each run)
log_path = './logs/'


# project name on wandb and HPC
project_name = 'YOUR_PROJ_NAME'
# e-mail address to recieve notifications
e_mail = 'E@MAIL.COM'
# conda location
conda_env = 'A_CONDA_ENV_PATH'
# file name of the slurm_wrapper, don't change this if you haven't write a new one
slurm_wrapper_name = './slurm_wrapper.py'
# file name of the training code
train_script_name = './test_solve.py'


# define custom sweep hyperparameters
#     - how many sweeps do you want to run in total
total_sweep = 6
#     - how many sweeps do you want to run parallelly
pool_size = 3


# define wandb sweep parameters
#     - project definition
sweep_config = {
    "project": project_name,
    'program': slurm_wrapper_name,
    "name": "offline-sweep",
    'method': 'bayes'
}
#     - metric definition
metric = {
    'name': 'best_err',
    'goal': 'minimize'   
}
sweep_config['metric'] = metric
#     - parameters search range definition
parameters_dict = {
    'lr': {
        'values': [1e-4, 1e-5, 1e-6]
    },
    'embedding_dim': {
        'values': [128, 256, 512]
    },
    'embedding_hidden_layers': {
        'values': [1, 2, 4]
    },
    'feedforward_dim': {
        'values': [512, 1024, 2048]
    },
    'num_head': {
        'values': [2, 4, 8]
    },
    'num_layers': {
        'values': [4, 5, 6]
    },
    'output_hidden_layers': {
        'values': [2, 4, 6]
    },
    'dropout': {
        'values': [0.1, 0.25, 0.5]
    },
}
sweep_config['parameters'] = parameters_dict

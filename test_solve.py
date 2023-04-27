import sys
import json
import time
import myconfig


def train(config, out_path, job_id):
    best_err = config['feedforward_dim'] * config['dropout']
    time.sleep(120)
    
    # collect wandb result into file
    rtn = {"best_err": best_err}
    json_dump = json.dumps(rtn)
    with open(out_path + f'{job_id}.rtn', 'w') as fresult:
        fresult.write(json_dump)


if __name__ == '__main__':
    job_id = sys.argv[1]
    config = json.loads(sys.argv[2])
    
    # set work folder
    train(config, myconfig.log_path, job_id)
    
import pandas as pd

def process(confs, args):
    # Get confs
    read_path = confs["envs"][confs["active_env"]]["read"]

    main_df = pd.read_csv(f"{read_path}/sample_data.csv")

    return [main_df]

import pandas as pd

def process(confs, variables):
    # Get confs
    read_path = confs["envs"][confs["active_env"]]["read"]

    main_df = pd.read_csv(f"{read_path}/sample_data.csv")

    variables.main_df = main_df
    variables.test_number = 10

    return

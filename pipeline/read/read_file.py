import pandas as pd
from tools.engine import variables_storage

def process(pipe):
    # Get confs
    read_path = pipe.__confs__["envs"][pipe.__confs__["active_env"]]["read"]

    var_str = variables_storage()
    main_df = pd.read_csv(f"{read_path}/sample_data.csv")
    var_str.update("main_df", main_df)

    return

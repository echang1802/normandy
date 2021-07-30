import pandas as pd
from engine.variables_storage import variables_storage

def process(pipe, log):
    # Get confs
    read_path = pipe.get_env_confs()["read"]
    var_str = variables_storage()
    log.info("Configuration ready")

    main_df = pd.read_csv(f"{read_path}/sample_data.csv")
    log.info("Data readed")

    var_str.update("main_df", main_df)
    log.info("Data stored")

    return

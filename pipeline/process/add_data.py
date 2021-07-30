import pandas as pd
from engine.variables_storage import variables_storage

def process(pipe, log):
    # Get confs
    write_path = pipe.get_env_confs()["write"]
    var_str = variables_storage()
    log.info("Configuration ready")

    main_df = var_str.get("main_df").describe()
    log.info("Data recupered")

    main_df = main_df.append(pd.DataFrame({
        "foo" : [2,2,2],
        "bar" : [9,10,11]
    }))

    main_df.to_csv(f"{write_path}/data_extra.csv")
    log.info("Process ready")

    return

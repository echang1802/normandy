
from tools.engine import variables_storage

def process(pipe):
    # Get confs
    write_path = pipe.__confs__["envs"][pipe.__confs__["active_env"]]["write"]
    var_str = variables_storage()

    main_df = var_str.get("main_df").describe()

    var_str.update("main_df", main_df)

    main_df.to_csv(f"{write_path}/sample_process.csv")

    return

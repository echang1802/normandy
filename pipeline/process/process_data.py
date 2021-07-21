

def process(confs, variables):
    # Get confs
    write_path = confs["envs"][confs["active_env"]]["write"]

    main_df = variables.main_df.describe()
    variables.main_df = main_df
    variables.test_number += 10

    main_df.to_csv(f"{write_path}/sample_process.csv")

    return

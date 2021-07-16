

def process(confs, args):
    # Parse args
    main_df = args[0]

    # Get confs
    write_path = confs["envs"][confs["active_env"]]["write"]

    main_df = main_df.describe()

    main_df.to_csv(f"{write_path}/sample_process.csv")

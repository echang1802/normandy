import pandas as pd

def process(confs, args):
    # Parse args
    main_df = args[0]

    # Get confs
    write_path = confs["envs"][confs["active_env"]]["write"]

    main_df = main_df.append(pd.DataFrame({
        "id" : [6,7,8],
        "foo" : [2,2,2],
        "bar" : [9,10,11]
    }))

    main_df.to_csv(f"{write_path}/data_extra.csv")

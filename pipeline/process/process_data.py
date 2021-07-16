

def process(args):
    # Parse args
    print(args)
    main_df = args[0]

    main_df = main_df.describe()

    main_df.to_csv("sample_process.csv")

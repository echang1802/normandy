import pandas as pd

def process(args):

    main_df = pd.read_csv("raw/sample_data.csv")

    return [main_df]

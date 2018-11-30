import pandas as pd
pd.options.display.max_rows = None

df = pd.read_csv('../data/original_data.csv')
df1 = df.iloc[:len(df)//6, :]
df2 = df.iloc[len(df)//6:, :]
df1.to_csv('../data/data_simulation.csv', index=False)
df2.to_csv('../data/data_training.csv', index=False)

import pandas as pd


KEPLER_COLUMNS=["koi_pdisposition",
                ]

df_kepler=pd.read_csv("data/kepler.csv", comment="#")
df_k2=pd.read_csv("data/k2.csv", comment="#")
df_tess=pd.read_csv("data/tess.csv", comment="#")

print(len(df_kepler), len(df_k2), len(df_tess))
print(df_kepler.columns, df_k2.columns, df_tess.columns, sep="\n")

import pandas as pd


df = pd.read_csv('./datasets/medical_qs_all.csv')
df = df.dropna(axis=0)
print(df.info())
df= df[['medical_qs', 'department']]
print(df.info())
df.to_csv('./datasets/medical_qs_all_drop_nun.csv', index=False)
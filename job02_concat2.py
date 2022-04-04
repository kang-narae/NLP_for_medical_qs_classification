import pandas as pd
import glob
data_paths = glob.glob('./notwell/*')
print(data_paths)
for path in data_paths:
    df_temp = pd.read_csv(path)
    # print(df_temp)
    l = df_temp.shape[1]
    j = int(l/3)
    df = pd.DataFrame()
    for i in range(1,j):  # 1~10
            a = (i - 1) * 3
            b = a+1
            c = b+1
            globals()['family_{}'.format(i)] = df_temp[[str(a), str(b), str(c)]]
            k = globals()['family_{}'.format(i)]
            k.columns = ['title', 'content', 'department']
            # print(globals()['family_{}'.format(i)].head())
            df = pd.concat([df, k], ignore_index=True)
    print(df.head())
    df.info()
    name = path[10:]
    # df.to_csv(f'./notwell/1{name}', index = False)
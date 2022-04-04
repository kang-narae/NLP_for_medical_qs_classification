import pandas as pd
import glob
data_paths = glob.glob('./datasets/nonwell/*')
df = pd.DataFrame()
for paths in data_paths:
    paths = glob.glob(paths)
    for path in paths:
        path = glob.glob(path+'/*')
        print(path)
        for i in path:
            print(i)
            df_temp = pd.read_csv(i)
            # df_temp = df_temp.reset_index()
            df_temp.columns = ['index','title','content','department']
            df_temp= df_temp.drop(['index'], axis = 1)
            print(df_temp.head())
            print(df_temp.info())
            df_temp.columns = ['title', 'content', 'department']
            df = pd.concat([df, df_temp], axis='rows')


# print(df.head())
# df.info()
# #
df.to_csv('./datasets/concat_all_nunwell.csv', index = False)
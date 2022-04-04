import pandas as pd

family = pd.read_csv('./datasets/medical_qs_17_Family100.csv')
print(family.head())


for i in range(1, 11):  # 1~10
        a = (i - 1) * 3
        b = a+1
        c = b+1
        globals()['family_{}'.format(i)] = family[[str(a), str(b), str(c)]]
        print(globals()['family_{}'.format(i)].head())
        k = globals()['family{}'.format(i)]
        k.columns= ['title', 'content', 'department']
        k.to_csv('./datasets/family/family_'+str(i)+'.csv')
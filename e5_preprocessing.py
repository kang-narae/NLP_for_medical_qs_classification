import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.utils import to_categorical
import pickle
from konlpy.tag import Okt


pd.set_option('display.unicode.east_asian_width', True)
df = pd.read_csv('./datasets/medical_qs_all_drop_nun_drop_family_change_female.csv')
# print(df.head())
# print(df.category.value_counts())
df.info()

X = df.medical_qs  # 이러면 시리즈야
Y = df.department
#df로 바꾸려면 이차원 이어야하니까

# X= df[['medical_qs']]
# Y = df[['department']]

encoder = LabelEncoder()   #라벨 인코더 객체를 만들어서
labeled_Y = encoder.fit_transform(Y)   # 인코더 객체가 Y를 가지고 라벨인코딩을 한 객체가 labeled_Y. Y의 결과값이 인코딩이 됐지.
# print(encoder.classes_)
# print(labeled_Y[:5])
with open('./output/encoder_tuesday.pickle', 'wb') as f:
    pickle.dump(encoder, f)

onehot_Y = to_categorical(labeled_Y)
# print(onehot_Y)

okt = Okt()
# x = []
for i in range(len(X)):          #X는 qs.  len(X)는 medical_qs의 개수.
   X[i] = okt.morphs(X[i], stem=True)          #각 qs를 형태소 분리해라

stopwords= pd.read_csv('./stopwords/stopwords.csv', index_col=0)

for j in range(len(X)):
   words =[]
   for i in range(len(X[j])):          # X[j]는 qs 하나하나. len(X[j])는 각 qs의 길이 (형태소 개수)
      if len(X[j][i]) > 1:  #두글자부터만 보겠다
         if X[j][i] not in list(stopwords['stopword']):  #그중에서도 불용어에 포함 안 되는 애들만
            words.append(X[j][i])
   X[j] = ' '.join(words)  #각 qs를 불용어 제외한 토큰들로 대체한다.
print(X[1])

token = Tokenizer()
token.fit_on_texts(X)   # 이 X안에 있는 모든 토큰화된 단어를 찾아서 라벨링을 해줌. 그래서 X의 다른 row의 같은 단어는 같은 라벨링임. 딕셔너리로 하고.
  #fit_on_texts를 했으니까 token객체에 X의 변환된 정보 딕셔너리가 들어가 있음. 이 token을 저장함.
  #tokened_X는 아직 저장안해. 전처리 해줘야함. 길이도 맞춰야하고 트레이닝 셋 테스트셋 나누기도 해야하고.

tokened_X = token.texts_to_sequences(X)   #리스트로 들어감.
print(tokened_X[1])

with open('./output/medical_token_tuesday.pickle', 'wb') as f:
   pickle.dump(token, f)   #피클로 토큰 저장해놓자 .. 근데 왜 token만 저장 ? tokened_X가 아니고? 나중에 쓸 거라서.

wordsize = len(token.word_index) + 1   #토큰해놓은 건 인덱스는 0없고 1부터인데, 우리가 0을 쓸 거라서 (?) +1을 함. 문장 자리수 맞추려고 앞에 0 채우는 거임.

print('wordsize', wordsize)
# print(token.word_index)

max = 0
for i in range(len(tokened_X)):
   if max < len(tokened_X[i]):
      max = len(tokened_X[i])
print(max)          #max는 X(medical_qs)의 토큰의 개수.


X_pad = pad_sequences(tokened_X, max)
print(X_pad[:5])

X_train, X_test, Y_train, Y_test = train_test_split(
   X_pad, onehot_Y, test_size = 0.1)

print(X_train.shape, Y_train.shape)
print(X_test.shape, Y_test.shape)

xy= X_train, X_test, Y_train, Y_test
np.save('./crawling_data/medical_qs_max_{}_wordsize_{}_tuesday'.format(max,wordsize), xy)



# X.apply(okt.morphs(X))
# okt_morph_X= okt.morphs(X[1], stem=True)    #stem=True 주면 원형(표제어)로 줌. 원형으로 만들어진 걸로 학습시킬 수 있지.
# print(X[1])
# print(okt_morph_X)
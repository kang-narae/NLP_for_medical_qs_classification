import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import QPixmap
from tensorflow.keras.models import load_model
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.utils import to_categorical
import pickle
from konlpy.tag import Okt

form_window = uic.loadUiType('./app.ui')[0]

class Exam(QWidget, form_window):
    def __init__(self):
        super().__init__()
        self.path = None
        self.setupUi(self)
        self.model = load_model('./output/medical_qs_classification_model_0.623869776725769_change_female_dentist.h5')

        self.btn_input.clicked.connect(self.predict_department)  #btn_input 클릭하면 predict_department 함수 실행

    def predict_department(self):
        input_text = self.input_text.toPlainText()  #인풋텍스트에서 받은 거


        try:
            okt = Okt()  # 형태소 기준으로 나눠주는 함수, 종류가 5개 -> 결국 다 사용해서 5번 돌린다. open korea token


            X = okt.morphs(input_text, stem=True)  # stem=True-> 원형으로 만들어주기(ex.접었다->접다)
            print(X)

            stopwords = pd.read_csv('./stopwords/stopwords.csv',
                                    index_col=0)  # 아주 기본적인 불용어 리스트 불러오기, 데이터의 종류에 따라 불용어는 달라진다.

            words = []
            for i in range(len(X)):
                if len(X[i]) > 1:  # 글자의 크기가 1 이하는 제외
                    if X[i] not in list(stopwords['stopword']):  # 불용어에 속하면 제외
                        words.append(X[i])
            X = ' '.join(words)
            print(X)

              # X 안의 모든 형태소를 찾아서 unique한 값(숫자)을 부여 dict 형태, token 안에 변환된 dict 정보가 저장되어 있다.
            with open('./output/medical_token_change_female_dentist.pickle', 'rb') as f:
                print('debug01')
                token = pickle.load(f)
                print('debug02')
            print('debug03')
            tokened_X = token.texts_to_sequences([X])  # 토큰화된 X를 리스트로 넣어서, 숫자로 된 list 화 .
            print('debug04')
            print(tokened_X)
            X_pad = pad_sequences(tokened_X, 816)   # 0 채우고
            print(X_pad)
            predict_value = self.model.predict(X_pad)   # X_pad 예측 돌린 값
            print(predict_value)
        except:
            print('error')
        self.input_label.setText(predict_value)   #인풋라벨에다가 넣는다

app = QApplication(sys.argv)
mainWindow = Exam()
mainWindow.show()
sys.exit(app.exec_())
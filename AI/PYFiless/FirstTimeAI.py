###########################
# 라이브러리 사용
import tensorflow as tf
import pandas as pd
import numpy as np
import math
import os
            
###########################
# 모델을 저장할 폴더 생성
def createDirectory(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print("good")
    except OSError:
        print("Error: Failed to create the directory.")
        
def FirstTimeAI(heatFeelLevel, filename, firstValue, secondValue, thirdValue, fourthValue):
    ###########################
    # 0. 각종 구조체 및 변수 처리
    # heatFeelLevel 더위 정도를 나타내는 변수. 0 = 안탐, 1 = 보통, 2 = 많이탐
    # filename = "MyfanStrong" 안드로이드 프로필로부터 받아온 프로필 이름. csv파일 제작에 사용.
    print("Start")
    print("1. 안드로이드 프로필 내용 활용 csv 읽기, Start")
    RaspberryLink = "/home/pi/AI"        # 라즈베리 폴더 위치 : /home/pi/AI/
    CSVsavelink = RaspberryLink + "/ProfileCSV/profile_" + filename + ".csv"
    CSVbackuplink = RaspberryLink + "/ProfileCSV/profile_" + filename + "_backup.csv"
    BasicModelSavelink = RaspberryLink + "/BasicModelFile/profile_"
    ModelSavelink = RaspberryLink + "/ModelFile/profile_" + filename
    ModelBackuplink = RaspberryLink + "/ModelFile/profile_" + filename +"_backup"
     
    ###########################
    # 1. 안드로이드 프로필 내용 활용 csv 읽기
    # 처음 사용할 시 지정한 더위 정도.
    if heatFeelLevel == 0: # 더위 안탐 (Storng)
        CSVfile_origin = pd.read_csv(RaspberryLink + "/BasicCSV/Bstrong.csv")
    elif heatFeelLevel == 1: # 더위 보통 (normal)
        CSVfile_origin = pd.read_csv(RaspberryLink + "/BasicCSV/Bnormal.csv")
    else : # 더위 많이탐 (weak)
        CSVfile_origin = pd.read_csv(RaspberryLink + "/BasicCSV/Bweak.csv")

    # 프로필 맞춤 원본과 백업 파일 생성.
    CSVfile_origin.to_csv(CSVsavelink, header = ['Power','InTemp','OutTemp','InHumi','OutHumi'], index = False)
    CSVfile_origin.to_csv(CSVbackuplink, header = ['Power','InTemp','OutTemp','InHumi','OutHumi'], index = False)
        
    CSVfile = pd.read_csv(CSVsavelink)
        
    print("1. 안드로이드 프로필 내용 활용 csv 읽기, Finish")
    ###########################
    # 2. 독립, 종속 변수 분리
    print("2. 독립, 종속 변수 분리, Start")
    indep = CSVfile[['InTemp','OutTemp','InHumi','OutHumi']]
    dep = CSVfile[['Power']]

    print(indep.shape, dep.shape)
    
    print("2. 독립, 종속 변수 분리, Finish")
    ###########################
    # 3. 모델 구조 만들기.
    print("3. 모델 구조 만들기, Start")
    X = tf.keras.layers.Input(shape=[4])
    Y = tf.keras.layers.Dense(1)(X)
    
    print("3. 모델 구조 만들기, Finish")
    ###########################
    # 4. 베이직 모델 불러오기
    # 맨 초기 csv 값은 모두 같기 때문에 베이직 모델 사용.
    print("4. 베이직 모델 불러오기, Start")
    if heatFeelLevel == 0: # 더위 안탐 (Storng)
        model = tf.keras.models.load_model(BasicModelSavelink + "MyfanStrong" )
    elif heatFeelLevel == 1: # 더위 보통 (normal)
        model = tf.keras.models.load_model(BasicModelSavelink + "MyfanNormal" )
    else : # 더위 많이탐 (weak)
        model = tf.keras.models.load_model(BasicModelSavelink + "MyfanWeak" )
        
    print("4. 베이직 모델 불러오기, Finish")
    ###########################
    # 5. 모델 이용.
    # 순서대로 'InTemp','OutTemp','InHumi','OutHumi' 값 받아온것 집어넣기.
    # ytest는 자동으로 측정된 값. 이 값을 올림으로 y로 만든뒤, os로 보내서 선풍기 풍속제어를 할 예정.
    print("5. 모델 이용, Start")
    ytest = model.predict([[firstValue, secondValue, thirdValue, fourthValue]])
    print(ytest)
    y = math.ceil(ytest)
    if y > 20 :
        y = 20

    ###########################################
    # 모델 이용 테스트 파트.
    # weak, normal, strong 순으로 총 세개로 나뉘어져 있음
    # 즉, 지워도 무관.


    # weak 테스트
    ytest1 = model.predict([[19.5, 20, 25, 20]])
    ytest2 = model.predict([[19.7,20,44,40]])
    ytest3 = model.predict([[20.2,20,65,60]])
    ytest4 = model.predict([[21,20,81,80]])
    ytest5 = model.predict([[20.1,21,24,20]])
    ytest6 = model.predict([[20.4,21,46,40]])
    ytest7 = model.predict([[31.8,32,31,30]])
    ytest8 = model.predict([[31.5,32,50,50]])
    ytest9 = model.predict([[32.1,32,65,60]])
    ytest10 = model.predict([[33.5,32,85,80]])
    ytest11 = model.predict([[31,32,69,70]])

    y1 = math.ceil(ytest1)
    y2 = math.ceil(ytest2)
    y3 = math.ceil(ytest3)
    y4 = math.ceil(ytest4)
    y5 = math.ceil(ytest5)
    y6 = math.ceil(ytest6)
    y7 = math.ceil(ytest7)
    y8 = math.ceil(ytest8)
    y9 = math.ceil(ytest9)
    y10 = math.ceil(ytest10)
    y11 = math.ceil(ytest11)

    print("원래 값, 예측 올림값, 예측값.")
    print("5, ",y1 , ytest1)
    print("5, ",y2 , ytest2)
    print("5, ",y3 , ytest3)
    print("5, ",y4 , ytest4)
    print("5, ",y5 , ytest5)
    print("5, ",y6 , ytest6)
    print("10, ",y7 , ytest7)
    print("10, ",y8 , ytest8)
    print("15, ",y9 , ytest9)
    print("15, ",y10 , ytest10)
    print("15, ",y11 , ytest11)

    '''
    # normal 테스트
    ytest1 = model.predict([[19.5, 20, 25, 20]])
    ytest2 = model.predict([[19.7,20,44,40]])
    ytest3 = model.predict([[20.2,20,65,60]])
    ytest4 = model.predict([[21,20,81,80]])
    ytest5 = model.predict([[20.1,21,24,20]])
    ytest6 = model.predict([[20.4,21,46,40]])
    ytest7 = model.predict([[32.1,32,35,30]])
    ytest8 = model.predict([[31.3,32,23,20]])
    ytest9 = model.predict([[32.3,32,88,90]])
    ytest10 = model.predict([[34.2,34,88,90]])
    ytest11 = model.predict([[35.2,36,68,70]])

    y1 = math.ceil(ytest1)
    y2 = math.ceil(ytest2)
    y3 = math.ceil(ytest3)
    y4 = math.ceil(ytest4)
    y5 = math.ceil(ytest5)
    y6 = math.ceil(ytest6)
    y7 = math.ceil(ytest7)
    y8 = math.ceil(ytest8)
    y9 = math.ceil(ytest9)
    y10 = math.ceil(ytest10)
    y11 = math.ceil(ytest11)

    print("원래 값, 예측 올림값, 예측값.")
    print("5, ",y1 , ytest1)
    print("5, ",y2 , ytest2)
    print("5, ",y3 , ytest3)
    print("5, ",y4 , ytest4)
    print("5, ",y5 , ytest5)
    print("5, ",y6 , ytest6)
    print("10, ",y7 , ytest7)
    print("10, ",y8 , ytest8)
    print("15, ",y9 , ytest9)
    print("15, ",y10 , ytest10)
    print("15, ",y11 , ytest11)
    '''
    '''
    # strong 테스트
    ytest1 = model.predict([[19.5, 20, 25, 20]])
    ytest2 = model.predict([[19.7,20,44,40]])
    ytest3 = model.predict([[20.2,20,65,60]])
    ytest4 = model.predict([[21,20,81,80]])
    ytest5 = model.predict([[20.1,21,24,20]])
    ytest6 = model.predict([[20.4,21,46,40]])
    ytest7 = model.predict([[26.9,27,90,80]])
    ytest8 = model.predict([[33.4,33,67,60]])
    ytest9 = model.predict([[37.2,37,88,80]])
    ytest10 = model.predict([[37.6,38,66,70]])
    ytest11 = model.predict([[40,41,19,20]])

    y1 = math.ceil(ytest1)
    y2 = math.ceil(ytest2)
    y3 = math.ceil(ytest3)
    y4 = math.ceil(ytest4)
    y5 = math.ceil(ytest5)
    y6 = math.ceil(ytest6)
    y7 = math.ceil(ytest7)
    y8 = math.ceil(ytest8)
    y9 = math.ceil(ytest9)
    y10 = math.ceil(ytest10)
    y11 = math.ceil(ytest11)

    print("원래 값, 예측 올림값, 예측값.")
    print("5, ",y , ytest)
    print("===============")
    print("5, ",y1 , ytest1)
    print("5, ",y2 , ytest2)
    print("5, ",y3 , ytest3)
    print("5, ",y4 , ytest4)
    print("5, ",y5 , ytest5)
    print("5, ",y6 , ytest6)
    print("10, ",y7 , ytest7)
    print("10, ",y8 , ytest8)
    print("15, ",y9 , ytest9)
    print("15, ",y10 , ytest10)
    print("15, ",y11 , ytest11)
    '''
    print("5. 모델 이용, Finish")
    
    
    ###########################
    # 5. 모델 및 CSV 저장

    # 모델 저장 구문
    createDirectory(ModelSavelink)
    model.save(ModelSavelink)
    model.save(ModelBackuplink)
    
    return y
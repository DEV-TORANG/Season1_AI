###########################
# 라이브러리 사용
import tensorflow as tf
import pandas as pd
import numpy as np
import math
import csv
import os


###########################
# 모델 업데이트       
def ModelUpdate(filename):
    
    CSVsavelink = "/home/pi/AI/ProfileCSV/profile_" + filename + ".csv"
    CSVbackuplink = "/home/pi/AI/ProfileCSV/profile_" + filename + "_backup.csv"
    ModelSavelink = "/home/pi/AI/ModelFile/profile_" + filename
    ModelBackuplink = "/home/pi/AI/ModelFile/profile_" + filename +"_backup"
    
    CSVfile = pd.read_csv(CSVsavelink)

    indep = CSVfile[['InTemp','OutTemp','InHumi','OutHumi']]
    dep = CSVfile[['Power']]

    X = tf.keras.layers.Input(shape=[4])
    Y = tf.keras.layers.Dense(1)(X)
    
    model = tf.keras.models.Model(X, Y)
    model.compile(loss='mse') # mse는 로스값.
    model.fit(indep, dep, epochs = 1000, verbose = 0)
    model.fit(indep, dep, epochs = 1000)

    model.save(ModelSavelink)
    model.save(ModelBackuplink)
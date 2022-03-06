###########################
# 라이브러리 사용
import tensorflow as tf
import pandas as pd
import numpy as np
import math
import csv
import os

def CSVupdate(filename, pressValue, firstValue, secondValue, thirdValue, fourthValue):
    count = 0 # 처음 사용하는가 아닌가를 구분하는 변수.
    heatFeelLevel = 0 # 더위 정도를 나타내는 변수. 0 = 안탐, 1 = 보통, 2 = 많이탐
    CSVsavelink = "/home/pi/AI/ProfileCSV/profile_" + filename + ".csv"
    CSVbackuplink = "/home/pi/AI/ProfileCSV/profile_" + filename + "_backup.csv"
    ModelSavelink = "/home/pi/AI/ModelFile/profile_" + filename
    ModelBackuplink = "/home/pi/AI/ModelFile/profile_" + filename +"_backup"
    
    CSVfile = open(CSVsavelink,'a', newline='')
    writer = csv.writer(CSVfile)
    writer.writerow([pressValue, firstValue, secondValue, thirdValue, fourthValue])
 
    CSVfile.close()
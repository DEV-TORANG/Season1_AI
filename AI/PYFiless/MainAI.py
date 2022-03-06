#-*- coding:utf-8 -*-

###########################
# 라이브러리 사용
import multiprocessing as mp
import tensorflow as tf
import pandas as pd
import numpy as np
import math
import os

import time

import FirstTimeAI
import AfterTimeAI
import CSVupdate
import WriteAndReadTXT

import api
import MotorCopy
import DHT22_Confirm
import Modelupdate

# API, 온습도 실행 스레드
# Main 돌아갈 스레드
# 블루투스 입출력 스레드
    
#####################################################
# 1. 메인에서 사용할 오토/수동모드 함수
# 오토 모드를 선택했을때 실행되는 함수.

def AutoMode(Firsttime, heatFeelLevel, APITemp, APIHumi, filename):
     # 내부 온도(온습도), 내부 습도(온습도)
    firstValue, thirdValue = DHT22_Confirm.DHTvalues()
    # 외부 온도(API), 외부 습도(API)
    secondValue = float(APITemp)
    fourthValue = float(APIHumi)
    # secondValue, fourthValue = api.API_measurement()    

                                                                                                                                                   # 테스트 문자들. 지워도 무관.-----------------
    #firstValue = 20.9
    #secondValue = 21
    #thirdValue = 61
    #fourthValue = 60
    #---------------------------------------------
            
    # 첫 시동인가 아닌가.
    if Firsttime == "1":
        pressValue = FirstTimeAI.FirstTimeAI(heatFeelLevel, filename, firstValue, secondValue, thirdValue, fourthValue)
    else:
        pressValue = AfterTimeAI.AfterTimeAI(filename, firstValue, secondValue, thirdValue, fourthValue)
    
    MotorCopy.setReceivedFanSpeed(pressValue)
    WriteAndReadTXT.WriteforAndroid_auto(APIHumi, APIHumi, pressValue)
    
    # 5분마다 재실행.
    print("5분 대기 후 AI 재실행")
    time.sleep(1)

# 오토 모드를 껐을때 실행되는 함수.
def PassiveMode(pressValue, APITemp, APIHumi, filename):
    # 일단은 테스트 값. 이후 API 및 온습도 센서 값으로 대체.
    # 내부 온도(온습도), 내부 습도(온습도)
    RaspberryLink = "/home/pi/AI" 
    CSVsavelink = RaspberryLink + "/ProfileCSV/profile_" + filename + ".csv"
    CSVbackuplink = RaspberryLink + "/ProfileCSV/profile_" + filename + "_backup.csv"
    
    firstValue, thirdValue = DHT22_Confirm.DHTvalues()
    secondValue = APITemp
    fourthValue = APIHumi
    
    print(pressValue)
    
    MotorCopy.setReceivedFanSpeed(pressValue)
    
    
    '''
    if os.path.exists(CSVsavelink) == True:
        
        th = mp.Process(target = CSVupdate.CSVupdate(), args=(filename, pressValue, firstValue, secondValue, thirdValue, fourthValue))
        th.start()
        th.join()
        
        
    '''

#####################################################
# 2. 변수 설정 및 메인

## startValue 
## powerOnOff 켜져있을때 1, 꺼져있을때 0
## CheckAuto 오토 모드일때 1, 수동 모드일때 0
## Firsttime 프로필이 처음 시동인지 아닌지를 나타내는 변수
# 1이라면 맞다, 0이라면 아니다.
## heatFeelLevel 프로필이 처음 시동일때, 원하는 온도 값.
# 0 = strong, 1 = normal, 2 = weak
## filename 프로필의 이름.
## pressValue 바뀐 풍속 값.

print("start")

Cnt = 0
startValue = 0
APITemp = 00.0
APIHumi = 00.0

while startValue != 1:
    if startValue == 1 :
        break
    powerOnOff, CheckAuto, a, b, c, d, e= WriteAndReadTXT.ReadforOS()
    startValue = powerOnOff
    print("Raspberry is not ready.")
    time.sleep(1)


print("start, Check TEMP,HUMI")

# 내부 온도(온습도), 내부 습도(온습도)
firstValue, thirdValue = DHT22_Confirm.DHTvalues()
# 외부 온도(API), 외부 습도(API)
secondValue = APITemp
fourthValue = APIHumi
# secondValue, fourthValue = api.API_measurement()  

WriteAndReadTXT.WriteforAndroid(APITemp, APIHumi)

print("start, Main Process")

powerOnOff = 1
while powerOnOff != 0 :
    if powerOnOff == 0 :
        break
    powerOnOff, CheckAuto, a, b, c, d, e = WriteAndReadTXT.ReadforOS()
    print("powerOnOff :: ", powerOnOff )
    if powerOnOff == 1:
        if CheckAuto == 1:
            if a == "1":
                Firsttime = a
                heatFeelLevel = b
                APITemp = c
                APIHumi = d
                filename = e
            else :
                heatFeelLevel = 0
                Firsttime = a
                APITemp = b
                APIHumi = c
                filename = d
        else :
            pressValue = a
            APITemp = b
            APIHumi = c
            filename = d
    else :
        powerOnOff = 0
        
    # 켜져있을때 동안 실행하라.
    if powerOnOff == 1:
        # 만약 오토 모드라면, 실행
        if CheckAuto == 1:
            print("Auto Start")
            AutoMode(Firsttime, heatFeelLevel, APITemp, APIHumi, filename)
                
        # 오토 모드가 아니라면, 실행. (수동 모드)
        else :
            print("Passive Start")
            # 오토인지 아닌지 체크.
            # 오토가 아니라면 계속 반복.
            
            # 안드로이드로 값을 보낼 함수.
            if Cnt == 15 :
                # Cnt가 15가 되면 API, 온습도값을 안드로이드로 보내기.
                WriteAndReadTXT.WriteforAndroid(APITemp, APIHumi)
                CSVupdate.CSVupdate(filename, pressValue, firstValue, secondValue, thirdValue, fourthValue)
                Cnt = 0
            # 만약 오토모드가 됬다면 중단.
            if CheckAuto == 1 :
                break
                
            else:
                # inValue 읽기 반복..
                powerOnOff, CheckAuto, a, b, c, d, e = WriteAndReadTXT.ReadforOS()
                # 만약 전원이 켜져있다면,
                if powerOnOff == 1:
                    # 만약 오토모드 일 경우에,
                    if CheckAuto == 1:
                        # a 값이 1인 경우, (처음 사용하는 경우.)
                        if a == 1:
                            Firsttime = a
                            heatFeelLevel = b
                            APITemp = c
                            APIHumi = d
                            filename = e
                        # a 값이 0인 경우, (처음 사용이 아닌 경우.)
                        else :
                            Firsttime = a
                            APITemp = b
                            APIHumi = c
                            filename = d
                    # 만약 수동모드 일 경우에,
                    else :
                        pressValue = a
                        APITemp = b
                        APIHumi = c
                        filename = d
                # 만약 전원이 꺼져있다면,
                else :
                    powerOnOff = 0
                
            print("Passive Fin")
            PassiveMode(int(pressValue), APITemp, APIHumi, filename)
            Cnt += 1
            print("Cnt :: ",Cnt)
            
    else :
        print("Finish")
        MotorCopy.setReceivedFanSpeed(0)
        Modelupdate.ModelUpdate(filename)
        break
print("Main Process Finish")

import pandas as pd
import numpy as np
import DHT22_Confirm
import time
import api
import os

def is_non_zero_file(fpath) :
    return os.path.getsize(fpath) > 0

def WriteforAndroid():
    
    firstValue, thirdValue = DHT22_Confirm.DHTvalues()
    secondValue = 4.5
    fourthValue = 60
    # secondValue, fourthValue = api.API_measurement()  
    
    f = open("/home/pi/AI/TempCSV/outValue.txt", 'w')
    
    fiVa = str(firstValue)
    seVa = str(secondValue)
    thVa = str(thirdValue)
    foVa = str(fourthValue)
    
    # 보내줘야 하는 값
    # 1. API 두개, 2. 온습도 온도 두개.
    # OutTemp, InTemp, OutHumi, InHumi
    print(seVa + ","+ fiVa + "," + foVa + "," + thVa + ",")
    f.write(seVa + "C,"+ fiVa + "C," + foVa + "%," + thVa + "%,")
    
    f.close()
    
def WriteforAndroid_auto(pressValue):
    
    firstValue, thirdValue = DHT22_Confirm.DHTvalues()
    secondValue = 4.5
    fourthValue = 60
    # secondValue, fourthValue = api.API_measurement()  
    
    f = open("/home/pi/AI/TempCSV/outValue.txt", 'w')
    
    fiVa = str(firstValue)
    seVa = str(secondValue)
    thVa = str(thirdValue)
    foVa = str(fourthValue)
    prVa = str(pressValue)
    
    # 보내줘야 하는 값
    # 1. API 두개, 2. 온습도 온도 두개.
    # OutTemp, InTemp, OutHumi, InHumi, pressValue
    print(seVa + ","+ fiVa + "," + foVa + "," + thVa + "," + prVa + ",")
    f.write(seVa + "C,"+ fiVa + "C," + foVa + "%," + thVa + "%," + prVa + ",")
    
    f.close()

def ReadforOS():
    file_link = ('/home/pi/AI/TempCSV/inValue.txt')
    f = open(file_link, 'r')
    trashValue = 1
    
    if (os.stat(file_link) == 0) == True :
        print("None file!")
        f.close()
        return 0, 0, 0, 0, 0
    
    else :
        print("Exist file!")
        time.sleep(1)
        
    lines = f.readlines()
    for line in lines:
        powerCheck = line[:8]
        print("powerCheck ::",powerCheck)
        # 오토일 경우
        # 처음 사용하는 사용자 일 경우,
        # 전원, 자동모드, 처음인지 아닌지, 더위 타는 정도, 파일 명
        #
        # 처음 사용자가 아닌 경우
        # 전원, 자동모드, 처음인지 아닌지, 파일 명
        #
        # 수동일 경우
        # 전원, 수동모드, 풍속레벨, 파일명

        # 전원이 켜져있다면,
        if powerCheck == "powerOon" :
            print("is it work?")
            powerCheck = 1
            modeCheck = line[9:16]

            # 오토 모드 라면,
            if modeCheck == "autoOon" :
                modeCheck = 1
                experienceCheck = line[17:18]
                
                # 처음 이라면,
                if experienceCheck == "1" :
                    heatFeelLevel = line[19:20]
                    filename = line[21:1000]
                    print("powerCheck ::", powerCheck)
                    f.close()
                    return powerCheck, modeCheck, experienceCheck, heatFeelLevel, filename        
                # 처음이 아니라면,
                else :
                    filename = line[19:1000]
                    print("powerCheck ::", powerCheck)
                    f.close()
                    return powerCheck, modeCheck, experienceCheck, filename, trashValue
                    
            # 수동 모드 라면,
            else :
                modeCheck = 0
                testPower = line[17:18]
                if testPower == "0" :
                    powerLevel = line[18:19]
                else :
                    powerLevel = line[17:19]
                filename = line[20:1000]
                print("powerCheck ::", powerCheck)
                
                f.close()
                return powerCheck, modeCheck, powerLevel, filename, trashValue
                    
        # 전원이 꺼져있다면,
        else :
            powerCheck = 0
            f.close()
            return powerCheck, trashValue, trashValue, trashValue, trashValue
            
    '''
    # 자동모드  autoOon, autoOff
    # 전원      powerOon, powerOff  
    print("HFL " + powerCheck + "\n")
    print("FT " + modeCheck + "\n")
    print("FN " + experienceCheck + "\n")
    print("FN " + heatFeelLevel + "\n")
    print("FN " + filename + "\n")
    '''

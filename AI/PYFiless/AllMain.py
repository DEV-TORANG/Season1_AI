import multiprocessing as mp
import tensorflow as tf
import pandas as pd
import numpy as np
import math
import os
import time

'''
import FirstTimeAI
import AfterTimeAI
import CSVupdate
import api
import MainAI
'''

def ProcessPlus():
    time.sleep(1)
    print("a + b = ?")

def ProcessMinus():
    time.sleep(1)
    print("a - b = ?")

if __name__ == "__main__":

    th1 = mp.Process(target = ProcessPlus())
    th2 = mp.Process(target = ProcessMinus())
    
    th1.start()
    th2.start()
    
    th1.join()
    th2.join()

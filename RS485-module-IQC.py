__VERSION__ = '1.0.0'

import pelco_d 
from driver import *
import logging
from datetime import datetime
import math
import os
import sys

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logStreamFormatter = logging.Formatter(
    fmt=f"%(levelname)-8s %(asctime)s \t %(message)s", 
    datefmt="%H:%M:%S"
)
consoleHandler = logging.StreamHandler(stream=sys.stdout)
consoleHandler.setFormatter(logStreamFormatter)
consoleHandler.setLevel(level=logging.DEBUG)
logFileFormatter = logging.Formatter(
    fmt=f"%(levelname)s %(asctime)s (%(relativeCreated)d) \t %(pathname)s F%(funcName)s L%(lineno)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
fileHandler = logging.FileHandler(filename='./RS485_iqc.info')
fileHandler.setFormatter(logFileFormatter)
fileHandler.setLevel(level=logging.DEBUG)
logger.addHandler(fileHandler)
logger.addHandler(consoleHandler)


class RS485_IQC():
    def __init__(self):
        self.error_times = 0
        self.start_time = datetime.now()
        self.testtimes = 10000
        logger.info("RS485 IQC test start at : " + self.start_time.strftime("%Y-%m-%d %H:%M:%S"))

    def iqc_finish(self):
        finish_time = datetime.now()
        logger.info("RS485 IQC test end at : " + finish_time.strftime("%Y-%m-%d %H:%M:%S") + " usage time : " + str(round((finish_time - self.start_time).total_seconds()/60,2)) + " min")


    def iqc_test(self,times):
        if(times%2!=0):
            times +=1
            if(times%2!=0):
                times = 100000
        for i in  range(0,times):
            print(i)
            if(i<=times/2):
                try:
                    RS485.get_pan_position()
                    if(i>=100 and self.error_times>0):
                        break
                except Exception as e:
                    self.error_times += 1
                    msg = f"Error occurs, e:{e}"
                    print(msg)
                    logger.error(msg)
                
            else:
                try:
                    RS485.get_tilt_position()
                    if(i>=(times/2+100) and self.error_times>0):
                        break
                except Exception as e:
                    self.error_times += 1
                    msg = f"Error occurs, e:{e}"
                    print(msg)
                    logger.error("at "+ i + "times")
                    logger.error(msg)


 
    def iqc(self):
        self.iqc_test(10000)
        self.iqc_finish()
        if(self.error_times==0):
            logger.info("OK")
        else:
            logger.info("NG")
        
if __name__ == '__main__':
    #RS485
    RS485 = PTZ()
    IQC = RS485_IQC().iqc()




    
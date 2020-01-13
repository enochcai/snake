# -*- coding:utf-8 -*-
import random
import datetime
import os

#将经过的时间转为时分秒
def GetCostTimeTuple(iSecond):
    iSecond=int(iSecond)
    iHour=iSecond/3600
    iMin=iSecond%3600/60
    iSec=iSecond%60
    return iHour,iMin,iSec

#随机数,0-(iEnd-1)
def Random(iEnd):
    return random.randint(0,iEnd-1)

#创建文件夹
def CreateMyFolder(sPath):
    oFolder=os.path.exists(sPath)
    if oFolder:
        return
    os.makedirs(sPath)

#记录log,只支持二级
def log_file(sFileName,sLog):
    sTitlePath="E:/logfile/"
    if "/" in sFileName:
        lstFile=sFileName.split("/")
        if len(lstFile)>2:
            print "only 2level file is support"
            return
        sFolderPath=sTitlePath+lstFile[0]
        CreateMyFolder(sFolderPath)
    sPath="%s%s.txt"%(sTitlePath,sFileName)
    aFile=open(sPath,"a+")
    sTime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    sAllLog="[%s]%s\n"%(sTime,sLog)
    aFile.write(sAllLog)
    aFile.close()




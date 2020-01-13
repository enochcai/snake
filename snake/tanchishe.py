# -*- coding:utf-8 -*-

from tools import *
from Tkconstants import LEFT

import Tkinter
import random
import tkMessageBox
from Tkinter import StringVar

#每个点的类型
POINT_TYPE_NONE=1#空
POINT_TYPE_WALL=2#墙
POINT_TYPE_FOOD=3#食物
POINT_TYPE_SNAKE=4#蛇

POINT_WIDTH=10

SHE_DEFAULT_LEN=3#贪吃蛇初始长度

DIRECT_UP="Up"
DIRECT_DOWN="Down"
DIRECT_LEFT="Left"
DIRECT_RIGHT="Right"

DIRECT_REVERSE={
    DIRECT_UP:DIRECT_DOWN,
    DIRECT_DOWN:DIRECT_UP,
    DIRECT_LEFT:DIRECT_RIGHT,
    DIRECT_RIGHT:DIRECT_LEFT,
    }

KEYCODE_DIRECT={
    37:DIRECT_LEFT,
    38:DIRECT_UP,
    39:DIRECT_RIGHT,
    40:DIRECT_DOWN,
    }

COLOR_DEL="white"

STATE_NONE=0
STATE_START=1
STATE_OVER=2
STATE_END=3

def GetPointColor(iType):
    if iType==POINT_TYPE_NONE:
        sColor="white"
    elif iType==POINT_TYPE_WALL:
        sColor="red"
    elif iType==POINT_TYPE_FOOD:
        sColor="green"
    elif iType==POINT_TYPE_SNAKE:
        sColor="blue"
    else:
        sColor="white"
    return sColor
        
class CGame(object):
    def __init__(self,iPointWidth=10,iXPointsNum=50,iYPointsNum=50):
        self.m_Root=None
        self.m_Canvas=None
        self.m_Snake=None
        self.m_PointWidth=iPointWidth
        self.m_XPointsNum=iXPointsNum
        self.m_YPointsNum=iYPointsNum
        self.m_PointMap={}#(x,y):type
        self.m_PointObj={}#(x,y):obj
        self.m_Speed=200
        self.m_Score=0
        self.m_GameState=STATE_NONE
        self.m_RefreshFood=0
        
    def Init(self):
        self.m_Root=Tkinter.Tk()
        self.m_Root.title("贪吃蛇")
        iXLen=self.m_PointWidth*(10+self.m_XPointsNum)
        iCanvasXLen=self.m_PointWidth*self.m_XPointsNum
        iYLen=self.m_PointWidth*self.m_YPointsNum
        sGeometry="%sx%s"%(iXLen,iYLen)
        self.m_Root.geometry(sGeometry)
        self.m_Canvas=Tkinter.Canvas(self.m_Root,bg='white',width=iCanvasXLen,height=iYLen)
        self.m_Canvas.bind("<KeyRelease>",self.TrySetSnakeDirect)
        self.m_Canvas.pack(side=LEFT)
        self.m_Var=StringVar()
        self.m_ScoreMsg=Tkinter.Message(self.m_Root,textvariable=self.m_Var, aspect=5000,font=('Fixdsys', 10, "bold"), bg="#696969")
        self.m_ScoreMsg.pack()
        self.m_Var.set("分数：%s"%(self.m_Score))
        self.m_StartBtn=Tkinter.Button(self.m_Root,text="开始",command=self.GameStart,bg='red',fg='white')
        self.m_StartBtn.pack()
        self.m_Root.mainloop()
        
        
    def GameStart(self):
        self.m_GameState=STATE_START
        self.m_Score=0
        self.m_RefreshFood=0
        self.InitMap()
        self.InitSnake()
        self.RefreshFood()
        self.m_Canvas.focus_set()
        self.m_Root.after(self.m_Speed,self.Next)
        
    def InitMap(self):
        for i in xrange(self.m_YPointsNum):
            for j in xrange(self.m_XPointsNum):
                if i==0 or i==self.m_YPointsNum-1 or j==0 or j==self.m_XPointsNum-1:
                    iType=POINT_TYPE_WALL
                else:
                    iType=POINT_TYPE_NONE
                self.m_PointMap[(i,j)]=iType
                sColor=GetPointColor(iType)
                self.DrawPoint(i,j,sColor)
            
    def DrawPoint(self,x,y,sColor):#(0,0)左上角
        iLeftTopX=x*self.m_PointWidth
        iLeftTopY=y*self.m_PointWidth
        iRightBottomX=(x+1)*self.m_PointWidth
        iRightBottomY=(y+1)*self.m_PointWidth
        oPoint=self.m_Canvas.create_rectangle(iLeftTopX,iLeftTopY,iRightBottomX,iRightBottomY,outline=sColor,fill=sColor)
        self.m_PointObj[(x,y)]=oPoint
        
    def SetPointType(self,x,y,iType):
        self.m_PointMap[(x,y)]=iType
        
        
    def RefreshFood(self):
        for _ in xrange(10):
            x=Random(self.m_XPointsNum-2)+1
            y=Random(self.m_YPointsNum-2)+1
            tPos=(x,y)
            if tPos in self.m_Snake.m_Body:
                print "inbody",x,y
                continue            self.SetPointType(x,y,POINT_TYPE_FOOD)
            self.DrawPoint(x,y,"blue")
            break
    
    def InitSnake(self):
        self.m_Snake=CSnake(self)
        self.m_Snake.DrawBody()
        
    def Next(self):
        if self.m_GameState==STATE_OVER:
            message=tkMessageBox.showinfo("Game Over", "your score: %d"%self.m_Score)
            return
        if self.m_RefreshFood:
            self.RefreshFood()
            self.m_RefreshFood=0
        self.m_Root.after(self.m_Speed,self.Next)
        self.Crawl()
        
    def CalNextPoint(self,sDirect):
        if sDirect==DIRECT_UP:
            iXHead,iYHead=self.m_Snake.m_Body[0]
            iNextX=iXHead
            iNextY=iYHead-1
        elif sDirect==DIRECT_DOWN:
            iXHead,iYHead=self.m_Snake.m_Body[0]
            iNextX=iXHead
            iNextY=iYHead+1
        elif sDirect==DIRECT_LEFT:
            iXHead,iYHead=self.m_Snake.m_Body[0]
            iNextX=iXHead-1
            iNextY=iYHead
        elif sDirect==DIRECT_RIGHT:
            iXHead,iYHead=self.m_Snake.m_Body[0]
            iNextX=iXHead+1
            iNextY=iYHead
        else:
            return -1,-1
        return iNextX,iNextY
        
    def Crawl(self):
        iNextX,iNextY=self.CalNextPoint(self.m_Snake.m_Direct)
        tPoint=(iNextX,iNextY)
        iPointType=self.m_PointMap.get(tPoint)
        if iPointType==POINT_TYPE_WALL:
            self.m_GameState=STATE_OVER
        elif iPointType==POINT_TYPE_FOOD:
            self.m_Score+=1
            self.m_Var.set("分数：%s"%(self.m_Score))
            self.m_RefreshFood=1
            self.SetPointType(iNextX,iNextY,POINT_TYPE_NONE)
        elif iPointType==POINT_TYPE_SNAKE:
            self.m_GameState=STATE_OVER
        else:
            self.m_Snake.DelBodyNode()
        self.m_Snake.m_Body.insert(0,(iNextX,iNextY))
        self.m_Snake.DrawBody()
        
    def AfterCrawl(self):
        #检测是否撞墙
        iXHead,iYHead=self.m_Body[0]
        
    def TrySetSnakeDirect(self,event):
        iCode=event.keycode
        if not iCode in KEYCODE_DIRECT:
            return
        sDirect=KEYCODE_DIRECT[iCode]
        self.m_Snake.SetDirect(sDirect)
        
    
class CSnake(object):
    def __init__(self,oGame):
        self.m_Game=oGame
        self.m_Body=[(2,3),(2,2),(2,1),]#第一个为蛇头
        self.m_Color="blue"
        self.m_HeadColor="black"
        self.m_Direct=DIRECT_DOWN
        
    def DrawBody(self):
        for idx,(x,y)in enumerate(self.m_Body):
            if idx==0:
                self.m_Game.DrawPoint(x,y,self.m_HeadColor)
            else:
                self.m_Game.DrawPoint(x,y,self.m_Color)
            self.m_Game.SetPointType(x,y,POINT_TYPE_SNAKE)
                
    def DelBodyNode(self):
        tDel=self.m_Body.pop()
        self.m_Game.DrawPoint(tDel[0],tDel[1],COLOR_DEL)
        self.m_Game.SetPointType(tDel[0],tDel[1],POINT_TYPE_NONE)
        
    def DrawHeadNode(self):
        tHead=self.m_Body[0]
        self.m_Game.DrawPoint(tHead[0],tHead[1],self.m_HeadColor)
        
    def SetDirect(self,sDirect):
        sReverse=DIRECT_REVERSE[self.m_Direct]
        if sDirect==sReverse:#不能反向
            return
        iNextX,iNextY=self.m_Game.CalNextPoint(sDirect)
        if iNextX==-1 or iNextY==-1:
            return
        tPos=(iNextX,iNextY)
#         if tPos in self.m_Body:#不能咬到自己
#             return
        self.m_Direct=sDirect
    

                                                                                                                                                                                                                                                                                                                                                              

oGame=CGame()
oGame.Init()    



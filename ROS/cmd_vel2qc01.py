#!/usr/bin/env python
# -*- coding: utf-8 -*-
from websocket import create_connection
import struct
import rospy
from geometry_msgs.msg import Twist
import time

ws = create_connection("ws://192.168.1.136:54323")

STOP = 0
FW   = 1
RW   = 2
CW   = 3
CCW  = 4
RGT  = 5
LFT  = 6
BRK  = 9
OFF  = 0
ON   = 1

ULTRA_LOW  = 0
LOW        = 1
NORMAL     = 2
HIGH       = 3
ULTRA_HIGH = 4
NoSpeed    = 99

State = STOP
xSpeed = NoSpeed
ySpeed = NoSpeed
zSpeed = NoSpeed



#制御コマンド定義

command_stp      =  [0xff,0x55,0x01,0x06]
command_dwn      =  [0xff,0x55,0x04,0x01,0x07,0xc8,0x00]
command_up       =  [0xff,0x55,0x04,0x01,0x08,0xc8,0x00]

command_fw = [[]*7]*5
command_fw[ULTRA_LOW]   =  [0xff,0x55,0x04,0x01,0x01,0x0d,0x07]
command_fw[LOW]         =  [0xff,0x55,0x04,0x01,0x01,0xe8,0x03]
command_fw[NORMAL]      =  [0xff,0x55,0x04,0x01,0x01,0xf4,0x01]
command_fw[HIGH]        =  [0xff,0x55,0x04,0x01,0x01,0xc8,0x00]
command_fw[ULTRA_HIGH]  =  [0xff,0x55,0x04,0x01,0x01,0x64,0x00]

command_rw = [[]*7]*5
command_rw[ULTRA_LOW]   =  [0xff,0x55,0x04,0x01,0x04,0x0d,0x07]
command_rw[LOW]         =  [0xff,0x55,0x04,0x01,0x04,0xe8,0x03]
command_rw[NORMAL]      =  [0xff,0x55,0x04,0x01,0x04,0xf4,0x01]
command_rw[HIGH]        =  [0xff,0x55,0x04,0x01,0x04,0xc8,0x00]
command_rw[ULTRA_HIGH]  =  [0xff,0x55,0x04,0x01,0x04,0x64,0x00]

command_cw = [[]*7]*5
command_cw[ULTRA_LOW]   =  [0xff,0x55,0x04,0x01,0x02,0x0d,0x07]
command_cw[LOW]         =  [0xff,0x55,0x04,0x01,0x02,0xe8,0x03]
command_cw[NORMAL]      =  [0xff,0x55,0x04,0x01,0x02,0xf4,0x01]
command_cw[HIGH]        =  [0xff,0x55,0x04,0x01,0x02,0xc8,0x00]
command_cw[ULTRA_HIGH]  =  [0xff,0x55,0x04,0x01,0x02,0x64,0x00]

command_ccw = [[]*7]*5
command_ccw[ULTRA_LOW]  =  [0xff,0x55,0x04,0x01,0x03,0x0d,0x07]
command_ccw[LOW]        =  [0xff,0x55,0x04,0x01,0x03,0xe8,0x03]
command_ccw[NORMAL]     =  [0xff,0x55,0x04,0x01,0x03,0xf4,0x01]
command_ccw[HIGH]       =  [0xff,0x55,0x04,0x01,0x03,0xc8,0x00]
command_ccw[ULTRA_HIGH] =  [0xff,0x55,0x04,0x01,0x03,0x64,0x00]

command_rgt = [[]*7]*5
command_rgt[ULTRA_LOW]  =  [0xff,0x55,0x04,0x01,0x05,0x0d,0x07]
command_rgt[LOW]        =  [0xff,0x55,0x04,0x01,0x05,0xe8,0x03]
command_rgt[NORMAL]     =  [0xff,0x55,0x04,0x01,0x05,0xf4,0x01]
command_rgt[HIGH]       =  [0xff,0x55,0x04,0x01,0x05,0xc8,0x00]
command_rgt[ULTRA_HIGH] =  [0xff,0x55,0x04,0x01,0x05,0x64,0x00]

command_lft = [[]*7]*5
command_lft[ULTRA_LOW]  =  [0xff,0x55,0x04,0x01,0x06,0x0d,0x07]
command_lft[LOW]        =  [0xff,0x55,0x04,0x01,0x06,0xe8,0x03]
command_lft[NORMAL]     =  [0xff,0x55,0x04,0x01,0x06,0xf4,0x01]
command_lft[HIGH]       =  [0xff,0x55,0x04,0x01,0x06,0xc8,0x00]
command_lft[ULTRA_HIGH] =  [0xff,0x55,0x04,0x01,0x06,0x64,0x00]


command_rbw      =  [0xff,0x55,0x02,0x0a,0x03]
command_red      =  [0xff,0x55,0x02,0x09,0x01]
command_gln      =  [0xff,0x55,0x02,0x09,0x02]
command_ble      =  [0xff,0x55,0x02,0x09,0x03]
command_yel      =  [0xff,0x55,0x02,0x09,0x04]
command_vio      =  [0xff,0x55,0x02,0x09,0x05]
command_aqu      =  [0xff,0x55,0x02,0x09,0x06]
command_ledoff   =  [0xff,0x55,0x02,0x09,0x00]

command_spDo     =  [0xff,0x55,0x05,0x0b,0x06,0x01,0x7d,0x00]
command_spLe     =  [0xff,0x55,0x05,0x0b,0x26,0x01,0x7d,0x00]




def Move_Cntrl(com,spd):

    if com == FW:
        ws.send(command_spDo)
        ws.send(command_ble)
        ws.send(command_fw[spd])
    elif com == RW:
        ws.send(command_spDo)
        ws.send(command_red)
        ws.send(command_rw[spd])
    elif com == CW:
        ws.send(command_spDo)
        ws.send(command_gln)
        ws.send(command_cw[spd])
    elif com == CCW:
        ws.send(command_spDo)
        ws.send(command_yel)
        ws.send(command_ccw[spd])
    elif com == BRK:
        ws.send(command_spDo)
        ws.send(command_ledoff)
        ws.send(command_stp)
    elif com == RGT:
        ws.send(command_spDo)
        ws.send(command_aqu)
        ws.send(command_rgt[spd])
    elif com == LFT:
        ws.send(command_spDo)
        ws.send(command_aqu)
        ws.send(command_lft[spd])
    else:
        ws.send(command_spDo)
        ws.send(command_vio)
        ws.send(command_stp)


def spcom(spd):

    if (spd < 20):
       Speed = ULTRA_LOW
    elif (spd < 40):
       Speed = LOW
    elif (spd < 60):
       Speed = NORMAL
    elif (spd < 90):
       Speed = HIGH
    else :
       Speed = ULTRA_HIGH
    return Speed


def qc_contrl(msg):
    global State
    global xSpeed
    global ySpeed
    global zSpeed


    print("Get Twist data")
    lx = msg.linear.x
    ly = msg.linear.y
    lz = msg.linear.z
    ax = msg.angular.x
    ay = msg.angular.y
    az = msg.angular.z

    xspd = int(100 * abs(lx))
    yspd = int(100 * abs(ly))
    zspd = int(100 * abs(az))

    if xspd > 100 :
       xspd = 100
    elif xspd < 0:
       xspd = 0
    if yspd > 100 :
       yspd = 100
    elif yspd < 0:
       yspd = 0
    if zspd > 100 :
       zspd = 100
    elif zspd < 0:
       zspd = 0


    if (lx == 0) and (ly == 0) and (az == 0 ):
       print("STOP")
       if (State != STOP):
           Move_Cntrl(STOP,0)
           State = STOP
           xSpeed = NoSpeed
           ySpeed = NoSpeed
           zSpeed = NoSpeed
    elif (lx == 0) and (ly == 0):
       if az < 0:
           print ("CW")
           if (zSpeed != spcom(zspd)):
               zSpeed = spcom(zspd)
               Move_Cntrl(CW,spcom(zspd))
               State = CW
       else:
           print ("CCW")
           if (zSpeed != spcom(zspd)):
               zSpeed = spcom(zspd)
               Move_Cntrl(CCW,spcom(zspd))
               State = CCW
    elif (ly == 0) and (az == 0):
       if lx > 0:
           print("FW")
           if (xSpeed != spcom(xspd)):
               xSpeed = spcom(xspd)
               Move_Cntrl(FW,xSpeed)
               State = FW
       else:
           print("RW")
           if (xSpeed != spcom(xspd)):
               xSpeed = spcom(xspd)
               Move_Cntrl(RW,spcom(xspd))
               State = RW
    elif (lx == 0) and (az == 0):
       if ly < 0:
           print("RGT")
           if (ySpeed != spcom(yspd)):
               ySpeed = spcom(yspd)
               Move_Cntrl(RGT,ySpeed)
               State = RGT
       else:
           print("LFT")
           if (ySpeed != spcom(yspd)):
               ySpeed = spcom(yspd)
               Move_Cntrl(LFT,spcom(yspd))
               State = LFT
    else:
       pass


rospy.init_node('cmd_vel2qc')
rospy.Subscriber('cmd_vel',Twist,qc_contrl)
rospy.spin()



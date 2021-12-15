from websocket import create_connection
import time
import struct


def ws_recv():
    data = ws.recv()
    recv1 = list(struct.unpack_from("B",data[0],0))
    recv2 = list(struct.unpack_from("B",data[1],0))
    recv = recv1 + recv2
    return recv

ws = create_connection("ws://192.168.1.136:54323")
print "Open"
print "Sending command"

command_stp      =  [0xff,0x55,0x01,0x06]
command_dwn      =  [0xff,0x55,0x04,0x01,0x07,0xc8,0x00]
command_up       =  [0xff,0x55,0x04,0x01,0x08,0xc8,0x00]

command_fw       =  [0xff,0x55,0x04,0x01,0x01,0xc8,0x00]
command_fwUH     =  [0xff,0x55,0x04,0x01,0x01,0x64,0x00]

command_rw       =  [0xff,0x55,0x04,0x01,0x04,0xc8,0x00]
command_cw       =  [0xff,0x55,0x04,0x01,0x02,0xc8,0x00]
command_ccw      =  [0xff,0x55,0x04,0x01,0x03,0xc8,0x00]
command_rgt      =  [0xff,0x55,0x04,0x01,0x05,0xc8,0x00]
command_lft      =  [0xff,0x55,0x04,0x01,0x06,0xc8,0x00]


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



ws.send(command_rbw)
print "Received '{}'".format(ws_recv())
time.sleep(0.5)


ws.send(command_fw)
print "Received '{}'".format(ws_recv())
time.sleep(2)

ws.send(command_fwUH)
print "Received '{}'".format(ws_recv())
time.sleep(2)


ws.send(command_stp)
print "Received '{}'".format(ws_recv())
time.sleep(0.5)


ws.send(command_up)
print "Received '{}'".format(ws_recv())
time.sleep(0.5)


ws.send(command_spDo)
print "Received '{}'".format(ws_recv())
time.sleep(0.5)


ws.send(command_spLe)
print "Received '{}'".format(ws_recv())
time.sleep(0.5)


ws.send(command_red)
print "Received '{}'".format(ws_recv())
time.sleep(0.5)


ws.send(command_rw)
print "Received '{}'".format(ws_recv())
time.sleep(2)

ws.send(command_stp)
print "Received '{}'".format(ws_recv())
time.sleep(0.5)


ws.send(command_gln)
print "Received '{}'".format(ws_recv())
time.sleep(0.5)
ws.send(command_ble)
print "Received '{}'".format(ws_recv())
time.sleep(0.5)
ws.send(command_yel)
print "Received '{}'".format(ws_recv())
time.sleep(0.5)
ws.send(command_vio)
print "Received '{}'".format(ws_recv())
time.sleep(0.5)
ws.send(command_aqu)
print "Received '{}'".format(ws_recv())
time.sleep(0.5)
ws.send(command_ledoff)
print "Received '{}'".format(ws_recv())
time.sleep(0.5)




#ws.send(command_stp)
#print "Received '{}'".format(ws_recv())
#time.sleep(0.5)

ws.send(command_spDo)
print "Received '{}'".format(ws_recv())
time.sleep(0.5)



ws.close()

print "Close"


import socket
import time
import sys
import spidev
import math

# spi_setup
spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz = 1000000

#get_value
def readAdc(channel):
        adc = spi.xfer2([1,(8+channel)<<4,0])
        data = ((adc[1]&3) << 8) + adc[2]
        return data


# scket connect
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("", 55555))
s.listen()
soc, addr = s.accept()
print("Conneted by"+str(addr))


#reset
on_cnt0 = 0
off_cnt0 = 0
flg0 = 0
on_cnt1 = 0
off_cnt1 = 0
flg1 = 0
on_cnt2 = 0
off_cnt2 = 0
flg2 = 0


try:
    while True:
        #collect data-----------------------
        data0 = readAdc(0)
        data1 = readAdc(1)
        data2 = readAdc(2)
        print('channel0 : ',data0,'channel1 : ',data1,'channel2 : ',data2)
        
        #judge on or off--------------------
        #data0
        if data0 < 10:
            on_cnt0 = on_cnt0 + 1
            off_cnt0 = 0
        else:
            off_cnt0 = off_cnt0 + 1
            on_cnt0 = 0
        #data1
        if data1 < 10:
            on_cnt1 = on_cnt1 + 1
            off_cnt1 = 0
        else:
            off_cnt1 = off_cnt1 + 1
            on_cnt1 = 0
        #data2
        if data2 < 10:
            on_cnt2 = on_cnt2 + 1
            off_cnt2 = 0
        else:
            off_cnt2 = off_cnt2 + 1
            on_cnt2 = 0

        #send data to client-----------------
#         if on_cnt0 == 5:
#             val = '1,0,0'
#             senddata = val.encode('utf-8')
#             soc.send(senddata)
#             
#         if off_cnt0 == 5:
#             val = '0,0,0'
#             senddata = val.encode('utf-8')
#             soc.send(senddata)
        
        #change flg value----------------
        if on_cnt0 == 5:
            flg0 = 1
        if off_cnt0 == 3:
            flg0 = 0
        if on_cnt1 == 5:
            flg1 = 1
        if off_cnt1 == 3:
            flg1 = 0
        if on_cnt2 == 5:
            flg2 = 1
        if off_cnt2 == 3:
            flg2 = 0
            
        #send data to client---------------------
        sendval = str(flg0)+','+str(flg1)+','+str(flg2)
        senddata = sendval.encode('utf-8')
        soc.send(senddata)

        #print(on_cnt0,off_cnt1)
        #print('sendval => ',sendval)
        
        time.sleep(1)
        
except KeyboardInterrupt:
    data = "q"
    soc.send(data.encode('utf-8'))
    
    soc.close()
    spi.close()
    sys.exit()
    
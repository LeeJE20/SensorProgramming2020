# degital clock
import smbus2 as smbus
import time

bus = smbus.SMBus(1)
addr = 0x20
config_port = 0x06
out_port = 0x02
# 0 1 2 3 4 5 6 7 8 9
data = (0xFC,0x60,0xDA,0xF2,0x66,0xB6,0x3E,0xE0,0xFE,0xF6,0x01)
# seg1, seg2, seg3, seg4, seg5, seg6
digit = (0x7F, 0xBF, 0xDF, 0xEF, 0xF7, 0xFB)
out_disp=0

bus.write_word_data(addr, config_port, 0x0000)

# 시간, 분, 초 리턴
def whatTimeIsIt():
    tm = time.gmtime(time.time())
    tmlist = []
    tmlist.append(str(tm.tm_hour))
    tmlist.append(str(tm.tm_min))
    tmlist.append(str(tm.tm_sec))

    return tmlist

# 시간을 한 숫자씩 분해
def getClockNum(tmlist):
    numlist = []
    for i in range (0, 3):
        num = int(tmlist[i])
        if num < 10:
            numlist.append(0)
            numlist.append(num)
        else:
            numlist.append(int(num/10))
            numlist.append(num%10)
    return numlist


try:
    while True:
        tmlist = whatTimeIsIt()
        numlist = getClockNum(tmlist)
        print(numlist)
        # seg1 부터 seg6까지, 0~9까지 반복하면서 출력
        for i in range (0,6,1):
            out_disp = data[numlist[i]] << 8 | digit[i]
            bus.write_word_data(addr, out_port, out_disp)
            time.sleep(0.001) #0.1초 주면 흘러가는 걸로 보인다.  
            if (i==1 or i==3) :
                # 시간 사이에 도트 표시
                out_disp = data[10] << 8 | digit[i]
                bus.write_word_data(addr, out_port, out_disp)
                time.sleep(0.001)

                
              
except KeyboardInterrupt:
    pass
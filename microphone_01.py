import spidev # SPI 통신을 위해 모듈 가져오기
import time
sound = spidev.SpiDev() # 객체 생성
sound.open(0, 1) # 0번 채널의 SPI 버스 1번 채널
sound.max_speed_hz = 1000000 # 최대 주파수 설정


for _ in range(100):
    data = sound.xfer2([0x06, 0x80, 0x00])
    ret = ((data[1] & 0x0F) << 8) | data[2]
    print("sound = %d"%ret)
    time.sleep(0.05)


sound.close()

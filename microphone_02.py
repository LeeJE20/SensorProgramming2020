import spidev # SPI 통신을 위해 모듈 가져오기
import time

def sound_init():
    sound = spidev.SpiDev()
    sound.open(0, 1)
    sound.max_speed_hz = 1000000
    return sound

def sound_measure(sound, cal, base = 2047):
    data = sound.xfer2([0x06, 0x80, 0x00])
    ret = ((data[1] & 0x0F) << 8) | data[2]
    return abs(base - (ret - cal))

def sound_destroy(sound):
    sound.close()


# if __name__ == "__main__":
#     sound = sound_init()
#     for _ in range(100):
#         print("sound = %d"%sound_measure(sound, 30))
#         time.sleep(0.05)
#     sound_destroy(sound)


try:
    sound = sound_init()
    while True:
        print("sound = %d"%sound_measure(sound, 30))
        time.sleep(0.05)
        if sound_measure(sound, 30)>60:
            GPIO.output(led_pins[0], True)
            time.sleep(3)
        else:
            GPIO.output(led_pins[0], False)
except KeyboardInterrupt:
    pass
    GPIO.cleanup()
    sound_destroy(sound)
    print("Program is terminated..!!!")
# 정은: 쓰레드 종료 동작 잘 되도록 수정
# 피에조부저 작동 잘 되게 해야함.


import RPi.GPIO as GPIO
import time
import threading

GPIO.setmode(GPIO.BCM)

# led setting
led_pin1 = 14
led_pin2 = 15
GPIO.setup(led_pin1, GPIO.OUT)
GPIO.setup(led_pin2, GPIO.OUT)

# piezo setting
gpio_pin = 13
scale = [523, 493]
GPIO.setup(gpio_pin, GPIO.OUT)

# jogswitch setting
gpio = [5, 6, 16, 20, 21]
stat = [0, 0, 0, 0, 0]
for i in range(5):
    GPIO.setup(gpio[i], GPIO.IN)

# Lcd setting
# (1) Define GPIO to LCD mapping
LCD_RS = 23
LCD_RW = 24
LCD_E = 26
LCD_D4 = 17
LCD_D5 = 18
LCD_D6 = 27
LCD_D7 = 22
# (2) Define some device constants
LCD_WIDTH = 16  # Maximum characters per line
LCD_CHR = True
LCD_CMD = False
LCD_LINE_1 = 0x80  # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0  # LCD RAM address for the 2nd line
# (3) Timing constants
E_PULSE = 0.0005
E_DELAY = 0.0005


# 쓰레드 조절
killThread = False


# (4)
def lcd_init():
    # Initialise display
    lcd_byte(0x33, LCD_CMD)  # 00110011 Initialise
    lcd_byte(0x32, LCD_CMD)  # 00110010 Initialise
    lcd_byte(0x06, LCD_CMD)  # 00000110 Cursor move direction
    lcd_byte(0x0C, LCD_CMD)  # 00001100 Display On,Cursor Off, Blink Off
    lcd_byte(0x28, LCD_CMD)  # 00101000 Data length, number of lines, font size
    lcd_byte(0x01, LCD_CMD)  # 00000001 Clear display
    time.sleep(E_DELAY)


def lcd_toggle_enable():
    time.sleep(E_DELAY)
    GPIO.output(LCD_E, True)
    time.sleep(E_PULSE)
    GPIO.output(LCD_E, False)
    time.sleep(E_DELAY)


def lcd_byte(bits, mode):
    # Send byte to data pins
    # bits = data
    # mode = True for character
    # False for command
    GPIO.output(LCD_RS, mode)  # RS

    # High bits
    GPIO.output(LCD_D4, False)
    GPIO.output(LCD_D5, False)
    GPIO.output(LCD_D6, False)
    GPIO.output(LCD_D7, False)
    if bits & 0x10 == 0x10:
        GPIO.output(LCD_D4, True)
    if bits & 0x20 == 0x20:
        GPIO.output(LCD_D5, True)
    if bits & 0x40 == 0x40:
        GPIO.output(LCD_D6, True)
    if bits & 0x80 == 0x80:
        GPIO.output(LCD_D7, True)
    # Toggle 'Enable' pin
    lcd_toggle_enable()

    # Low bits
    GPIO.output(LCD_D4, False)
    GPIO.output(LCD_D5, False)
    GPIO.output(LCD_D6, False)
    GPIO.output(LCD_D7, False)
    if bits & 0x01 == 0x01:
        GPIO.output(LCD_D4, True)
    if bits & 0x02 == 0x02:
        GPIO.output(LCD_D5, True)
    if bits & 0x04 == 0x04:
        GPIO.output(LCD_D6, True)
    if bits & 0x08 == 0x08:
        GPIO.output(LCD_D7, True)
    # Toggle 'Enable' pin
    lcd_toggle_enable()


def lcd_string(message, line):
    # Send string to display
    message = message.ljust(LCD_WIDTH, " ")  # left-align
    lcd_byte(line, LCD_CMD)
    for i in range(LCD_WIDTH):
        lcd_byte(ord(message[i]), LCD_CHR)


# led function
def blink(run_event):
    while run_event.is_set():
        GPIO.output(led_pin1, True)
        GPIO.output(led_pin2, False)  # Off 27
        time.sleep(1)  # Wait one second
        GPIO.output(led_pin1, False)  # Off 17
        GPIO.output(led_pin2, True)  # On 27
        time.sleep(1)  # Wait one second



# piezo function
def alert(run_event):
    p = GPIO.PWM(gpio_pin, 100)
    GPIO.output(gpio_pin, True)
    p.start(100)

    while run_event.is_set():
        p.ChangeFrequency(scale[0])
        time.sleep(0.5)
        p.ChangeFrequency(scale[1])
        time.sleep(0.5)




# Lcd function
def alertLcd(run_event):
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)  # Use BCM GPIO numbers
    GPIO.setup(LCD_E, GPIO.OUT)  # E
    GPIO.setup(LCD_RS, GPIO.OUT)  # RS
    GPIO.setup(LCD_D4, GPIO.OUT)  # DB4
    GPIO.setup(LCD_D5, GPIO.OUT)  # DB5
    GPIO.setup(LCD_D6, GPIO.OUT)  # DB6
    GPIO.setup(LCD_D7, GPIO.OUT)  # DB7
    lcd_init()

    while run_event.is_set():
        lcd_string("Emergency!!", LCD_LINE_1)
        lcd_string("Please call 119!", LCD_LINE_2)
        # time.sleep(3)  # 3 second delay
        time.sleep(1.5)
        lcd_string("After call 119,", LCD_LINE_1)
        lcd_string("Press red switch", LCD_LINE_2)
        time.sleep(1.5)
        # time.sleep(3)

    lcd_string("hello", LCD_LINE_1)
    lcd_string("world", LCD_LINE_2)
    time.sleep(1)


# main function
def emergency():
    # 쓰레드 제어를 위한 객체
    run_event = threading.Event()
    run_event.set()
    # work(run_event)

    # 쓰레드 생성
    t1 = threading.Thread(target=blink, args = [run_event])
    t2 = threading.Thread(target=alert, args = [run_event])
    t3 = threading.Thread(target=alertLcd, args = [run_event])

    # 쓰레드 실행
    t1.start()
    t2.start()
    t3.start()

    while True:
        for i in range(5):
            state = GPIO.input(gpio[i])
            if state != stat[i]:
                stat[i] = state
        if (stat[4] == 1):
            # 쓰레드한테 종료 신호 보냄
            run_event.clear()

            # 모든 쓰레드가 종료되길 기다림
            t1.join()
            t2.join()
            t3.join()

            
            # 현재 쓰레드 종료
            break

            



try:
    emergency()
finally:
    print("Quit")
    GPIO.cleanup()
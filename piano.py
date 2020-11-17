import pygame # pygame 모듈의 임포트
import sys # 외장 모듈
from pygame.locals import * # QUIT 등의 pygame 상수들을 로드한다.
import RPi.GPIO as GPIO
#import time



GPIO.setmode(GPIO.BCM)

#LED 설정
led_pin1 = 14
led_pin2 = 15
GPIO.setup(led_pin1, GPIO.OUT)
GPIO.setup(led_pin2, GPIO.OUT)





#음계
scale = [32.7032, 34.6478, 36.7081, 38.8909, 41.2034, 43.6535, 46.2493, 48.9994, 51.9130, 55.0000, 58.2705, 61.7354]
name = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
note = dict(zip(name, scale))

#옥타브
octav = 4

# 피에조 설정
gpio_pin = 13 # 피에조
GPIO.setup(gpio_pin, GPIO.OUT)
p = GPIO.PWM(gpio_pin, 100)
p.start(100) # start the PWM on 100% duty cycle

# 화면 크기
width = 900
height = 600

# 색깔
white = (255, 255, 255)
black = (  0,   0,   0)
blue = (  18,   102,   255)
green = (71, 200, 62)
# fps = 30


pygame.init() # 초기화


pygame.display.set_caption('Hello, Piano!') # 창 제목 설정
displaysurf = pygame.display.set_mode((width, height), 0, 32) # 메인 디스플레이를 설정한다
#clock = pygame.time.Clock() # 시간 설정

defaultFont = pygame.font.SysFont('Consolas', 40) # 서체 설정
helloPiano = defaultFont.render('Hello, Piano!', True, blue) # .render() 함수에 내용과 안티앨리어싱, 색을 전달하여 글자 이미지 생성
hellorect = helloPiano.get_rect() # 생성한 이미지의 rect 객체를 가져온다
hellorect.center = (width / 2, 30) # 해당 rect의 중앙을 화면 중앙에 맞춘다


# 프로그램 키 설명 관련
infoFont = pygame.font.SysFont('Consolas', 30) # 설명 폰트

# 설명 글
octavInfo=["a: one octav down", "s: one octav up", " ",
    "z: change octav to 1", "x: change octav to 2", "c: change octav to 3",
    "v: change octav to 4", "b: change octav to 5", "n: change octav to 6",
    "m: change octav to 7", ",: change octav to 8"]

noteInfo=["q: low A", "w: low B",
          "e: C", "r: D", "t: E", "y: F", "u: G", "i: A", "o: B",
          "p: high C", "[: high D", "]: high E"]

semiNoteInfo=["2: low A#", " ",
          "4: C#", "5: D#", " ", "7: F#", "8: G#", "9: A#", " ",
          "-: high C#", "=: high D#"]

# 원하는 위치에 글씨 쓰는 함수
def printText(msg, color=green, pos=(50,65), font = defaultFont):
    textSurface     = font.render(msg, True, color)
    textRect        = textSurface.get_rect()
    textRect.topleft= pos
    displaysurf.blit(textSurface, textRect)

# 소리 내기 함수
# string 음이름 (C, C# 등), int 소리 낼 음의 옥타브
def sound(noteName, localOctav):
    printText("note: "+str(noteName))
    printText("octav: "+str(localOctav), pos = (300, 65))
    GPIO.output(led_pin1, True)
    # 한 옥타브가 올라가면 주파수는 2배가 된다.
    countedOctav = 2**(localOctav-1)
    p.ChangeDutyCycle(50)
    p.ChangeFrequency(note[noteName] * countedOctav)

# 배경 흰색으로
displaysurf.fill(white)

while True: # 아래의 코드를 무한 반복한다.

    for event in pygame.event.get(): # 발생한 입력 event 목록의 event마다 검사

        if event.type == QUIT: # event의 type이 QUIT에 해당할 경우 (x 클릭)
            GPIO.cleanup()
            pygame.quit() # pygame을 종료한다
            sys.exit() # 창을 닫는다

        if event.type == pygame.KEYDOWN:# 키가 눌리면
            displaysurf.fill(white) # 이전 화면 지우기
            GPIO.output(led_pin1, True) # 키 입력 받으면 LED 켜짐

            # 종료
            if event.key == pygame.K_ESCAPE: # esc 키
                GPIO.cleanup()
                pygame.quit() # pygame을 종료한다
                sys.exit() # 창을 닫는다

            # 옥타브 절대 변경
            if event.key == pygame.K_z:
                printText("changed octav")
                octav = 1
            elif event.key == pygame.K_x:
                printText("changed octav")
                octav = 2
            elif event.key == pygame.K_c:
                printText("changed octav")
                octav = 3
            elif event.key == pygame.K_v:
                printText("changed octav")
                octav = 4
            elif event.key == pygame.K_b:
                printText("changed octav")
                octav = 5
            elif event.key == pygame.K_n:
                printText("changed octav")
                octav = 6
            elif event.key == pygame.K_m:
                printText("changed octav")
                octav = 7
            elif event.key == pygame.K_COMMA: # , 입력
                printText("changed octav")
                octav = 8

            # 옥타브 상대 변경
            elif event.key == pygame.K_a:
                if octav > 1:
                    printText("changed octav")
                    octav -= 1
                else:
                    printText("cannot change octav: too low")
            elif event.key == pygame.K_s:
                if octav < 8:
                    printText("changed octav")
                    octav += 1
                else:
                    printText("cannot change octav: too high")


            # 낮은 음계 입력
            elif event.key == pygame.K_q:
                if octav > 1:
                    sound("A", octav - 1)
                else:
                    printText('cannot play A: too low')
            elif event.key == pygame.K_2:
                if octav > 1:
                    sound("A#", octav - 1)
                else:
                    printText('cannot play A#: too low')
            elif event.key == pygame.K_w:
                if octav > 1:
                    sound("B", octav - 1)
                else:
                    printText('cannot play B: too low')

            # 높은 음계 입력
            elif event.key == pygame.K_p:
                if octav < 8:
                    sound("C", octav + 1)
                else:
                    printText('cannot play C: too high')
            elif event.key == pygame.K_MINUS: # - 입력
                if octav < 8:
                    sound("C#", octav + 1)
                else:
                    printText('cannot play C#: too high')
            elif event.key == pygame.K_LEFTBRACKET: # [ 입력
                if octav < 8:
                    sound("D", octav + 1)
                else:
                    printText('cannot play D: too high')
            elif event.key == pygame.K_EQUALS: # = 입력
                if octav < 8:
                    sound("D#", octav + 1)
                else:
                    printText('cannot play D#: too high')
            elif event.key == pygame.K_RIGHTBRACKET: # ] 입력
                if octav < 8:
                    sound("E", octav + 1)
                else:
                    printText('cannot play E: too high')

            # 일반 음계 입력 (현재 옥타브 음계)
            elif event.key == pygame.K_e:
                sound("C", octav)
            elif event.key == pygame.K_4:
                sound("C#", octav)
            elif event.key == pygame.K_r:
                sound("D", octav)
            elif event.key == pygame.K_5:
                sound("D#", octav)
            elif event.key == pygame.K_t:
                sound("E", octav)
            elif event.key == pygame.K_y:
                sound("F", octav)
            elif event.key == pygame.K_7:
                sound("F#", octav)
            elif event.key == pygame.K_u:
                sound("G", octav)
            elif event.key == pygame.K_8:
                sound("G#", octav)
            elif event.key == pygame.K_i:
                sound("A", octav)
            elif event.key == pygame.K_9:
                sound("A#", octav)
            elif event.key == pygame.K_o:
                sound("B", octav)

            # 그 외의 키보드 (잘못 입력)
            else:
                GPIO.output(led_pin2, True) # 키 입력 받으면 켜짐
                p.ChangeDutyCycle(0)
                printText('wrong key')

        # 키보드 뗄 떼
        if event.type == pygame.KEYUP:
            # LED 끄기
            GPIO.output(led_pin1, False)
            GPIO.output(led_pin2, False)
            # 소리 끄기
            p.ChangeDutyCycle(0)
            # 화면 지우기
            displaysurf.fill(white)


    displaysurf.blit(helloPiano, hellorect) # displaysurf의 hellorect의 위치에 helloPiano를 뿌린다

    printText("Current Octav: "+str(octav), pos=(50,120)) # 현재 옥타브값 표시

    # 설명서
    startPos = 180
    for text in octavInfo:
        printText(text, pos=(40,startPos), font = infoFont, color = black)
        startPos+=34

    startPos = 180
    for text in noteInfo:
        printText(text, pos=(300,startPos), font = infoFont, color = black)
        startPos+=34

    startPos = 197
    for text in semiNoteInfo:
        printText(text, pos=(420,startPos), font = infoFont, color = black)
        startPos+=34


    xPos = 570
    printText("esc: quit program", pos=(xPos,180), font = infoFont, color = black)


    # 제작자
    startPos = 300
    printText("2020. 10. 12", pos=(xPos, startPos), color = blue)
    printText("Sensor Programming", pos=(xPos, startPos + 50), color = blue)
    printText("1811512", pos=(xPos, startPos + 150), color = blue)
    printText("Lee JungEun", pos=(xPos, startPos + 200), color = blue)

    pygame.display.flip() # 화면을 업데이트한다
    # clock.tick(fps) # 화면 표시 회수 설정만큼 루프의 간격을 둔다

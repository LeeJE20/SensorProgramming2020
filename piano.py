import pygame # pygame 모듈의 임포트
import sys # 외장 모듈
from pygame.locals import * # QUIT 등의 pygame 상수들을 로드한다.
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

led_pin1 = 14
GPIO.setup(led_pin1, GPIO.OUT)


gpio_pin = 13

scale = [ 261, 294, 329, 349, 392, 440, 493, 523 ]
GPIO.setup(gpio_pin, GPIO.OUT)
p = GPIO.PWM(gpio_pin, 100)
p.start(100) # start the PWM on 100% duty cycle
#p.ChangeDutyCycle(50)









width = 600 # 상수 설정
height = 400
white = (255, 255, 255)
black = (  0,   0,   0)
fps = 10

pygame.init() # 초기화

pygame.display.set_caption('Piano!') # 창 제목 설정
displaysurf = pygame.display.set_mode((width, height), 0, 32) # 메인 디스플레이를 설정한다
clock = pygame.time.Clock() # 시간 설정

gulimfont = pygame.font.SysFont('consolas', 30) # 서체 설정
helloworld = gulimfont.render('Hello, Piano!', 4, black) # .render() 함수에 내용과 안티앨리어싱, 색을 전달하여 글자 이미지 생성
hellorect = helloworld.get_rect() # 생성한 이미지의 rect 객체를 가져온다
hellorect.center = (width / 2, height / 2) # 해당 rect의 중앙을 화면 중앙에 맞춘다


def printText(msg, color='BLACK', pos=(50,50)):
    textSurface     = gulimfont.render(msg, True, black)
    #textSurface     = gulimfont.render(msg,True, pygame.Color(color),None)
    textRect        = textSurface.get_rect()
    textRect.topleft= pos
 
    displaysurf.blit(textSurface, textRect)

displaysurf.fill(white)

while True: # 아래의 코드를 무한 반복한다.
    
    for event in pygame.event.get(): # 발생한 입력 event 목록의 event마다 검사
        if event.type == QUIT: # event의 type이 QUIT에 해당할 경우
            GPIO.cleanup()
            pygame.quit() # pygame을 종료한다
            sys.exit() # 창을 닫는다
            

    
    
        if event.type == pygame.KEYDOWN:# If user pressed.
            print("key 이벤트 발생")
            p.ChangeDutyCycle(50)
            if event.key == pygame.K_w:
                print("w")
                printText('w1')
                GPIO.output(led_pin1, False)
                p.ChangeFrequency(scale[0])
                #time.sleep(0.5)
            elif event.key == pygame.K_a:
                print("a")
                GPIO.output(led_pin1, True)
                p.ChangeFrequency(scale[1])
                #time.sleep(0.5)
            elif event.key == pygame.K_s:
                print("Player moved down!")
            elif event.key == pygame.K_d:
                print("Player moved right!")
            else:
                p.ChangeDutyCycle(0)
                print("worng key")
                
        if event.type == pygame.KEYUP:
            
            p.ChangeDutyCycle(0)
            displaysurf.fill(white)
        
            
    #displaysurf.fill(white) # displaysurf를 하얀색으로 채운다
    displaysurf.blit(helloworld, hellorect) # displaysurf의 hellorect의 위치에 helloworld를 뿌린다
    
    pygame.display.flip() # 화면을 업데이트한다
    #clock.tick(fps) # 화면 표시 회수 설정만큼 루프의 간격을 둔다

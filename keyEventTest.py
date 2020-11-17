import keyboard #Using module keyboard
while True:#making a loop
    print("w")
    if keyboard.is_pressed('q'):#if key 'q' is pressed 
        print('You Pressed A Key!')
        break#finishing the loop
print("finish")

"""
import pygame


pygame.init()
done  = False
flag  = None
pressed = None
print("start\n")
while True:
    print("10")
    for event in pygame.event.get():# User did something
        print("12")
        if event.type == pygame.KEYDOWN:# If user release what he pressed.
            print("14")
            if event.key == pygame.K_w:
                print("Player moved up!")
            elif event.key == pygame.K_a:
                print("Player moved left!")
            elif event.key == pygame.K_s:
                print("Player moved down!")
            elif event.key == pygame.K_d:
                print("Player moved right!")

        
print("finish")
"""
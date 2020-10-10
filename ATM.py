import pygame
import sys

# initializing the constructor
pygame.init()

# screen resolution
res = (720, 720)

# opens up a window
screen = pygame.display.set_mode(res)

# white color
color = (255, 255, 255)

# light shade of the button
color_light = (170, 170, 170)

# dark shade of the button
color_dark = (100, 100, 100)

# stores the width of the
# screen into a variable
width = screen.get_width()

# stores the height of the
# screen into a variable
height = screen.get_height()

# defining a font
smallfont = pygame.font.SysFont('Corbel', 35)

# rendering a text written in
# this font
text = smallfont.render('quit', True, color)

# used to determine which screen to display
menu = "PIN"

def draw_numpad(pos):
    #if statement changes with eye tracker
    if (width / 4) + 200 <= pos[0] <= (width / 4) + 299 and (height / 4) + 300 <= pos[1] <= (height / 4) + 399:
        pygame.draw.rect(screen, color_light, [(width / 4) + 200, (height / 4) + 300, 99, 99])
        count = 1
        for i in range(3):
            for j in range(3):
                pygame.draw.rect(screen, color_dark, [(width / 4) + (j * 100), (height / 4) + (i * 100), 99, 99])
                if count == 1:
                    text = smallfont.render('1', True, color)
                    count += 1
                elif count == 2:
                    text = smallfont.render('2', True, color)
                    count += 1
                elif count == 3:
                    text = smallfont.render('3', True, color)
                    count += 1
                elif count == 4:
                    text = smallfont.render('4', True, color)
                    count += 1
                elif count == 5:
                    text = smallfont.render('5', True, color)
                    count += 1
                elif count == 6:
                    text = smallfont.render('6', True, color)
                    count += 1
                elif count == 7:
                    text = smallfont.render('7', True, color)
                    count += 1
                elif count == 8:
                    text = smallfont.render('8', True, color)
                    count += 1
                elif count == 9:
                    text = smallfont.render('9', True, color)
                    count += 1
                screen.blit(text, ((width / 4) + (j * 100) + 50, (height / 4) + (i * 100) + 50))
        pygame.draw.rect(screen, color_dark, [(width / 4) + (100), (height / 4) + (300), 99, 99])
        text = smallfont.render('0', True, color)
        screen.blit(text, ((width / 4) + (150), (height / 4) + (350)))
        text = smallfont.render('Enter', True, color)
        screen.blit(text, ((width / 4) + (210), (height / 4) + (350)))
    else:
        count = 1
        for i in range(3):
            for j in range(3):
                pygame.draw.rect(screen, color_dark, [(width / 4) + (j * 100), (height / 4) + (i * 100), 99, 99])
                if count == 1:
                    text = smallfont.render('1', True, color)
                    count += 1
                elif count == 2:
                    text = smallfont.render('2', True, color)
                    count += 1
                elif count == 3:
                    text = smallfont.render('3', True, color)
                    count += 1
                elif count == 4:
                    text = smallfont.render('4', True, color)
                    count += 1
                elif count == 5:
                    text = smallfont.render('5', True, color)
                    count += 1
                elif count == 6:
                    text = smallfont.render('6', True, color)
                    count += 1
                elif count == 7:
                    text = smallfont.render('7', True, color)
                    count += 1
                elif count == 8:
                    text = smallfont.render('8', True, color)
                    count += 1
                elif count == 9:
                    text = smallfont.render('9', True, color)
                    count += 1
                screen.blit(text, ((width / 4) + (j * 100) + 50, (height / 4) + (i * 100) + 50))
        pygame.draw.rect(screen, color_dark, [(width / 4) + (100), (height / 4) + (300), 99, 99])
        text = smallfont.render('0', True, color)
        screen.blit(text, ((width / 4) + (150), (height / 4) + (350)))

        pygame.draw.rect(screen, color_dark, [(width / 4) + (200), (height / 4) + (300), 99, 99])
        text = smallfont.render('Enter', True, color)
        screen.blit(text, ((width / 4) + (210), (height / 4) + (350)))

while True:

    for ev in pygame.event.get():

        if ev.type == pygame.QUIT:
            pygame.quit()

            # checks if a mouse is clicked
            #this can all be changed to track inputs from eye tracker
        if ev.type == pygame.MOUSEBUTTONDOWN:

            # if the mouse is clicked on the
            # button the game is terminated
            if menu == "DorW" and width / 3 <= mouse[0] <= width / 3 + 140 and height / 2 <= mouse[
                1] <= height / 2 + 40:
                menu = "Deposit"
            elif menu == "DorW" and width / 1.5 <= mouse[0] <= width / 1.5 + 180 and height / 2 <= mouse[1] <= height / 2 + 40:
                menu = "Withdrawal"
            elif menu == "PIN" and (width / 4) + 200 <= mouse[0] <= (width / 4) + 299 and (height / 4) + 300 <= mouse[1] <= (height / 4) + 399:
                menu = "DorW"
            elif menu == "Deposit" and (width / 4) + 200 <= mouse[0] <= (width / 4) + 299 and (height / 4) + 300 <= mouse[1] <= (height / 4) + 399:
                menu = "PostD"
            elif menu == "Withdrawal" and (width / 4) + 200 <= mouse[0] <= (width / 4) + 299 and (height / 4) + 300 <= mouse[1] <= (height / 4) + 399:
                menu = "PostW"
            elif (menu == "PostD" or menu == "PostW") and width / 3 <= mouse[0] <= width / 3 + 140 and height / 2 <= mouse[1] <= height / 2 + 40:
                menu = "DorW"
            elif (menu == "PostD" or menu == "PostW") and width / 1.5 <= mouse[0] <= width / 1.5 + 180 and height / 2 <= mouse[1] <= height / 2 + 40:
                pygame.quit()


            # fills the screen with a color
    screen.fill((60, 25, 60))
    if menu == "DorW":
        # stores the (x,y) coordinates into
        # the variable as a tuple
        mouse = pygame.mouse.get_pos()

        text = smallfont.render("Deposit or Withdrawal?", True, color)
        screen.blit(text, (width / 4, 50))

        # if mouse is hovered on a button it
        # changes to lighter shade
        # if statement changes with eye tracker
        if width / 3 <= mouse[0] <= width / 3 + 140 and height / 2 <= mouse[1] <= height / 2 + 40:
            pygame.draw.rect(screen, color_light, [width / 3, height / 2, 140, 40])
            pygame.draw.rect(screen, color_dark, [width / 1.5, height / 2, 180, 40])
        elif width / 1.5 <= mouse[0] <= width / 1.5 + 180 and height / 2 <= mouse[1] <= height / 2 + 40:
            pygame.draw.rect(screen, color_light, [width / 1.5, height / 2, 180, 40])
            pygame.draw.rect(screen, color_dark, [width / 3, height / 2, 140, 40])

        else:
            pygame.draw.rect(screen, color_dark, [width / 3, height / 2, 140, 40])
            pygame.draw.rect(screen, color_dark, [width / 1.5, height / 2, 180, 40])

            # superimposing the text onto our button
        text = smallfont.render('Deposit', True, color)
        screen.blit(text, (width / 3, height / 2))
        text = smallfont.render('Withdrawal', True, color)
        screen.blit(text, (width / 1.5, height / 2))

    elif menu == "PIN":
        mouse = pygame.mouse.get_pos()
        text = smallfont.render("Please enter your PIN", True, color)
        screen.blit(text, (width / 4, 50))

        draw_numpad(mouse)

    elif menu == "Deposit":
        mouse = pygame.mouse.get_pos()

        text = smallfont.render("Input Deposit amount:", True, color)
        screen.blit(text, (width / 4, 50))

        draw_numpad(mouse)

    elif menu == "Withdrawal":
        mouse = pygame.mouse.get_pos()

        text = smallfont.render("Input Withdrawal amount:", True, color)
        screen.blit(text, (width / 4, 50))

        draw_numpad(mouse)

    elif menu == "PostD":
        #This can be taken out when we get the eye tracker working
        mouse = pygame.mouse.get_pos()
        text = smallfont.render("Your money has been deposited.", True, color)
        screen.blit(text, (width / 4, 50))
        text = smallfont.render("Would you like to make another transaction?", True, color)
        screen.blit(text, (width / 8, 100))

        #if statements will change with eye tracker
        if width / 3 <= mouse[0] <= width / 3 + 100 and height / 2 <= mouse[1] <= height / 2 + 40:
            pygame.draw.rect(screen, color_light, [width / 3, height / 2, 100, 40])
            pygame.draw.rect(screen, color_dark, [width / 1.5, height / 2, 100, 40])
        elif width / 1.5 <= mouse[0] <= width / 1.5 + 100 and height / 2 <= mouse[1] <= height / 2 + 40:
            pygame.draw.rect(screen, color_light, [width / 1.5, height / 2, 100, 40])
            pygame.draw.rect(screen, color_dark, [width / 3, height / 2, 100, 40])

        else:
            pygame.draw.rect(screen, color_dark, [width / 3, height / 2, 100, 40])
            pygame.draw.rect(screen, color_dark, [width / 1.5, height / 2, 100, 40])

            # superimposing the text onto our button
        text = smallfont.render('Yes', True, color)
        screen.blit(text, (width / 3, height / 2))
        text = smallfont.render('No', True, color)
        screen.blit(text, (width / 1.5, height / 2))

    elif menu == "PostW":
        mouse = pygame.mouse.get_pos()
        text = smallfont.render("Please take your withdrawal.", True, color)
        screen.blit(text, (width / 4, 50))
        text = smallfont.render("Would you like to make another transaction?", True, color)
        screen.blit(text, (width / 8, 100))

        #if statements change with eye tracker
        if width / 3 <= mouse[0] <= width / 3 + 100 and height / 2 <= mouse[1] <= height / 2 + 40:
            pygame.draw.rect(screen, color_light, [width / 3, height / 2, 100, 40])
            pygame.draw.rect(screen, color_dark, [width / 1.5, height / 2, 100, 40])
        elif width / 1.5 <= mouse[0] <= width / 1.5 + 180 and height / 2 <= mouse[1] <= height / 2 + 40:
            pygame.draw.rect(screen, color_light, [width / 1.5, height / 2, 100, 40])
            pygame.draw.rect(screen, color_dark, [width / 3, height / 2, 100, 40])

        else:
            pygame.draw.rect(screen, color_dark, [width / 3, height / 2, 100, 40])
            pygame.draw.rect(screen, color_dark, [width / 1.5, height / 2, 100, 40])

            # superimposing the text onto our button
        text = smallfont.render('Yes', True, color)
        screen.blit(text, (width / 3, height / 2))
        text = smallfont.render('No', True, color)
        screen.blit(text, (width / 1.5, height / 2))

    # updates the frames of the game
    pygame.display.update()

import pygame

# initialize pygame
pygame.init()

# screen size
screenX = 500
screenY = 300

# scores file
file = open("scores.txt", "a")

# variables
click = False
pos = []
player = 1
winText = ""
gameEnd = False
aiBlockBool = False
aiTryWinBool = False
checkCrossBool = False
playerTurn = 0
winner = 0
# fonts
font = pygame.font.SysFont(None, 40)
scoreFont = pygame.font.SysFont(None, 22)
fontCol = (255, 255, 255)
scoreMenuText = scoreFont.render("LAST SCORES: ", False, fontCol)
# images
xImage = pygame.image.load('cross-icon.png')
oImage = pygame.image.load('circle-icon.png')
menuImage = pygame.image.load('menu-icon.png')
# functional rects
againRect = pygame.rect.Rect((screenX // 2 - 120, screenY // 2, 240, 50))
AiRect = pygame.rect.Rect((screenX // 2 - 160, screenY // 2 - 60, 300, 50))
MultiRect = pygame.rect.Rect((screenX // 2 - 160, screenY // 2, 300, 50))

# list of lists
tabOfFields = []

for i in range(3):
    row = [0] * 3
    tabOfFields.append(row)
print(tabOfFields)

# creating a screen
screen = pygame.display.set_mode((screenX, screenY))

# title and icon
pygame.display.set_caption("KÓŁKO KRZYŻYK")
icon = pygame.image.load("tic-tac-toe.png")
pygame.display.set_icon(icon)


# drawing the game board
def drawBoard():
    # rgb colors
    backGr = (68, 82, 97)
    line = (0, 61, 92)
    screen.fill(backGr)
    screen.blit(menuImage, (310, 5))
    screen.blit(scoreMenuText, (340, 55))

    for i in range(0, 4):
        pygame.draw.line(screen, line, (0, i * 100), (300, i * 100), 3)
        pygame.draw.line(screen, line, (i * 100, 0), (i * 100, screenY), 3)

    # reading the last game results from a file
    file = open("scores.txt", "r")
    if file.readable():
        text = file.readlines()
    y = 80
    for i in reversed(text):
        scoreText = scoreFont.render(i[:-1], False, fontCol)
        screen.blit(scoreText, (340, y))
        y += 25


# draw x and o on the board
def drawXAndO():
    x = 0
    for i in tabOfFields:
        y = 0
        for j in i:
            if j == 1:
                screen.blit(xImage, (x * 100 + 2, y * 100 + 2))
            if j == -1:
                screen.blit(oImage, (x * 100 + 2, y * 100 + 2))
            y += 1
        x += 1


def check_winner():
    global winner, gameEnd
    notEmpty = 0
    # check game over with no winner
    for i in range(3):
        for j in range(3):
            if tabOfFields[i][j] != 0:
                notEmpty += 1
    if notEmpty == 9:
        winner = 3
        gameEnd = True

    y = 0
    for x in tabOfFields:
        # check in columns
        if sum(x) == 3:
            winner = 1
            gameEnd = True
        if sum(x) == -3:
            winner = 2
            gameEnd = True
        # check in rows
        if tabOfFields[0][y] + tabOfFields[1][y] + tabOfFields[2][y] == 3:
            winner = 1
            gameEnd = True
        if tabOfFields[0][y] + tabOfFields[1][y] + tabOfFields[2][y] == -3:
            winner = 2
            gameEnd = True
        y += 1

        # check cross
        if tabOfFields[0][0] + tabOfFields[1][1] + tabOfFields[2][2] == 3 or tabOfFields[0][2] + tabOfFields[1][1] + \
                tabOfFields[2][0] == 3:
            winner = 1
            gameEnd = True
        if tabOfFields[0][0] + tabOfFields[1][1] + tabOfFields[2][2] == -3 or tabOfFields[0][2] + tabOfFields[1][1] + \
                tabOfFields[2][0] == -3:
            winner = 2
            gameEnd = True


# choose the best available field on the board centre --> corners ..
def aiFindBestField():
    # center
    if tabOfFields[1][1] == 0:
        tabOfFields[1][1] = -1
    # corners
    elif tabOfFields[2][2] == 0:
        tabOfFields[2][2] = -1
    elif tabOfFields[0][0] == 0:
        tabOfFields[0][0] = -1
    elif tabOfFields[2][0] == 0:
        tabOfFields[2][0] = -1
    elif tabOfFields[0][2] == 0:
        tabOfFields[0][2] = -1
    # else
    elif tabOfFields[1][0] == 0:
        tabOfFields[1][0] = -1
    elif tabOfFields[1][2] == 0:
        tabOfFields[1][2] = -1
    elif tabOfFields[0][1] == 0:
        tabOfFields[0][1] = -1
    elif tabOfFields[2][1]:
        tabOfFields[2][1] = -1


# check if you need to block the player's next move
# check columns, rows and cross
def aiBlock():
    global winner, gameEnd, aiBlockBool, tabOfFields

    y = 0
    col = 0
    row = 0
    for x in tabOfFields:

        # columns
        if sum(x) == 2:
            for i in range(3):
                if tabOfFields[col][i] == 0:
                    tabOfFields[col][i] = -1
                    aiBlockBool = True
                    return aiBlockBool
        col += 1

        # rows
        if tabOfFields[0][y] + tabOfFields[1][y] + tabOfFields[2][y] == 2:
            for i in range(3):
                if tabOfFields[i][row] == 0:
                    tabOfFields[i][row] = -1
                    aiBlockBool = True
                    return aiBlockBool
        row += 1
        y += 1

        # cross
        if tabOfFields[0][0] + tabOfFields[1][1] + tabOfFields[2][2] == 2:
            for i in range(3):
                if tabOfFields[i][i] == 0:
                    tabOfFields[i][i] = -1
                    aiBlockBool = True
                    return aiBlockBool

        if tabOfFields[0][2] + tabOfFields[1][1] + tabOfFields[2][0] == 2:
            j = 2
            for i in range(3):
                if tabOfFields[i][j] == 0:
                    tabOfFields[i][j] = -1
                    aiBlockBool = True
                    return aiBlockBool
                j -= 1


# protection against losing in the initial phase when the opponent marks two opposite corners
def checkCross():
    global checkCrossBool
    if tabOfFields[0][0] == 1 and tabOfFields[1][1] == -1 and tabOfFields[2][2] == 1:
        if tabOfFields[0][1] == 0:
            tabOfFields[0][1] = -1
        elif tabOfFields[1][0] == 0:
            tabOfFields[1][0] = -1
        checkCrossBool = True
        return checkCrossBool

    if tabOfFields[0][2] == 1 and tabOfFields[1][1] == -1 and tabOfFields[2][0] == 1:
        if tabOfFields[0][1] == 0:
            tabOfFields[0][1] = -1
        elif tabOfFields[1][0] == 0:
            tabOfFields[1][0] = -1
        checkCrossBool = True
        return checkCrossBool


# check the columns, rows and cross to see if you can win the next move
def aiTryToWin():
    global winner, gameEnd, aiTryWinBool, tabOfFields
    y = 0
    col = 0
    row = 0

    for x in tabOfFields:

        # columns
        if sum(x) == -2:
            for i in range(3):
                if tabOfFields[col][i] == 0:
                    tabOfFields[col][i] = -1
                    aiTryWinBool = True
                    return aiTryWinBool
        col += 1

        # rows
        if tabOfFields[0][y] + tabOfFields[1][y] + tabOfFields[2][y] == -2:
            for i in range(3):
                if tabOfFields[i][row] == 0:
                    tabOfFields[i][row] = -1
                    aiTryWinBool = True
                    return aiTryWinBool
        row += 1
        y += 1

        # cross
        if tabOfFields[0][0] + tabOfFields[1][1] + tabOfFields[2][2] == -2:
            for i in range(3):
                if tabOfFields[i][i] == 0:
                    tabOfFields[i][i] = -1
                    aiTryWinBool = True
                    return aiTryWinBool

        if tabOfFields[0][2] + tabOfFields[1][1] + tabOfFields[2][0] == -2:
            j = 2
            for i in range(3):
                if tabOfFields[i][j] == 0:
                    tabOfFields[i][j] = -1
                    aiTryWinBool = True
                    return aiTryWinBool
                j -= 1

    # aiTryWinBool = False
    return aiTryWinBool


# draw a win and play again message
def draw_winner(winner, x):
    global winText
    if winner + x == 3:
        winText = " Computer wins!"
    elif winner == 3:
        winText = ' No  one  wins !'
    else:
        winText = ' Player  ' + str(winner) + '  wins!'

    win_img = font.render(winText, True, fontCol)
    pygame.draw.rect(screen, (68, 82, 97), (screenX // 2 - 120, screenY // 2 - 60, 240, 50))
    pygame.draw.rect(screen, (0, 0, 0), (screenX // 2 - 120, screenY // 2 - 60, 240, 50), 3)
    screen.blit(win_img, (screenX // 2 - 110, screenY // 2 - 50))

    againText = 'Play Again?'
    againImg = font.render(againText, True, fontCol)
    pygame.draw.rect(screen, (68, 82, 97), againRect)
    pygame.draw.rect(screen, (0, 0, 0), (screenX // 2 - 120, screenY // 2, 240, 50), 3)
    screen.blit(againImg, (screenX // 2 - 85, screenY // 2 + 10))


# game selection window
def drawTypeWindow():
    AiText = 'Player VS Computer'
    AiImg = font.render(AiText, True, fontCol)
    pygame.draw.rect(screen, (68, 82, 97), AiRect)
    pygame.draw.rect(screen, (0, 0, 0), (screenX // 2 - 160, screenY // 2 - 60, 300, 50), 3)
    screen.blit(AiImg, (screenX // 2 - 145, screenY // 2 - 50))

    MultiText = 'Multiplayer'
    MultiImg = font.render(MultiText, True, fontCol)
    pygame.draw.rect(screen, (68, 82, 97), MultiRect)
    pygame.draw.rect(screen, (0, 0, 0), (screenX // 2 - 160, screenY // 2, 300, 50), 3)
    screen.blit(MultiImg, (screenX // 2 - 85, screenY // 2 + 10))


# start window
def start():
    drawBoard()
    drawTypeWindow()


# player vs computer loop
def playerVsComputer():
    global tabOfFields, checkCrossBool, player, winner, click, gameEnd, playerTurn, aiBlockBool, aiTryWinBool

    running = True
    while running:

        drawBoard()
        drawXAndO()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if gameEnd == 0 and player == 1:
                if event.type == pygame.MOUSEBUTTONDOWN and click == False:
                    click = True
                if event.type == pygame.MOUSEBUTTONUP and click == True:
                    click = False
                    pos = pygame.mouse.get_pos()
                    cellX = pos[0]
                    cellY = pos[1]
                    if tabOfFields[cellX // 100][cellY // 100] == 0:
                        tabOfFields[cellX // 100][cellY // 100] = player
                        player *= -1
                        check_winner()
                        playerTurn += 1

            elif gameEnd == 0 and player == -1:
                if playerTurn < 2:
                    aiFindBestField()

                elif playerTurn < 3:
                    checkCross()
                    if not checkCrossBool:
                        aiBlock()
                        if not aiBlockBool:
                            aiFindBestField()

                else:
                    aiTryToWin()
                    if not aiTryWinBool:
                        aiBlock()
                        if not aiBlockBool:
                            aiFindBestField()

                player *= -1
                check_winner()
                aiBlockBool = False
                aiTryWinBool = False
                checkCrossBool = False

        if gameEnd:
            draw_winner(winner, 1)
            # check for clik
            if event.type == pygame.MOUSEBUTTONDOWN and click == False:
                click = True
            if event.type == pygame.MOUSEBUTTONUP and click == True:
                click = False
                pos = pygame.mouse.get_pos()
                if againRect.collidepoint(pos):
                    # reset
                    tabOfFields = []
                    pos = []
                    player = 1
                    winner = 0
                    gameEnd = False
                    playerTurn = 0
                    for i in range(3):
                        row = [0] * 3
                        tabOfFields.append(row)
                    file = open("scores.txt", "a")
                    if file.writable():
                        file.write(str(winText) + "\n")
                    file.close()
                    startWindowLoop()
        # updating
        pygame.display.update()
    pygame.quit()


# multiplayer loop
def multiplayer():
    global tabOfFields, player, winner, click, gameEnd

    running = True
    while running:

        drawBoard()
        drawXAndO()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if gameEnd == 0:
                if event.type == pygame.MOUSEBUTTONDOWN and click == False:
                    click = True
                if event.type == pygame.MOUSEBUTTONUP and click == True:
                    click = False
                    pos = pygame.mouse.get_pos()
                    cellX = pos[0]
                    cellY = pos[1]
                    if tabOfFields[cellX // 100][cellY // 100] == 0:
                        tabOfFields[cellX // 100][cellY // 100] = player
                        player *= -1
                        check_winner()

        if gameEnd == True:
            draw_winner(winner, 0)

            # check for clik
            if event.type == pygame.MOUSEBUTTONDOWN and click == False:
                click = True
            if event.type == pygame.MOUSEBUTTONUP and click == True:
                click = False
                pos = pygame.mouse.get_pos()
                if againRect.collidepoint(pos):
                    # reset
                    tabOfFields = []
                    pos = []
                    player = 1
                    winner = 0
                    gameEnd = False

                    for i in range(3):
                        row = [0] * 3
                        tabOfFields.append(row)
                    file = open("scores.txt", "a")
                    if file.writable():
                        file.write(str(winText) + "\n")
                    file.close()
                    startWindowLoop()
        # updating
        pygame.display.update()
    pygame.quit()


def startWindowLoop():
    global click
    run = True
    while run:
        start()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN and click == False:
                click = True
            if event.type == pygame.MOUSEBUTTONUP and click == True:
                click = False
                pos = pygame.mouse.get_pos()
                if MultiRect.collidepoint(pos):
                    multiplayer()
                if AiRect.collidepoint(pos):
                    playerVsComputer()

        pygame.display.update()
    pygame.quit()


#main loop
run = True
while run:
    startWindowLoop()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and click == False:
            click = True
        if event.type == pygame.MOUSEBUTTONUP and click == True:
            click = False
    pygame.display.update()

pygame.quit()

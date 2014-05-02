# Gems
# Jessica Rex
# Python Creative Inquiry

import pygame, time, random, sys, copy
from pygame.locals import *

# program window dimensions
WINDOWHEIGHT = 600 # height (pixels)
WINDOWWIDTH  = 1000 # width (pixels)

# board dimensions
BOARDHEIGHT = 8 # rows
BOARDWIDTH  = 8 # columns
GEMBOX = 64     # each space

# RGB colors used in the game
RED   = (255,     0,   0)
BLUE  = (  0,   102, 204)
WHITE = (255,   255, 255)
BLACK = (  0,     0,   0)
SAND  = (244,   164,  96)

SELECTBORDERCOLOR = RED  # color of border of selection
SCORECOLOR        = WHITE # color of score
OVERCOLOR         = RED   # color for Game Over
OVERBACKCOLOR     = BLACK # background for Game OVER
BACKGROUND        = BLUE
BOARDBACKGROUND   = SAND

GEMNUMS = 9 # number of gem types
assert GEMNUMS >= 5

FPS = 15       # frames per second
MOVESPEED = 40 # animation speed

# direction constants- only ways you can move (i.e. no diagonal)
RIGHT = 'right'
LEFT  = 'left'
UP    = 'up'
DOWN  = 'down'

EMPTY_BOX = -1
FALLINGROW = 'falling row' # row above board that falls

# space from sides of board to window edge
XEDGE = int((WINDOWWIDTH - GEMBOX * BOARDWIDTH) /2)
YEDGE = int((WINDOWHEIGHT - GEMBOX * BOARDHEIGHT) /2)

def main():
    global GEMPICS, FONT, BOARDRECTS, DISPLAY

    # set up
    pygame.init()
    DISPLAY = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('Gems')
    FONT = pygame.font.Font('Kleymissky_0283.otf', 32)

    # load in images to GEMPICS
    GEMPICS = []
    for i in range(1, GEMNUMS + 1):
        gemPic = pygame.image.load('gem%s.png' % i)
        if gemPic.get_size() != (GEMBOX, GEMBOX):
            gemPic = pygame.transform.smoothscale(gemPic, (GEMBOX, GEMBOX))
        GEMPICS.append(gemPic)

    # use pygame.Rect objects for the board spaces
    # useful for board to pixel coordinate translations
    BOARDRECTS = []
    for x in range(BOARDWIDTH):
        BOARDRECTS.append([])
        for y in range(BOARDHEIGHT):
            s = pygame.Rect((XEDGE + (x * GEMBOX), YEDGE + (y * GEMBOX),
                             GEMBOX, GEMBOX))
            BOARDRECTS[x].append(s)

    # actually set the game to run
    while True:
        playGame()

    pygame.quit()


def playGame():
    # board initialization
    board = getBlank()
    score = 0
    level = 1
    totalScore = 0 # internal, used to keep track of score for entire game
    fillAndAnimate(board, [], score)

    # start of game initialization
    gameOver = False
    continueTextSurf = None
    gameOverTextSurf = None
    firstGemPick = None
    lastMouseDownY = None
    lastMouseDownX = None

    # display the directions
    welcomeTextSurf = None
    welcomeTextSurf = FONT.render('Welcome to Gems! Match gems in groups of 3 or more to earn at least 70 points and advance!', 1, OVERCOLOR, OVERBACKCOLOR)
    welcomeTextRect = welcomeTextSurf.get_rect()
    welcomeTextRect.center = int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2)
    DISPLAY.blit(welcomeTextSurf, welcomeTextRect)
    pygame.display.update()  # update the display
    pygame.time.delay(10000) # give them time to read the directions

    # main loop for the game
    while True:
        chosenBox = None
        for event in pygame.event.get():
            # handle exiting the game
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == KEYUP and event.key == K_BACKSPACE:
                return # begin new game
            elif event.type == MOUSEBUTTONUP:
                if gameOver:
                    return
                if event.pos == (lastMouseDownX, lastMouseDownY):
                    chosenBox = checkForClick(event.pos)
                else:
                    firstGemPick = checkForClick((lastMouseDownX, lastMouseDownY))
                    chosenBox    = checkForClick(event.pos)
                    if not firstGemPick or not chosenBox:
                        # invalid drag, deselect both
                        firstGemPick = None
                        chosenBox = None
            elif event.type == MOUSEBUTTONDOWN:
                # start of mouse click or drag
                lastMouseDownX, lastMouseDownY = event.pos

        if chosenBox and not firstGemPick:
            # was first gem clicked on
            firstGemPick = chosenBox
        elif chosenBox and firstGemPick:
            # two gems clicked, swap them
            firstSwapGem, secondSwapGem = getSwap(board, firstGemPick, chosenBox)
            if firstSwapGem == None and secondSwapGem == None:
                # gems weren't adjacent- no swap
                firstGemPick = None  # deselect
                continue

            # show swap animation
            boardCopy = getBoardCopyNoGems(board, (firstSwapGem, secondSwapGem))
            animateMove(boardCopy, [firstSwapGem, secondSwapGem], [], score)

            # swap gems in board structure
            board[firstSwapGem['x']][firstSwapGem['y']] = secondSwapGem['imageNum']
            board[secondSwapGem['x']][secondSwapGem['y']] = firstSwapGem['imageNum']

            # see if it was matching
            matchedGems = findMatches(board)
            if matchedGems == []:
                # was an invalid match, swap back
                animateMove(boardCopy, [firstSwapGem, secondSwapGem], [], score)
                board[firstSwapGem['x']][firstSwapGem['y']] = firstSwapGem['imageNum']
                board[secondSwapGem['x']][secondSwapGem['y']] = secondSwapGem['imageNum']
            else:
                # matching move
                addPoints = 0
                while matchedGems != []:
                    # remove matched gems, pull board down

                    points = []
                    for gemSet in matchedGems:
                        addPoints += (10 + (len(gemSet) - 3) * 10)
                        for gem in gemSet:
                            board[gem[0]][gem[1]] = EMPTY_BOX
                        points.append({'points': addPoints,
                                       'x': gem[0] * GEMBOX + XEDGE,
                                       'y': gem[1] * GEMBOX + YEDGE})
                    score += addPoints

                    # drop new gems
                    fillAndAnimate(board, points, score)

                    # check for new matches
                    matchedGems = findMatches(board)
            firstGemPick = None

            if not possibleMove(board):
                if score >= 100:
                    continueTextSurf = FONT.render('You have passed this level with a score of %s. Pass the hangman challenge to continue.' % (score), 1, OVERCOLOR, OVERBACKCOLOR)
                    continueTextRect = continueTextSurf.get_rect()
                    continueTextRect.center = int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2)
                    DISPLAY.blit(continueTextSurf, continueTextRect)
                    pygame.display.update()
                    import hangman
                    if hangman.play():
                        gameOver = False
                        level += 1
                        totalScore += score
                        board = getBlank()
                        score = 0
                        fillAndAnimate(board, points, score)
                    else:
                        totalScore += score
                        gameOver = True
                else:
                    totalScore += score
                    gameOver = True
            
        # draw board
        DISPLAY.fill(BACKGROUND)
        drawBoard(board)
        if firstGemPick != None:
            selectSpace(firstGemPick['x'], firstGemPick['y'])
        if gameOver:
            if gameOverTextSurf == None:
                # renders text
                if level == 1:
                    gameOverTextSurf = FONT.render('Game Over. Your Final Score is: %s (Click to start over)' % (score), 1, OVERCOLOR, OVERBACKCOLOR)
                else:
                    gameOverTextSurf = FONT.render('Game Over. Your Final Score is: %s (Click to start over)' % (totalScore), 1, OVERCOLOR, OVERBACKCOLOR)
                gameOverTextRect = gameOverTextSurf.get_rect()
                gameOverTextRect.center = int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2)
            DISPLAY.blit(gameOverTextSurf, gameOverTextRect)
        displayLevel(level)
        displayScore(score)
        pygame.display.update()

def getGem(board, x, y):
    if x < 0 or y < 0 or x >= BOARDWIDTH or y >= BOARDHEIGHT:
       return None
    else:
        return board[x][y]

# takes (X, Y) coordinates of two gems; if they are adjacent, then 'direction' keys
# are set so that they will have appropriate direction keys when swapped
def getSwap(board, gemOneXY, gemTwoXY):
    gemOne = {'imageNum': board[gemOneXY['x']][gemOneXY['y']],
                'x': gemOneXY['x'],
                'y': gemOneXY['y']}
    gemTwo = {'imageNum': board[gemTwoXY['x']][gemTwoXY['y']],
                 'x': gemTwoXY['x'],
                 'y': gemTwoXY['y']}
    selectedGem = None
    # swapping horizontally (2 ways)
    if gemOne['x'] == gemTwo['x'] + 1 and gemOne['y'] == gemTwo['y']:
        gemOne['direction'] = LEFT
        gemTwo['direction'] = RIGHT
    elif gemOne['x'] == gemTwo['x'] - 1 and gemOne['y'] == gemTwo['y']:
        gemOne['direction'] = RIGHT
        gemTwo['direction'] = LEFT
    # swapping vertically (2 ways)
    elif gemOne['y'] == gemTwo['y'] + 1 and gemOne['x'] == gemTwo['x']:
        gemOne['direction'] = UP
        gemTwo['direction'] = DOWN
    elif gemOne['y'] == gemTwo['y'] - 1 and gemOne['x'] == gemTwo['x']:
        gemOne['direction'] = DOWN
        gemTwo['direction'] = UP
    else:
        # Gems are not adjacent; can't be swapped.
        return None, None
    return gemOne, gemTwo

# returns true is a matching move is possible on the current board
def possibleMove(board):
    # if we look at a set of three gems, we can view them as coordinates relative
    # to each other using numbers 0-3

    # we'll make a structure of configurations where it only takes one move
    # to make a triplet
    # for example ((0,1), (1,0), (2,0)) refers to:
    #     ()
    #    ()
    #    ()
    # where the () are the gems. each coordinate pair refers to one of the
    # gems, in order going down vertically, and their offset from the space
    # next to the first gem. there are 8 possible ways to be one away:
    
    oneMoveAway = (((0,1), (1,0), (2,0)),
                   ((0,1), (1,1), (2,0)),
                   ((0,0), (1,1), (2,0)),
                   ((0,1), (1,0), (2,1)),
                   ((0,0), (1,0), (2,1)),
                   ((0,0), (1,1), (2,1)),
                   ((0,0), (0,2), (0,3)),
                   ((0,0), (0,1), (0,3)))

    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            for check in oneMoveAway:
                # check each pattern to see if a move can be made
                if (getGem(board, x+check[0][0], y+check[0][1]) == \
                    getGem(board, x+check[1][0], y+check[1][1]) == \
                    getGem(board, x+check[2][0], y+check[2][1]) != None) or \
                   (getGem(board, x+check[0][1], y+check[0][0]) == \
                    getGem(board, x+check[1][1], y+check[1][0]) == \
                    getGem(board, x+check[2][1], y+check[2][0]) != None):
                    return True # return True the first time you find a move
    return False

# draws gem sliding the way its key indicates
# transition- a number between 0 and 100 indicating the progress of the move
def drawGemMove(gem, transition):
    moveX = 0
    moveY = 0
    transition = transition * 0.01

    if gem['direction'] == UP:
        moveY = -int(transition * GEMBOX)
    elif gem['direction'] == DOWN:
        moveY = int(transition * GEMBOX)
    elif gem['direction'] == RIGHT:
        moveX = int(transition * GEMBOX)
    elif gem['direction'] == LEFT:
        moveX = -int(transition * GEMBOX)

    baseX = gem['x']
    baseY = gem['y']
    if baseY == FALLINGROW:
        baseY = -1

    pixelX = XEDGE + (baseX * GEMBOX)
    pixelY = YEDGE + (baseY * GEMBOX)
    r = pygame.Rect( (pixelX + moveX, pixelY + moveY, GEMBOX, GEMBOX) )
    DISPLAY.blit(GEMPICS[gem['imageNum']], r)
    

def getBlank():
    # create blank board
    board = []
    for x in range(BOARDWIDTH):
        board.append([EMPTY_BOX] * BOARDHEIGHT)
    return board

# pulls down the gems to fill holes
def pullDown(board):
    for x in range(BOARDWIDTH):
        columnGems = []
        for y in range(BOARDHEIGHT):
            if board[x][y] != EMPTY_BOX:
                columnGems.append(board[x][y])
        board[x] = ([EMPTY_BOX] * (BOARDHEIGHT - len(columnGems))) + columnGems

def findMatches(board):
    matchingGems = [] # a list of lists of matching gems that should be removed
    boardCopy = copy.deepcopy(board)

    # loop through each space, checking for 3 adjacent identical gems
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            # look for horizontal matches
            if getGem(boardCopy, x, y) == getGem(boardCopy, x + 1, y) == getGem(boardCopy, x + 2, y) and getGem(boardCopy, x, y) != EMPTY_BOX:
                targetGem = boardCopy[x][y]
                offset = 0
                matchedSet = []
                while getGem(boardCopy, x + offset, y) == targetGem:
                    # keep checking if there's more than 3 gems in a row
                    matchedSet.append((x + offset, y))
                    boardCopy[x + offset][y] = EMPTY_BOX
                    offset += 1
                matchingGems.append(matchedSet)

            # look for vertical matches
            if getGem(boardCopy, x, y) == getGem(boardCopy, x, y + 1) == getGem(boardCopy, x, y + 2) and getGem(boardCopy, x, y) != EMPTY_BOX:
                targetGem = boardCopy[x][y]
                offset = 0
                matchedSet = []
                while getGem(boardCopy, x, y + offset) == targetGem:
                    # keep checking, in case there's more than 3 gems in a row
                    matchedSet.append((x, y + offset))
                    boardCopy[x][y + offset] = EMPTY_BOX
                    offset += 1
                matchingGems.append(matchedSet)

    return matchingGems

# find gems with empty space below them
def getFallingGems(board):
    boardCopy = copy.deepcopy(board)
    fallingGems = []
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT - 2, -1, -1):
            if boardCopy[x][y + 1] == EMPTY_BOX and boardCopy[x][y] != EMPTY_BOX:
                # space drops if not empty but the space below it is
                fallingGems.append( {'imageNum': boardCopy[x][y], 'x': x, 'y': y, 'direction': DOWN} )
                boardCopy[x][y] = EMPTY_BOX
    return fallingGems

def animateMove(board, gems, scoreText, score):
    transition = 0 # 0 represents beginning, 100 means finished.
    while transition < 100: # animation loop
        DISPLAY.fill(BACKGROUND)
        drawBoard(board)
        for gem in gems: # Draw each gem.
            drawGemMove(gem, transition)
        displayScore(score)
        for scores in scoreText:
            scoresSurf = FONT.render(str(scores['points']), 1, SCORECOLOR)
            scoresRect = scoresSurf.get_rect()
            scoresRect.center = (scores['x'], scores['y'])
            DISPLAY.blit(scoresSurf, scoresRect)

        pygame.display.update()
        #FPSCLOCK.tick(FPS)
        transition += MOVESPEED # progress the animation a little bit more for the next frame

def getColumnSlots(board):
    # Creates a slot for each column, fills it with number of gems it's missing
    # assumes gems have been dropped by gravity already
    boardCopy = copy.deepcopy(board)
    pullDown(boardCopy)

    colSlots = []
    for i in range(BOARDWIDTH):
        colSlots.append([])

    # count number of empty spaces in each column
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT-1, -1, -1): # start from bottom, go up
            if boardCopy[x][y] == EMPTY_BOX:
                potentialGems = list(range(len(GEMPICS)))
                for offsetX, offsetY in ((0, -1), (1, 0), (0, 1), (-1, 0)):
                    # Narrow down possible gems we should put in the
                    # blank space so we don't put two of the same gems
                    # next to each other
                    neighborGem = getGem(boardCopy, x + offsetX, y + offsetY)
                    if neighborGem != None and neighborGem in potentialGems:
                        potentialGems.remove(neighborGem)

                newGem = random.choice(potentialGems)
                boardCopy[x][y] = newGem
                colSlots[x].append(newGem)
    return colSlots

# gems is list of dicts
def moveGems(board, gems):
    for gem in gems:
        if gem['y'] != FALLINGROW:
            board[gem['x']][gem['y']] = EMPTY_BOX
            moveX = 0
            moveY = 0
            if gem['direction'] == LEFT:
                moveX = -1
            elif gem['direction'] == RIGHT:
                moveX = 1
            elif gem['direction'] == DOWN:
                moveY = 1
            elif gem['direction'] == UP:
                moveY = -1
            board[gem['x'] + moveX][gem['y'] + moveY] = gem['imageNum']
        else:
            # gem is located above the board (where new gems come from)
            board[gem['x']][0] = gem['imageNum'] # move to top row

def fillAndAnimate(board, points, score):
    colSlots = getColumnSlots(board)
    while colSlots != [[]] * BOARDWIDTH:
        # do the falling animation as long as there are more gems to drop
        fallingGems = getFallingGems(board)
        for x in range(len(colSlots)):
            if len(colSlots[x]) != 0:
                # cause the lowest gem in each slot to begin moving in the DOWN direction
                fallingGems.append({'imageNum': colSlots[x][0], 'x': x, 'y': FALLINGROW, 'direction': DOWN})

        boardCopy = getBoardCopyNoGems(board, fallingGems)
        animateMove(boardCopy, fallingGems, points, score)
        moveGems(board, fallingGems)

        # Make the next row of gems from the drop slots
        # the lowest by deleting the previous lowest gems.
        for x in range(len(colSlots)):
            if len(colSlots[x]) == 0:
                continue
            board[x][0] = colSlots[x][0]
            del colSlots[x][0]

def drawBoard(board):
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            pygame.draw.rect(DISPLAY, BOARDBACKGROUND, BOARDRECTS[x][y], 1)
            gemToDraw = board[x][y]
            if gemToDraw != EMPTY_BOX:
                DISPLAY.blit(GEMPICS[gemToDraw], BOARDRECTS[x][y])

# creates and returns copy of passed board data structure with no gems
def getBoardCopyNoGems(board, gems):
    boardCopy = copy.deepcopy(board)

    # Remove some of the gems from this board data structure copy.
    for gem in gems:
        if gem['y'] != FALLINGROW:
            boardCopy[gem['x']][gem['y']] = EMPTY_BOX
    return boardCopy

def selectSpace(x, y):
    pygame.draw.rect(DISPLAY, SELECTBORDERCOLOR, BOARDRECTS[x][y], 4)

# see if mouse click was on the board
def checkForClick(position):
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            if BOARDRECTS[x][y].collidepoint(position[0], position[1]):
                return {'x': x, 'y': y}
    return None # click not on the board

def displayScore(score):
    scorePic  = FONT.render('Score: %s' % (score), 1, SCORECOLOR)
    scoreRect = scorePic.get_rect()
    scoreRect.bottomleft = (10, WINDOWHEIGHT - 6)
    DISPLAY.blit(scorePic, scoreRect)

def displayLevel(level):
    levelPic = FONT.render('Level: %s' % (level), 1, SCORECOLOR)
    levelRect = levelPic.get_rect()
    levelRect.bottomleft = (10, WINDOWHEIGHT - 50)
    DISPLAY.blit(levelPic, levelRect)

if __name__ == '__main__':
    main()
    import hangman
    

import os
from GameState import GameState, GameSetup
from GraphicModeFunctions import allMarbleColors

def createSaveFile(gameSetup, gameState):
    """Called when the player wants to save the game
    Creates a new save file and writes the essential information about the saved game on different lines """

    if os.path.exists("saveFile.txt"):
        os.remove("saveFile.txt")
    f = open("saveFile.txt", "w+")
    f.write(gameSetup.gameMode)
    f.write("\n")
    f.write("AI? ")
    f.write(str(gameSetup.gameAgainstAI))
    f.write(" ")
    f.write(str(gameSetup.difficultyAI))
    f.write("\n")
    
    f.write("playerColors %d %d\n" % (gameSetup.playerColors[0], gameSetup.playerColors[1]))
    f.write("player1name %s\n" % (gameSetup.playerNames[0]))
    f.write("player2name %s\n" % (gameSetup.playerNames[1]))
    if gameSetup.gameAgainstAI:
        f.write("currentPlayer 1\n")
    else:
        f.write("currentPlayer %d\n" % (gameState.currentPlayer))
    f.write("score %d %d\n" % (gameState.score[0], gameState.score[1]))
    f.write("totalNbTurns %d %d\n" % (gameState.totalNbTurns[0], gameState.totalNbTurns[1]))
    f.write("nbSimpleMoves %d %d\n" % (gameState.nbSimpleMoves[0], gameState.nbSimpleMoves[1]))
    f.write("totalNbJumps %d %d\n" % (gameState.totalNbJumps[0], gameState.totalNbJumps[1]))
    f.write("grid\n")

    for i in range (25):
        for j in range (17):
            if gameState.grid[i][j] is None:
                f.write("%d %d None\n" % (i, j))
            else:
                f.write("%d %d %d\n" % (i, j, gameState.grid[i][j]))

def extractSaveFile():
    """Called when the player wants to play the game that was previously saved
    Opens the save file and reads each line one by one to extract all the information and put it the game"""

    file = open("saveFile.txt", "r")
    gameSetup = GameSetup()
    line_1 = file.readline().split()
    gameSetup.gameMode = ""
    for i in range (0, len(line_1)):
        gameSetup.gameMode += line_1[i]
        if i != len(line_1) - 1:
            gameSetup.gameMode += " "
    line_2 = file.readline().split()
    if line_2[1] == "True":
        gameSetup.gameAgainstAI = True
    else:
        gameSetup.gameAgainstAI = False
    gameSetup.difficultyAI = line_2[2]
    line_3 = file.readline().split()
    gameSetup.playerColors = [allMarbleColors[int(line_3[1])], allMarbleColors[int(line_3[2])]]
    line_4 = file.readline().split()
    gameSetup.playerNames = ["", ""]
    for i in range (1, len(line_4)):
        gameSetup.playerNames[0] += line_4[i]
        if i != len(line_4) - 1:
            gameSetup.playerNames[0] += " "
    line_5 = file.readline().split()
    for i in range (1, len(line_5)):
        gameSetup.playerNames[1] += line_5[i]
        if i != len(line_5) - 1:
            gameSetup.playerNames[1] += " "

    gameState = GameState(gameSetup)
    line_6 = file.readline().split()
    gameState.currentPlayer = int(line_6[1])
    line_7 = file.readline().split()
    gameState.score = [int(line_7[1]), int(line_7[2])]
    line_8 = file.readline().split()
    gameState.totalNbTurns = [int(line_8[1]),int(line_8[2])]
    line_9 = file.readline().split()
    gameState.nbSimpleMoves = [int(line_9[1]), int(line_9[2])]
    line_10 = file.readline().split()
    gameState.totalNbJumps = [int(line_10[1]), int(line_10[2])]
    file.readline()
    for i in range (12, 437):
        line = file.readline().split()
        if line[2] == "None":
            line[2] = None
        else:
            line[2] = int(line[2])
        gameState.grid[int(line[0])][int(line[1])] = line[2]

    return (gameSetup, gameState)

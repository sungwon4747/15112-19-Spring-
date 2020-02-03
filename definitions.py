#This function returns True if waterballoon hits something in four different directions, depending on how large the range is
def reactToBalloon(balloonCoord, monsterCoord, numSoda, maze):
    if balloonCoord == monsterCoord:
        return True
    elif numSoda == 0:
        if balloonCoord[0]+1 < 13:
            if balloonCoord[0]+1 == monsterCoord[0] and\
             balloonCoord[1] == monsterCoord[1]:
                return True
        if balloonCoord[0]-1 > -1:
            if balloonCoord[0]-1 == monsterCoord[0] and\
             balloonCoord[1] == monsterCoord[1]:
                return True
        if balloonCoord[1]+1 < 8:
            if balloonCoord[1]+1 == monsterCoord[1] and\
             balloonCoord[0] == monsterCoord[0]:
                return True
        if balloonCoord[1]-1 > -1:
            if balloonCoord[1]-1 == monsterCoord[1] and\
             balloonCoord[0] == monsterCoord[0]:
                return True
    elif numSoda == 1:
        if balloonCoord[0]+1 < 13:
            if maze[balloonCoord[1]][balloonCoord[0]+1] != 0:
                return False
            elif balloonCoord[0]+1 == monsterCoord[0] and\
             balloonCoord[1] == monsterCoord[1]:
                return True
            elif balloonCoord[0]+2 < 13:
                if maze[balloonCoord[1]][balloonCoord[0]+2] != 0:
                    return False
                elif balloonCoord[0]+2 == monsterCoord[0] and\
                 balloonCoord[1] == monsterCoord[1]:
                    return True
        if balloonCoord[0]-1 > -1:
            if maze[balloonCoord[1]][balloonCoord[0]-1] != 0:
                return False
            elif balloonCoord[0]-1 == monsterCoord[0] and\
             balloonCoord[1] == monsterCoord[1]:
                return True
            elif balloonCoord[0]-2 > -1:
                if maze[balloonCoord[1]][balloonCoord[0]-2] != 0:
                    return False
                elif balloonCoord[0]-2 == monsterCoord[0] and\
                 balloonCoord[1] == monsterCoord[1]:
                    return True
        if balloonCoord[1]+1 < 8:
            if maze[balloonCoord[1]+1][balloonCoord[0]] != 0:
                return False
            elif balloonCoord[1]+1 == monsterCoord[1] and\
             balloonCoord[0] == monsterCoord[0]:
                return True
            elif balloonCoord[1]+2 < 8:
                if maze[balloonCoord[1]+2][balloonCoord[0]] != 0:
                    return False
                elif balloonCoord[1]+2 == monsterCoord[1] and\
                 balloonCoord[0] == monsterCoord[0]:
                    return True
        if balloonCoord[1]-1 > -1:
            if maze[balloonCoord[1]-1][balloonCoord[0]] != 0:
                return False
            elif balloonCoord[1]-1 == monsterCoord[1] and\
             balloonCoord[0] == monsterCoord[0]:
                return True
            elif balloonCoord[1]-2 > -1:
                if maze[balloonCoord[1]-2][balloonCoord[0]] != 0:
                    return False
                elif balloonCoord[1]-2 == monsterCoord[1] and\
                 balloonCoord[0] == monsterCoord[0]:
                    return True
    elif numSoda == 2:
        if balloonCoord[0]+1 < 13:
            if balloonCoord[0]+1 == monsterCoord[0] and\
             balloonCoord[1] == monsterCoord[1]:
                return True
            elif balloonCoord[0]+2 < 13:
                if balloonCoord[0]+2 == monsterCoord[0] and\
                 balloonCoord[1] == monsterCoord[1]:
                    return True
            elif balloonCoord[0]+3 < 13:
                if balloonCoord[0]+3 == monsterCoord[0] and\
                 balloonCoord[1] == monsterCoord[1]:
                    return True
        if balloonCoord[0]-1 > -1:
            if balloonCoord[0]-1 == monsterCoord[0] and\
             balloonCoord[1] == monsterCoord[1]:
                return True
            elif balloonCoord[0]-2 > -1:
                if balloonCoord[0]-2 == monsterCoord[0] and\
                 balloonCoord[1] == monsterCoord[1]:
                    return True
            elif balloonCoord[0]-3 > -1:
                if balloonCoord[0]-3 == monsterCoord[0] and\
                 balloonCoord[1] == monsterCoord[1]:
                    return True
        if balloonCoord[1]+1 < 8:
            if balloonCoord[1]+1 == monsterCoord[1] and\
             balloonCoord[0] == monsterCoord[0]:
                return True
            elif balloonCoord[1]+2 < 8:
                if balloonCoord[1]+2 == monsterCoord[1] and\
                 balloonCoord[0] == monsterCoord[0]:
                    return True
            elif balloonCoord[1]+3 < 8:
                if balloonCoord[1]+3 == monsterCoord[1] and\
                 balloonCoord[0] == monsterCoord[0]:
                    return True
        if balloonCoord[1]-1 > -1:
            if balloonCoord[1]-1 == monsterCoord[1] and\
             balloonCoord[0] == monsterCoord[0]:
                return True
            elif balloonCoord[1]-2 > -1:
                if balloonCoord[1]-2 == monsterCoord[1] and\
                 balloonCoord[0] == monsterCoord[0]:
                    return True
            elif balloonCoord[1]-3 > -1:
                if balloonCoord[1]-3 == monsterCoord[1] and\
                 balloonCoord[0] == monsterCoord[0]:
                    return True

#This function gives coordinates of blocks on the map
def getCoordinateBlock(maze,row,col):
    possibleLoc = []
    for i in range(row):
        for j in range(col):
            index = '456789'
            if str(maze[i][j]) in index:
                possibleLoc.append([i,j])
    return possibleLoc

#This function gives coordinates of anywhere else but where the blocks are
def getCoordinateNotBlock(maze, row, col):
    possibleLoc = []
    for i in range(row):
        for j in range(col):
            if maze[i][j] == 0:
                possibleLoc.append([i,j])
    return possibleLoc
    
#This function checks if potential move of characters is legal or not
def movingCharLegal(data):
    col = (data.cx)//90
    row = (data.cy)//85
    if data.cx < 0 or data.cy < 0:
        return False
    if data.cx > 1172 or data.cy > 680:
        return False
    indexBlock = '13456789'
    if str(data.maze[row][col]) in indexBlock:
        return False
    return True

#This function moves the characters in x and y direction
def moveChar(data,col,row):
    data.cx += col
    data.cy += row
    if movingCharLegal(data) == True:
        if col != 0 and col > 0:
            data.character.moveX(col)
        elif col != 0 and col < 0:
            data.character.moveX(col)
        elif row != 0 and row > 0:
            data.character.moveY(row)
        elif row != 0 and row < 0:
            data.character.moveY(row)
    else:
        data.cx -= col
        data.cy -= row
        
#This function was used to see if there is any boxes left in the map
def boxAvailable(maze):
    count = 0
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            if maze[i][j] != 0:
                count += 1
    return count

#This function returns index of the nearest box
def findNearestBox(cy, cx, maze):
    index = '456789'
    if cx+1 < len(maze[0])-1:
        if str(maze[cy][cx+1]) in index:
            return [cy, cx+1]
        if cy+1 < len(maze)-1:
            if str(maze[cy+1][cx+1]) in index:
                return [cy+1, cx+1]
        if cy-1 > 0:
            if str(maze[cy-1][cx+1]) in index:
                return [cy-1, cx+1]
    if cx-1 > 0:
        if str(maze[cy][cx-1]) in index:
            return [cy, cx-1]
        if cy+1 < len(maze)-1:
            if str(maze[cy+1][cx-1]) in index:
                return [cy+1, cx-1]
        if cy-1 > 0:
            if str(maze[cy-1][cx-1]) in index:
                return [cy-1, cx-1]
    if cy+1 < len(maze)-1:
        if str(maze[cy+1][cx]) in index:
            return [cy+1, cx]
        if cx+1 < len(maze[0])-1:
            if str(maze[cy+1][cx+1]) in index:
                return [cy+1, cx+1]
        if cx-1 > 0:
            if str(maze[cy+1][cx-1]) in index:
                return [cy+1, cx-1]
    if cy-1 > 0:
        if str(maze[cy-1][cx]) in index:
            return [cy-1, cx]
        if cx+1 < len(maze[0])-1:
            if str(maze[cy-1][cx+1]) in index:
                return [cy-1, cx+1]
        if cx-1 > 0:
            if str(maze[cy][cx-1]) in index:
                return [cy-1, cx-1]
    return None
    
#AI choose one of the corners to run away from the user
def farFromPlayer(coordX, coordY):
    temp1 = ((coordX - 0)**2 + (coordY - 0)**2)**0.5
    temp2 = ((coordX - 12)**2 + (coordY - 0)**2)**0.5
    temp3 = ((coordX - 0)**2 + (coordY - 7)**2)**0.5
    temp4 = ((coordX - 12)**2 + (coordY - 7)**2)**0.5
    lst = [temp1, temp2, temp3, temp4]
    if min(lst) == temp1: return [0,0]
    if min(lst) == temp2: return [12,0]
    if min(lst) == temp3: return [0,7]
    if min(lst) == temp4: return [12,7]
    
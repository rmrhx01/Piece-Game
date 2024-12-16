from typing import List, Tuple, Optional
import pygame
FONTTOUSE = pygame.font.Font(pygame.font.get_default_font(), 15)
class Board:
    def __init__(self, X: int, Y: int, board: Optional[List[List[str]]] = None, startX = 50, startY = 50, block_size=20):
        self.X = X
        self.Y = Y
        if board is None:
            self._board = [[0 for _ in range(Y)] for _ in range(X)]  # Create a new list for each row
        else:
            self._board = [[board[y][x] for y in range(Y)] for x in range(X)]
        self.zeroes = 0
        self.rects = []
        self.block_size = block_size
        self.startX = startX
        self.startY = startY
        for i in range(self.X):
            for j in range(self.Y):
                self.rects.append(pygame.Rect(startX + i*block_size, startY + j*block_size, self.block_size, self.block_size))
                if self._board[i][j] == 0:
                    self.zeroes +=1

    def importBoardFromArray(self,board:List[List[str]]):
        self._board = [[board[x][y] for y in range(self.Y)] for x in range(self.X)]

    #Finds next available spot
    def findEmpties(self):
        temp = []
        for i in range(self.X):
            for j in range(self.Y):
                if self._board[i][j] == 0:
                    temp.append((i,j))   
        return temp
        
    #Check if a rotation fits inside the board
    def checkBounds(self,piece:List[Tuple[int,int]],x:int,y:int)->bool:
        for i,j in piece:
            if i+x >= self.X or j+y >= self.Y or i+x < 0 or j+y<0:
                #Out of bounds
                return False
        return True
    
    #Check if the current pieces are not using the spaces to use
    def checkOccupied(self,piece:List[Tuple[int,int]],x:int = 0,y:int = 0)->bool:
        for i,j in piece:
            if self._board[i+x][j+y] != 0:
                return False
        return True

    #Places the rotation while doing necessary checks
    def placeRotation(self, piece:List[Tuple[int,int]],color:str,x:int,y:int) -> bool:
        if not self.checkBounds(piece,x,y):
            return False
        if not self.checkOccupied(piece,x,y):
            return False
        for i,j in piece:
            self._board[i+x][j+y] = color
            self.zeroes -= 1
        return True
    
    def placePosition(self,piece:List[Tuple[int,int]],color:str):
        if not self.checkOccupied(piece):
            return False
        for i,j in piece:
            self._board[i][j] = color
            self.zeroes -= 1
        return True

    def undoRotation(self,piece:List[Tuple[int,int]],x:int = 0,y:int = 0):
        for i,j in piece:
            self._board[i+x][j+y] = 0
            self.zeroes += 1
        
    def solved(self):
        return self.zeroes == 0
    
    def printBoard(self):
        for j in range(self.Y):
            for i in range(self.X):
                print(self._board[i][j],end=' ')
            print()

    def deletePiece(self, tag:str):
        for i in range(self.X):
            for j in range(self.Y):
                if self._board[i][j] == tag:
                    self._board[i][j] = 0

    def draw(self, surface: pygame.Surface):
        for rect in self.rects:
            #Could add a variable for color
            pygame.draw.rect(surface,(255,255,255) ,rect)
            
            pygame.draw.rect(surface, (0, 0, 0), rect, width=1)    

class Piece: 
    #Dictionary to access the colors by tag
    color = {'A':(235, 140, 52),
             'B':(201, 38, 20),
             'C':(13, 42, 189),
             'D':(237, 213, 213),
             'E':(13, 143, 30),
             'F':(255, 255, 255),
             'G':(110, 217, 250),
             'H':(237, 147, 224),
             'I':(237, 227, 40),
             'J':(135, 50, 219),
             'K':(73, 245, 102),
             'L':(140, 140, 140),}

    def __init__(self,tag,block_size=20,initial_position=(0,0)):
        self.tag = tag
        self.parts = []
        self.rotations = []
        self.positions=[]
        self.size = 0
        self.x, self.y = initial_position
        self.block_size = block_size
        self.dragging = False
        self.rects = []
        self.text = FONTTOUSE.render(tag, True, (0, 0, 0))
        self.positionInBoard = None
        self.onBoard = False

    #Add part in relation to 0,0
    def addPart(self,x,y):
        self.parts.append((x,y))
        self.size += 1
        rect_x = self.x + x * self.block_size
        rect_y = self.y + y * self.block_size
        rect = pygame.Rect(rect_x, rect_y, self.block_size, self.block_size)
        self.rects.append(rect)
    
    def addParts(self,array:List[Tuple[int,int]]):
        for i in array:
            self.parts.append(i)
            self.size += 1
            rect_x = self.x + i[0] * self.block_size
            rect_y = self.y + i[1] * self.block_size
            rect = pygame.Rect(rect_x, rect_y, self.block_size, self.block_size)
            self.rects.append(rect)

    def rotateUP(self):
        for index, (x, y) in enumerate(self.parts):
            self.parts[index] = (x*-1,y)

    def rotateRIGHT(self):
        for index, (x, y) in enumerate(self.parts):
            self.parts[index] = (y*-1,x)

    def rotateDOWN(self):
        for index, (x, y) in enumerate(self.parts):
            self.parts[index] = (x*-1,y)

    def rotateLEFT(self):
        for index, (x, y) in enumerate(self.parts):
            self.parts[index] = (y,x*-1)

    def removeDuplicates(self):
        for index, rotation in enumerate(self.rotations):
            min_first = min(block[0] for block in rotation)
            min_second = min(block[1] for block in rotation)
            self.rotations[index] = [(x-min_first,y-min_second) for x,y in rotation]
        
        self.rotations = [tuple(sorted(rotation)) for rotation in self.rotations]
        self.rotations = list(set(self.rotations))
        self.rotations = [list(rotation) for rotation in self.rotations]
        self.rotations = [[(x-rotation[0][0],y-rotation[0][1]) for x,y in rotation] for rotation in self.rotations]

    def generateRotations(self):
        self.rotations = [[i for i in self.parts]]
        for _ in range(3):
            self.rotateRIGHT()
            self.rotations.append([i for i in self.parts])

        self.rotateUP()
        self.rotations.append([i for i in self.parts])
        for _ in range(3):
            self.rotateRIGHT()
            self.rotations.append([i for i in self.parts])
        self.removeDuplicates()
    
    def printPiece(self):
        for rotation in self.rotations:
            tempMatrix = [[0 for _ in range(4)] for _ in range(4)]
            
            minX = min(x[0] for x in rotation)
            minY = min(x[1] for x in rotation)
            for x,y in rotation:
                tempMatrix[x-minX][y-minY] = self.tag
            for i in range(4):
                for j in range(4):
                    print(tempMatrix[i][j],' ',end='')
                print()
            print()
    
    def generatePositions(self,board:Board):
        for x,y in board.findEmpties():
            for rotation in self.rotations:
                if board.checkBounds(rotation,x,y) and board.checkOccupied(rotation,x,y):
                    self.positions.append([(i+x,j+y) for i,j in rotation])

    def draw(self, surface: pygame.Surface): 
        for part_x, part_y in self.parts:
            rect_x = self.x + part_x * self.block_size
            rect_y = self.y + part_y * self.block_size
            offset = self.block_size/3
            rect = pygame.Rect(rect_x, rect_y, self.block_size, self.block_size)
        
            pygame.draw.rect(surface, Piece.color[self.tag],rect)
            pygame.draw.rect(surface, (0, 0, 0), rect, width=1)
            surface.blit(self.text,(rect_x+offset,rect_y+offset))

    def is_clicked(self, mouse_pos):
        for part_x, part_y in self.parts:
            rect_x = self.x + part_x * self.block_size
            rect_y = self.y + part_y * self.block_size
            rect = pygame.Rect(rect_x, rect_y, self.block_size, self.block_size)
            if rect.collidepoint(mouse_pos):
                return True
        return False
    
    def start_drag(self, mouse_pos):
        if self.is_clicked(mouse_pos):
            self.dragging = True
            #self.offset_x = self.x - mouse_pos[0]
            #self.offset_y = self.y - mouse_pos[1]
            self.offset_x = -1*self.block_size/2
            self.offset_y = -1*self.block_size/2

    def stop_drag(self):
        self.dragging = False

    def drag(self, mouse_pos):
        if self.dragging:
            self.x = mouse_pos[0] + self.offset_x
            self.y = mouse_pos[1] + self.offset_y

    def getClosestRect(self, board:Board) -> Tuple[int,int,pygame.Rect]:
        closestDist = 100000
        closestRect = None
        offset = self.block_size/2
        indexX = -1
        indexY = -1
        for index,rect in enumerate(board.rects):
            distance = ((self.x + offset - rect.center[0])**2 + (self.y + offset - rect.center[1])**2)**(1/2)
            if distance < closestDist:
                closestDist = distance
                closestRect = rect
                indexX = index//board.Y 
                indexY = index%board.Y
        return (indexX,indexY,closestRect)

    def findPosition(self,board:Board)->None:
        self.parts = []
        self.rects = []
        self.size = 0
        x = -1
        y = -1
        for i in range(board.X):
            for j in range(board.Y):
                if board._board[i][j] == self.tag:
                    if x == -1:
                        x = i
                        y = j
                        self.x = i * board.block_size + board.startX
                        self.y = j * board.block_size + board.startY
                    self.addPart(i-x,j-y)
        
    def __eq__(self,other):
        return self.size == other.size
    
    def __lt__(self,other):
        return self.size < other.size

    def __le__(self,other):
        return self.size <= other.size

    def __str__(self):
        return str((self.x,self.y))
    
    def __repr__(self):
        return self.tag

class Button:
    def __init__(self, x, y, h, w, text, color1, color2):
        self.x = x
        self.y = y
        self.h = h
        self.w = w
        self.color1 = color1
        self.color2 = color2
        self.text = FONTTOUSE.render(text, True, (0, 0, 0))
        self.rect = pygame.Rect(x,y,w,h)
        self.active = False
        self.name = text

    def draw(self, surface:pygame.Surface):
        offset_x = self.w/3
        offset_y = self.h/3
        if self.active:
            pygame.draw.rect(surface,self.color2,self.rect)
            pygame.draw.rect(surface,self.color1, self.rect, width=1)
        else: 
            pygame.draw.rect(surface,self.color1,self.rect)
            pygame.draw.rect(surface,self.color2, self.rect, width=1)
        
        surface.blit(self.text,(self.x+offset_x,self.y+offset_y))

def sortPieces(pieces:dict[Piece])->dict[Piece]:

    values = list(pieces.values())
    values.sort(reverse=True,key= lambda piece: (piece.size,len(piece.rotations)))

    # Sorted Dictionary
    newDict = {i.tag: pieces[i.tag] for i in values}
    return newDict

def solve(board:Board,pieces:List[Piece]):
    #check if solved
    if board.solved() == True:
        return board

    if pieces == []:
        return None

    currentPiece = pieces[0]
    
    for position in currentPiece.positions:
        if board.placePosition(position,currentPiece.tag) == True:
            currentPiece.positionInBoard = position[0]
            solution = solve(board,pieces[1:]) 
            if solution != None:
                return solution
            else:
                board.undoRotation(position)
    return None

import pygame
pygame.init()
from Game import *


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BLOCK_SIZE = 40

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Jueguito")


def declarePieces():
    A = Piece('A',initial_position=(69, 355),block_size=BLOCK_SIZE)
    parts = [(0,0),(1,0),(1,1),(1,2)]
    A.addParts(parts)
    A.generateRotations()


    B = Piece('B',initial_position=(203, 356),block_size=BLOCK_SIZE)
    parts = [(0,0),(1,0),(2,0),(0,1),(1,1)]
    B.addParts(parts)
    B.generateRotations()


    C = Piece('C',initial_position=(375, 354),block_size=BLOCK_SIZE)
    parts = [(0,0),(0,1),(1,0),(2,0),(3,0)]
    C.addParts(parts)
    C.generateRotations()

    D = Piece('D',initial_position=(556, 351),block_size=BLOCK_SIZE)
    parts = [(0,0),(1,0),(2,0),(3,0),(1,1)]
    D.addParts(parts)
    D.generateRotations()


    E = Piece('E',initial_position=(719, 359),block_size=BLOCK_SIZE)
    parts = [(0,0),(1,0),(1,1),(2,1),(3,1)]
    E.addParts(parts)
    E.generateRotations()


    F = Piece('F',initial_position=(58, 497),block_size=BLOCK_SIZE)
    parts = [(0,0),(0,1),(1,1)]
    F.addParts(parts)
    F.generateRotations()


    G = Piece('G',initial_position=(193, 546),block_size=BLOCK_SIZE)
    parts = [(0,0),(1,0),(2,0),(0,-1),(0,-2)]
    G.addParts(parts)
    G.generateRotations()

    H = Piece('H',initial_position=(330, 470),block_size=BLOCK_SIZE)
    parts = [(0,0),(0,1),(1,1),(1,2),(2,2)]
    H.addParts(parts)
    H.generateRotations()


    I = Piece('I',initial_position=(426, 502),block_size=BLOCK_SIZE)
    parts = [(0,0),(1,0),(-1,0),(1,1),(-1,1)]
    I.addParts(parts)
    I.generateRotations()

    J = Piece('J',initial_position=(547, 450),block_size=BLOCK_SIZE)
    parts = [(0,0),(1,0),(2,0),(3,0)]
    J.addParts(parts)
    J.generateRotations()

    K = Piece('K',initial_position=(572, 506),block_size=BLOCK_SIZE)
    parts = [(0,0),(1,0),(0,1),(1,1)]
    K.addParts(parts)
    K.generateRotations()

    L = Piece('L',initial_position=(679, 501),block_size=BLOCK_SIZE)
    parts = [(0,0),(1,0),(-1,0),(0,-1),(0,1)]
    L.addParts(parts)
    L.generateRotations()

    pieces = [A,B,C,D,E,F,G,H,I,J,K,L]
    return pieces


pieces = declarePieces()

board = Board(11,5,startX=SCREEN_WIDTH/2-5.5*BLOCK_SIZE,block_size=BLOCK_SIZE)

buttons = [
    Button(24,53,BLOCK_SIZE,3*BLOCK_SIZE,"New",(135, 131, 131),(196, 192, 192)),
    Button(24,125,BLOCK_SIZE,3*BLOCK_SIZE,"Solve",(135, 131, 131),(196, 192, 192))
]

active_piece = None
active_button = None
running = True
piecesToPlace = {piece.tag:piece for piece in pieces}
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if active_piece:
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    active_piece.rotateRIGHT()
                elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    active_piece.rotateLEFT()
                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    active_piece.rotateUP()
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    active_piece.rotateDOWN()
            if event.key == pygame.K_b:
                print("-------------------------------------------------")
                board.printBoard()
                print("-------------------------------------------------")    

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                for piece in pieces:
                    if piece.is_clicked(event.pos):
                        active_piece = piece
                        piece.start_drag(event.pos)
                        if active_piece.onBoard:
                            board.deletePiece(active_piece.tag)
                            piecesToPlace[active_piece.tag] = active_piece
                        active_piece.onBoard = False

                        break
                for button in buttons:
                    if button.rect.collidepoint(event.pos):
                        button.active = True
                        active_button = button
                        if button.name == 'Solve':
                            for piece in piecesToPlace.values():
                                piece.generatePositions(board)
                            piecesToPlace = sortPieces(piecesToPlace)
                            board = solve(board,[piece for piece in piecesToPlace.values()])
                            for piece in piecesToPlace.values():
                                piece.onBoard = True
                                piece.findPosition(board)
                        elif button.name == 'New':
                            pieces = declarePieces()
                            board = Board(11,5,startX=SCREEN_WIDTH/2-5.5*BLOCK_SIZE,block_size=BLOCK_SIZE)
                            piecesToPlace = {piece.tag:piece for piece in pieces}
                        elif button.name == 'Debug':
                            """
                            if index == -1:
                                for piece in piecesToPlace.values():
                                    piece.generatePositions(board)
                                piecesToPlace = sortPieces(piecesToPlace)
                                index = 0
                                board.placePosition(debug_piece.positions[index],debug_piece.tag)
                                piece.onBoard = True
                                debug_piece.findPosition(board)
                            else:
                                board.undoRotation(debug_piece.positions[index])
                                index += 1
                                board.placePosition(debug_piece.positions[index],debug_piece.tag)
                                debug_piece.findPosition(board)
                            """
                        break
                        
                

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # Left mouse button
                if active_piece:
                    active_piece.stop_drag()
                    x,y,closest = active_piece.getClosestRect(board) 
                    if closest.collidepoint((active_piece.x + active_piece.block_size/2, active_piece.y + active_piece.block_size/2)): 
                        if board.placeRotation(active_piece.parts,active_piece.tag,x,y):
                            active_piece.x = closest.x
                            active_piece.y = closest.y
                            active_piece.onBoard = True
                            del piecesToPlace[active_piece.tag]
                    active_piece = None
                elif active_button:
                    active_button.active = False

        elif event.type == pygame.MOUSEMOTION:
            if active_piece:
                active_piece.drag(event.pos)

    # Clear the screen
    screen.fill((0, 0, 0))

    board.draw(screen)

    # Draw all pieces
    for piece in pieces:
        piece.draw(screen)

    for button in buttons:
        button.draw(screen)

    

    # Update the display
    pygame.display.flip()

pygame.quit()
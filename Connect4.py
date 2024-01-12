import numpy as np
import pygame as py
import sys

from pygame import font

row_count = 6
column_count = 7
blue = (0, 0, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
white = (255, 255, 255)


def create_board():
    game_board = np.zeros((row_count, column_count))
    return game_board


# check if the column player choose is valid to drop piece
def valid_col_drop(board, col):
    return board[0][col] == 0  # check if the first row is 0, check start from top-left corner


# get next valid row in player choose column
def valid_row_drop(board, col):
    for r in reversed(range(row_count)):  # from bottom to top
        if board[r][col] == 0:
            return r

# drop the piece to player choose position
def drop_piece(board, row, col, piece):
    board[row][col] = piece

def is_win_drop(board, col, row, piece):
    count = 0
    # check horizontal
    for c in range(column_count):
        if board[row][c] == piece:
            count += 1
            if count == 4:
                return True
        else:
            count = 0
    # check vertical
    for r in range (row_count):
        if board[r][col] == piece:
            count += 1
            if count == 4:
                return True
        else:
            count = 0
    # check diagonal negative
    for i in range(-3, 4):
        if 0<= row + i < row_count and 0 <= col + i < column_count and board[row + i][col + i] == piece:
            count += 1
            if count == 4:
                return True
        else:
            count = 0
    # check diagonal postive
    for i in range(-3, 4):
        if 0<= row - i < row_count and 0 <= col + i < column_count and board[row - i][col + i] == piece:
            count += 1
            if count == 4:
                return True
        else:
            count = 0
    return False

def draw_piece(row, col, color):
    py.draw.circle(screen, color, (col, row), 45)

def draw_board(board):
    for r in range(row_count):
        for c in range(column_count):
            row = r*100 + 150
            col = c*100 + 50
            py.draw.rect(screen, blue, (c * 100, r * 100 + 100, 100, 100))
            draw_piece(row, col, black)
            if board[r][c] == 1:
                draw_piece(row, col, red)
            elif board[r][c] == 2:
                draw_piece(row, col, green)
    py.display.update()

def draw_text(text, x, y, color):

    text_surface = myfont.render(text, True, color)
    screen.blit(text_surface, (x, y))

def draw_winner_board(winner):
    for r in range(row_count):
        for c in range(column_count):
            py.draw.rect(screen, black, (c * 100, r * 100 + 100, 100, 100))
    py.draw.rect(screen, black, (0, 0, column_count * 100, 100))
    #draw_text("Game Over", 220, 260, white)
    # py.draw.rect(screen, white, (151, 361, 150, 50), 1)
    # py.draw.rect(screen, white, (457, 361, 150, 50), 1)
    draw_text("Retry", 170, 370, white)
    draw_text("Quit", 480, 370, white)
    draw_text(winner, 200, 260, white)
    py.display.update()


board = create_board()
print(board)
game_over = False
turn = 0

py.init()
screen = py.display.set_mode((column_count * 100, (row_count + 1) * 100))
py.display.set_caption("Connect Four")
myfont = py.font.SysFont(None, 40)
draw_board(board)
py.display.update()
has_winner = False

while not game_over:
    for event in py.event.get():
        if event.type == py.QUIT:
            sys.exit()

        if event.type == py.MOUSEMOTION:
            if turn == 0 and not has_winner:
                py.draw.rect(screen, black, (0, 0, column_count * 100, 100))
                posx = event.pos[0]
                draw_piece(50, posx, red)
            elif turn == 1 and not has_winner:
                py.draw.rect(screen, black, (0, 0, column_count * 100, 100))
                posx = event.pos[0]
                draw_piece(50, posx, green)
            py.display.update()

        if event.type == py.MOUSEBUTTONDOWN:
            if turn == 0:
                posx = event.pos[0]  # get the x of mouse click position
                posy = event.pos[1]
                col = posx // 100
                if valid_col_drop(board, col) and not has_winner:
                    row = valid_row_drop(board, col)
                    drop_piece(board, row, col, 1)
                    draw_board(board)
                    if is_win_drop(board,col, row, 1):
                        has_winner = True
                        draw_winner_board("Player 1 is the winner !")


            else:
                posx = event.pos[0]  # get the x of mouse click position
                posy = event.pos[1]
                col = posx // 100
                if valid_col_drop(board, col) and not has_winner:
                    row = valid_row_drop(board, col)
                    drop_piece(board, row, col, 2)
                    draw_board(board)
                    if is_win_drop(board,col, row, 2):
                        has_winner = True
                        draw_winner_board("Player 2 is the winner !")
                        #game_over = True
            print(board)
            # draw_board(board)
            turn += 1
            turn = turn % 2

        if event.type == py.MOUSEBUTTONDOWN and has_winner:
            posx = event.pos[0]  # get the x of mouse click position
            posy = event.pos[1]
            if 151 < posx < 299 and 361 < posy < 409:
                board = create_board()
                draw_board(board)
                has_winner = False
            elif 457 < posx < 594 and 361 < posy < 409:
                game_over = True



# import the necessary modules for the program: pygame, engine, and Ai.
import pygame
import engine
import Ai
'''
define constants for the dimensions(ابعاد) of the game board,
the number of squares in each axis, 
the size of each square,
and an empty dictionary to store images of chess pieces.
'''

# interface configs
WIDTH, HEIGHT = 512, 512   # Board dimensions
SQUARES_NUMBER = 8   # Number of squares in each axis
SQUARE_SIZE = 512 / 8  # the size of each square
IMAGES = {}     # dictionary to store images of chess pieces.

'''
This function loads images of chess pieces into the IMAGES dictionary.
 It uses the pygame.image.
 load function to load each image and pygame.transform.scale to resize them to the specified square size.
'cheSs/bB.png'
'cheSs/wK.png'
 '''
# loads pieces images into the memory
def get_images():
    pieces = ['bB', 'bK', 'bN', 'bp', 'bQ', 'bR', 'wB', 'wK', 'wN', 'wp', 'wQ', 'wR']
    for piece in pieces:
        IMAGES[piece] = pygame.transform.scale(pygame.image.load('cheSs/' + piece + '.png'), (SQUARE_SIZE, SQUARE_SIZE))

'''
This function draws the chessboard by filling the background with alternating colors for each square. 
The color of a square depends on its position,
and it is determined by the color1 and color2 variables.
'''
def draw_board(background):
    color1 = pygame.Color((177, 179, 178))
    color2 = pygame.Color((0, 163, 152))
    # 1.This loop colors each square(which it's side is defined by SQUARE_SIZE) according to the board numbering
    # 2.The color of a square depends on it's numbering on the board
    # 3.If a square's row number + column number is even then it's color is light else it's dark
    for row in range(SQUARES_NUMBER):
        for column in range(SQUARES_NUMBER):
            if ((row + column) % 2) == 0:
                color = color2
            else:
                color = color1
            pygame.draw.rect(background, color, pygame.Rect(row*SQUARE_SIZE, column*SQUARE_SIZE, SQUARE_SIZE,
                                                            SQUARE_SIZE))


# Drawing pieces by looping throw the board state we have and checking the board attribute in the engine
# We define the piece in the current position via it's row and column in the state space array in the engine module
def draw_pieces(screen, board_state):
    for row in range(SQUARES_NUMBER):
        for column in range(SQUARES_NUMBER):
            piece = board_state[row][column]  # Assigning the string representation of a piece to variable 'piece'
            if piece != '  ':   # Checking if 'piece' variable got an unoccupied square(two white spaces in the array)
                screen.blit(IMAGES[piece], (column*SQUARE_SIZE, row*SQUARE_SIZE))  # Drawing 'piece' if it's valid


def draw_current_state():
    draw_board(screen)
    draw_pieces(screen, game_state.board)

'''
    These condition initialize the game by setting up the Pygame window,
    filling the screen with a white color,
    creating a game state object,
    and setting various flags and variables to manage the game loop.
'''
if __name__ == '__main__':
    pygame.init() #These condition initialize the game by setting up the Pygame window,
    screen = pygame.display.set_mode((WIDTH, HEIGHT)) #filling the screen with a white color,
    screen.fill((0, 0, 0))
    game_state = engine.GameState() #creating a game state object,
    valid_moves = game_state.get_valid_moves()
    get_images()
    running = True  # Flag variable for running the game
    move_made = False  # Flag variable for checking weather a move is made or not
    square_highlighted = ()  # Stores highlighted squares
    current_move = []  # Stores the current move via highlighted squares(stores two tuples)
    white_human = True
    black_human = False
    undoing = False
    '''
    The while running: loop contains the main game loop where user input is processed,
      the game state is updated, and the screen is redrawn.
    '''
    while running:
        human_turn = (game_state.white_turn and white_human) or (not game_state.white_turn and black_human)
        game_over = game_state.is_check_mate() or game_state.is_stale_mate()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if human_turn and not game_over:  #This condition checks if it's the human player's turn and the game is not over.
                    position = pygame.mouse.get_pos()  # Getting the position of a clicked square on the screen
                    column = int(position[0] // SQUARE_SIZE) #: Calculates the column index of the clicked square based on the mouse x-coordinate and the size of each square.
                    row = int(position[1] // SQUARE_SIZE) # Calculates the row index of the clicked square based on the mouse y-coordinate and the size of each square.
                    if square_highlighted == (row, column):  # Preventing the engine from moving a piece in it's place
                                                             # (Checks if the clicked square is the same as the one already highlighted.) 
                        # If true, it unhighlights the square and clears the current move.
                        square_highlighted = ()
                        current_move = []
                    else: # If the clicked square is different from the highlighted square,
                        square_highlighted = (row, column) #it updates the highlighted square,
                        current_move.append(square_highlighted) #appends the new position to the current move,
                        print(row, column) # prints the row and column for debugging purposes.
                    if len(current_move) == 2: # Checks if two squares have been highlighted, representing a complete move.
                        #Creates a Move object using the positions of the two highlighted squares.
                        move = engine.Move(current_move[0], current_move[1], game_state.board)
                        if move in valid_moves: #Checks if the generated move is a valid move.
                            game_state.make_move(move) # If the move is valid, it applies the move to the game state.
                            move_made = True #Flags that a move has been made.
                            undoing = False #Flags that the game is not in the process of undoing a move.
                            square_highlighted = () # Clears the highlighted squares.
                            current_move = [] #Clears the current move list.
                        else: # If the generated move is not valid, it resets the current move to the first square clicked.
                            current_move = [square_highlighted]
            # This part of the code when a key is pressed, specifically when the KEYDOWN event occurs. It checks if the pressed key is the backspace key (pygame.K_BACKSPACE).
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:  # Undoing a move
                    game_state.undo() # Calls the undo method of the game_state object, which presumably undoes the last move made in the game.
                    undoing = True # Flags that the game is in the process of undoing a move.
                    move_made = True # Flags that a move has been made. This may seem counterintuitive, but it's likely used to trigger the updating of valid moves after undoing.
                    game_over = False #  Flags that the game is not over. This is probably used to continue the game after undoing a move.
        #if it's not the human player's turn (not human_turn), the game is not over (not game_over), and the game is not in the process of undoing a move (not undoing). In this case, it simulates the AI's move:
        if not human_turn and not game_over and not undoing: 
            Ai_move = Ai.find_best_move(game_state, valid_moves) # Calls a function (find_best_move) from the Ai module to determine the best move for the AI given the current game state and valid moves.
            if Ai_move is None: # If the best move is not available,
                Ai_move = Ai.find_random_move(valid_moves) # the AI falls back to making a random move by calling 'find_random_move' from the Ai module.

            game_state.make_move(Ai_move) # Applies the AI's move to the game state.
            move_made = True # Flags that a move has been made.
        if move_made: # If a move has been made,
            valid_moves = game_state.get_valid_moves() # it updates the valid moves by calling game_state.get_valid_moves() 
            move_made = False
        #Draws the updated state of the game on the screen and updates the display. 
        #This is part of the main game loop that continuously runs while the game is running.
        draw_current_state()
        pygame.display.flip()
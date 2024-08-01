import random
CHECKMATE = 1000 # Represents a score assigned to a state where the game is in checkmate. This is a high positive value, indicating a winning position for the player.
'''
عمق البحث" بيحدد عدد الخطوات اللي قدام الذكاء الاصطناعي بتشوفهم لما بتختار أحسن حركة ممكنة.
يعني لو عمق البحث هو 3، هتتأمل كل الاحتمالات اللي ممكن تحصل بعد 3 خطوات من كل حركة ممكنة، وبعدين هتختار الحركة اللي بتوصلها لنتيجة أحسن ليها على المدى البعيد.
'''
initial_depth = 3 # Specifies the initial depth for the minimax search. This determines how many moves ahead the AI looks when evaluating potential moves.
strength = {'Q': 10, 'R': 5, 'N': 3, 'B': 3, 'p': 1, 'K': 0}
# Any 'We, our or us' refers to the Ai

# Random Move Function:
def find_random_move(valid_moves): # is a function that takes a list of valid moves (valid_moves) and returns a randomly selected move from that list. It uses random.randint to generate a random index within the range of valid moves.
    return valid_moves[random.randint(0, len(valid_moves)-1)]

# Best Move Function:
def find_best_move(state, valid_moves):
    global next_move, counter  # The final move to be made by us
    # It initializes global variables next_move and counter.
    next_move = None 
    counter = 0
    
    #Calls the searching_moves function, passing the current state (state), valid moves, initial depth, and alpha-beta pruning bounds.
    searching_moves(state, valid_moves, initial_depth, -CHECKMATE, CHECKMATE, -1)  # Starting the search
    
    print(counter) # Prints the value of the counter variable, which counts the number of positions evaluated during the search.
    return next_move # Returns the move stored

# "def searching_moves" is a recursive function that implements the minimax algorithm with alpha-beta pruning.
# It evaluates the current position by recursively evaluating possible moves up to a certain depth (depth parameter).
# alpha and beta are used for alpha-beta pruning, and multiplier is used to determine whether it's the maximizing or minimizing player's turn.

# This function is a part of the minimax algorithm with alpha-beta pruning. It evaluates possible moves and returns the maximum score for the current state.
def searching_moves(state, valid_moves, depth, alpha, beta, multiplier):
    
    global next_move, counter # Indicates that next_move and counter are global variables,
    
    if depth == 0:  # If we got to the deepest depth  we are allowed to search
        # Returns the score of the current board state multiplied by the multiplier. This is a recursive evaluation of the board score using the get_board_score function.
        return multiplier * get_board_score(state)  # Start backtracking
    
    ## Initializes max_score to a very low value, representing the worst possible score for the maximizing player.
    max_score = -CHECKMATE  # If it's we initialize there max score as the lowest and they shall max it to win
    
    for move in valid_moves:  # We check every valid move we got for them
        
        ## Applies the current move to the game state.
        state.make_move(move)  # We make the move and check the score after using it
        
        ## Retrieves the valid moves for the next state after making the current move.
        next_moves = state.get_valid_moves()  # We get the children of the state after playing this game
        
        #Recursively calls "searching_moves" with the updated state and decreased depth. The negative sign is used to switch the players (maximizing to minimizing or vice versa(او العكس)).
        score1 = -searching_moves(state, next_moves, depth - 1, -beta, -alpha, -multiplier)
        
        if score1 > max_score: # Checks if the score obtained from the recursive call is greater than the current max_score.
            max_score = score1 # Updates max_score with the new maximum score.
            
            if depth == initial_depth: # : If the current depth is equal to the initial depth,  
                next_move = move # updates the next_move with the current move.
                #This is used to track the best move at the root level.
        
        state.undo() #  Undoes (التراجع) the move to revert to the previous state.
        counter += 1 #  Increments the counter variable, which is used to count the number of positions evaluated during the search.
        
        # Updates the alpha value if the current max_score is greater.
        if max_score > alpha:
            alpha = max_score
        
        # Breaks out of the loop if alpha is greater than or equal to beta, indicating that further exploration is unnecessary.
        if alpha >= beta:
            break
    return max_score


def get_board_score(state):  # Getting the score of each square on the bord
    if state.is_check_mate():
        if state.white_turn:
            return -CHECKMATE  # black wins
        else:
            return CHECKMATE  # white wins
    elif state.is_stale_mate():
        return 0
    score = 0
    for row in state.board:
        for piece in row:
            if piece[0] == 'w':
                score += strength[piece[1]]
            elif piece[0] == 'b':
                score -= strength[piece[1]] 
    return score

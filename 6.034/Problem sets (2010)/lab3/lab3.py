# 6.034 Fall 2010 Lab 3: Games
# Name: Ignacio Paricio
# Email: --

from util import INFINITY

### 1. Multiple choice

# 1.1. Two computerized players are playing a game. Player MM does minimax
#      search to depth 6 to decide on a move. Player AB does alpha-beta
#      search to depth 6.
#      The game is played without a time limit. Which player will play better?
#
#      1. MM will play better than AB.
#      2. AB will play better than MM.
#      3. They will play with the same level of skill.
ANSWER1 = 3

# 1.2. Two computerized players are playing a game with a time limit. Player MM
# does minimax search with iterative deepening, and player AB does alpha-beta
# search with iterative deepening. Each one returns a result after it has used
# 1/3 of its remaining time. Which player will play better?
#
#   1. MM will play better than AB.
#   2. AB will play better than MM.
#   3. They will play with the same level of skill.
ANSWER2 = 2

### 2. Connect Four
from connectfour import *
from basicplayer import *
from util import *
import tree_searcher

## This section will contain occasional lines that you can uncomment to play
## the game interactively. Be sure to re-comment them when you're done with
## them.  Please don't turn in a problem set that sits there asking the
## grader-bot to play a game!
## 
## Uncomment this line to play a game as white:
#run_game(human_player, basic_player)

## Uncomment this line to play a game as black:
#run_game(basic_player, human_player)

## Or watch the computer play against itself:
#run_game(basic_player, basic_player)

## Change this evaluation function so that it tries to win as soon as possible,
## or lose as late as possible, when it decides that one side is certain to win.
## You don't have to change how it evaluates non-winning positions.

def focused_evaluate(board):
    """
    Given a board, return a numeric rating of how good
    that board is for the current player.
    A return value >= 1000 means that the current player has won;
    a return value <= -1000 means that the current player has lost
    """    
    score = 0
    if board.is_game_over():
    # If the game has been won, we know that it must have been
    # won or ended by the previous move.
    # The previous move was made by our opponent.
    # Therefore, we can't have won, so return -1000.
    # (note that this causes a tie to be treated like a loss)
        # Use -1000 as a starting point, but still compute your best options
        score = -1000
    
    # If we can win the game, do so
    if board.longest_chain(board.get_current_player_id()) == 4:
        score = 1001
        return score
        
    score += board.longest_chain(board.get_current_player_id()) * 10
    # Prefer having your pieces in the center of the board.
    for row in range(6):
        for col in range(7):
            if board.get_cell(row, col) == board.get_current_player_id():
                score -= abs(3-col)
            elif board.get_cell(row, col) == board.get_other_player_id():
                score += abs(3-col)

    return score


## Create a "player" function that uses the focused_evaluate function
quick_to_win_player = lambda board: minimax(board, depth=4, eval_fn=focused_evaluate)

## You can try out your new evaluation function by uncommenting this line:
#run_game(basic_player, quick_to_win_player)
#run_game(human_player, quick_to_win_player)

## Write an alpha-beta-search procedure that acts like the minimax-search
## procedure, but uses alpha-beta pruning to avoid searching bad ideas
## that can't improve the result. The tester will check your pruning by
## counting the number of static evaluations you make.
##
## You can use minimax() in basicplayer.py as an example.

def alpha_beta_search_board_value(board, depth,
                      eval_fn, alpha, beta,
                      get_next_moves_fn=get_all_next_moves,
                      is_terminal_fn=is_terminal):
         
    # Base case: evaluate static node    
    if is_terminal_fn(depth, board):
        return eval_fn(board)
        
    # Recursive case: keep exploring 
    for move, new_board in get_next_moves_fn(board):
        if alpha >= beta:
            break
        val = -1 * alpha_beta_search_board_value(new_board, depth - 1, eval_fn,
                                                 -beta, -alpha,
                                                 get_next_moves_fn, is_terminal_fn)
        if val > alpha:
            alpha = val

    return alpha


def alpha_beta_search(board, depth,
                      eval_fn,
                      # NOTE: You should use get_next_moves_fn when generating
                      # next board configurations, and is_terminal_fn when
                      # checking game termination.
                      # The default functions set here will work
                      # for connect_four.
                      get_next_moves_fn=get_all_next_moves,
                      is_terminal_fn=is_terminal):
    # Define best_val; best_val[0] = score of move; best_val[1] = move
    best_val = [None, None] 
    
    alpha = NEG_INFINITY
    beta = INFINITY
    
    for move, new_board in get_next_moves_fn(board):
        val = -1 * alpha_beta_search_board_value(new_board, depth - 1, eval_fn,
                                                 alpha, beta,
                                                 get_next_moves_fn,
                                                 is_terminal_fn)
        if best_val[0] == None or val > best_val[0]:
            best_val = (val, move)

    return best_val[1]

## Now you should be able to search twice as deep in the same amount of time.
## (Of course, this alpha-beta-player won't work until you've defined
## alpha-beta-search.)
alphabeta_player = lambda board: alpha_beta_search(board,
                                                   depth=8,
                                                   eval_fn=focused_evaluate)

## This player uses progressive deepening, so it can kick your ass while
## making efficient use of time:
ab_iterative_player = lambda board: \
    run_search_function(board,
                        search_fn=alpha_beta_search,
                        eval_fn=focused_evaluate, timeout=5)
#run_game(human_player, ab_iterative_player)
                        
''' Test Ignacio: I'd expect a progressive deepening player using alpha-beta
    to consistently outperforma progressive deepening player using minimax
    when there is a time constraint 
minimax_iterative_player = lambda board: \
run_search_function(board, 
                    search_fn=minimax,
                    eval_fn=focused_evaluate, timeout=5)
run_game(ab_iterative_player, minimax_iterative_player)'''


## Finally, come up with a better evaluation function than focused-evaluate.
## By providing a different function, you should be able to beat
## simple-evaluate (or focused-evaluate) while searching to the
## same depth.

def better_evaluate(board):
    score = 0
    if board.is_game_over():
    # If the game has been won, we know that it must have been
    # won or ended by the previous move.
    # The previous move was made by our opponent.
    # Therefore, we can't have won, so return -1000.
    # (note that this causes a tie to be treated like a loss)
        # Use -1000 as a starting point, but still compute your best options
        score = -1000
    
    # If we can win the game, do so
    if board.longest_chain(board.get_current_player_id()) == 4:
        score = 5000
        return score
    
    # Prefer having longer chains
    chain_cells = board.chain_cells(board.get_current_player_id())
    for chain in chain_cells:
        if len(chain) == 3:
            score += 30
        elif len(chain) == 2:
            score += 5
            
    # Prefer having your pieces in the center of the board.
    for row in range(6):
        for col in range(7):
            if board.get_cell(row, col) == board.get_current_player_id():
                score -= abs(3-col)
            elif board.get_cell(row, col) == board.get_other_player_id():
                score += abs(3-col)

    return score

# Comment this line after you've fully implemented better_evaluate
#better_evaluate = memoize(basic_evaluate)

# Uncomment this line to make your better_evaluate run faster.
better_evaluate = memoize(better_evaluate)

# For debugging: Change this if-guard to True, to unit-test
# your better_evaluate function.
if False:
    board_tuples = (( 0,0,0,0,0,0,0 ),
                    ( 0,0,0,0,0,0,0 ),
                    ( 0,0,0,0,0,0,0 ),
                    ( 0,2,2,1,1,2,0 ),
                    ( 0,2,1,2,1,2,0 ),
                    ( 2,1,2,1,1,1,0 ),
                    )
    test_board_1 = ConnectFourBoard(board_array = board_tuples,
                                    current_player = 1)
    test_board_2 = ConnectFourBoard(board_array = board_tuples,
                                    current_player = 2)
    # better evaluate from player 1
    print("%s => %s" %(test_board_1, better_evaluate(test_board_1)))
    # better evaluate from player 2
    print("%s => %s" %(test_board_2, better_evaluate(test_board_2)))

## A player that uses alpha-beta and better_evaluate:
your_player = lambda board: run_search_function(board,
                                                search_fn=alpha_beta_search,
                                                eval_fn=better_evaluate,
                                                timeout=5)

#your_player = lambda board: alpha_beta_search(board, depth=4,
#                                              eval_fn=better_evaluate)

## Uncomment to watch your player play a game:
run_game(your_player, human_player)

## Uncomment this (or run it in the command window) to see how you do
## on the tournament that will be graded.
#run_game(your_player, basic_player)

# run_game(human_player, your_player)

## These three functions are used by the tester; please don't modify them!
def run_test_game(player1, player2, board):
    assert isinstance(globals()[board], ConnectFourBoard), "Error: can't run a game using a non-Board 3 object!"
    return run_game(globals()[player1], globals()[player2], globals()[board])
    
def run_test_search(search, board, depth, eval_fn):
    assert isinstance(globals()[board], ConnectFourBoard), "Error: can't run a game using a non-Board object!"
    return globals()[search](globals()[board], depth=depth,
                             eval_fn=globals()[eval_fn])

## This function runs your alpha-beta implementation using a tree as the search
## rather than a live connect four game.   This will be easier to debug.
def run_test_tree_search(search, board, depth):
    return globals()[search](globals()[board], depth=depth,
                             eval_fn=tree_searcher.tree_eval,
                             get_next_moves_fn=tree_searcher.tree_get_next_move,
                             is_terminal_fn=tree_searcher.is_leaf)
    
## Do you want us to use your code in a tournament against other students? See
## the description in the problem set. The tournament is completely optional
## and has no effect on your grade.
COMPETE = (True)

## The standard survey questions.
HOW_MANY_HOURS_THIS_PSET_TOOK = "2"
WHAT_I_FOUND_INTERESTING = "Creating functions to evaluate"
WHAT_I_FOUND_BORING = "Changing signs convention was confusing at first"
NAME = "Ignacio Paricio"
EMAIL = "sample"


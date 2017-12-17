from game_api import *
from boards import *
INF = float('inf')

def is_game_over_connectfour(board) :
    "Returns True if game is over, otherwise False."
    x = board.get_all_chains()
    if len(x) == 0:
        return False
    temp = len(x[0])
    for i in x:
        if len(i) > temp:
            temp = len(i)
    if temp >= 4:
        return True
    x = True
    for i in range(7):
        x = (board.is_column_full(i) and x)
    return x

def next_boards_connectfour(board) :
    """Returns a list of ConnectFourBoard objects that could result from the
    next move, or an empty list if no moves can be made."""
    if is_game_over_connectfour(board):
        return []
    li = []
    for i in range(7):
        if not board.is_column_full(i):
            li.append(board.add_piece(i))
    return li

def endgame_score_connectfour(board, is_current_player_maximizer) :
    """Given an endgame board, returns 1000 if the maximizer has won,
    -1000 if the minimizer has won, or 0 in case of a tie."""
    x = board.get_all_chains()
    temp = len(x[0])
    for i in x:
        if len(i) > temp:
            temp = len(i)
    if temp >= 4:
        if is_current_player_maximizer:
            return -1000
        return 1000
    return 0

def endgame_score_connectfour_faster(board, is_current_player_maximizer):
    """Given an endgame board, returns an endgame score with abs(score) >= 1000,
    returning larger absolute scores for winning sooner."""
    x = board.get_all_chains()
    temp = len(x[0])
    for i in x:
        if len(i) > temp:
            temp = len(i)
    if temp >= 4:
        if is_current_player_maximizer:
            return -1042 + board.count_pieces()
        return 1042 - board.count_pieces()
    return 0

def heuristic_connectfour(board, is_current_player_maximizer):
    """Given a non-endgame board, returns a heuristic score with
    abs(score) < 1000, where higher numbers indicate that the board is better
    for the maximizer."""
    currentchains = board.get_all_chains(True)
    nocurrentchains = len(currentchains)
    lencurrentchains = 0
    for i in currentchains:
        lencurrentchains += len(i)**2
    otherchains = board.get_all_chains(False)
    nootherchains = len(otherchains)
    lenotherchains = 0
    for i in otherchains:
        lenotherchains += len(i)**2
    p = lenotherchains + nootherchains-lencurrentchains-nocurrentchains
    if is_current_player_maximizer:
        return -p
    else:
        return p

# Now we can create AbstractGameState objects for Connect Four, using some of
# the functions you implemented above.  You can use the following examples to
# test your dfs and minimax implementations in Part 2.

# This AbstractGameState represents a new ConnectFourBoard, before the game has started:
state_starting_connectfour = AbstractGameState(snapshot = ConnectFourBoard(),
                                 is_game_over_fn = is_game_over_connectfour,
                                 generate_next_states_fn = next_boards_connectfour,
                                 endgame_score_fn = endgame_score_connectfour_faster)

# This AbstractGameState represents the ConnectFourBoard "NEARLY_OVER" from boards.py:
state_NEARLY_OVER = AbstractGameState(snapshot = NEARLY_OVER,
                                 is_game_over_fn = is_game_over_connectfour,
                                 generate_next_states_fn = next_boards_connectfour,
                                 endgame_score_fn = endgame_score_connectfour_faster)

# This AbstractGameState represents the ConnectFourBoard "BOARD_UHOH" from boards.py:
state_UHOH = AbstractGameState(snapshot = BOARD_UHOH,
                                 is_game_over_fn = is_game_over_connectfour,
                                 generate_next_states_fn = next_boards_connectfour,
                                 endgame_score_fn = endgame_score_connectfour_faster)


#### PART 2 ###########################################
# Note: Functions in Part 2 use the AbstractGameState API, not ConnectFourBoard.

def dfs_maximizing(state) :
    """Performs depth-first search to find path with highest endgame score.
    Returns a tuple containing:
     0. the best path (a list of AbstractGameState objects),
     1. the score of the leaf node (a number), and
     2. the number of static evaluations performed (a number)"""

    if state.is_game_over():
        return ([state,],state.get_endgame_score(),1)
    else:
        nextstate = state.generate_next_states()
        best = nextstate[0]
        eva = 0
        for i in nextstate:
            k = dfs_maximizing(i)
            eva += k[2]
            if k[1] > dfs_maximizing(best)[1]:
                best = i
        k = dfs_maximizing(best)
        return ([state,]+k[0],k[1],eva)


def minimax_endgame_search(state, maximize=True) :
    """Performs minimax search, searching all leaf nodes and statically
    evaluating all endgame scores.  Same return type as dfs_maximizing."""
    if state.is_game_over():
        return ([state,],state.get_endgame_score(),1)
    else:
        if maximize:
            nextstate = state.generate_next_states()
            best = nextstate[0]
            eva = 0
            for i in nextstate:
                k = minimax_endgame_search(i,False)
                eva += k[2]
                if k[1] > minimax_endgame_search(best,False)[1]:
                    best = i
            k = minimax_endgame_search(best,False)
            return ([state,]+k[0],k[1],eva)
        else:
            nextstate = state.generate_next_states()
            best = nextstate[0]
            eva = 0
            for i in nextstate:
                k = minimax_endgame_search(i,True)
                eva += k[2]
                if k[1] < minimax_endgame_search(best,True)[1]:
                    best = i
            k = minimax_endgame_search(best,True)
            return ([state,]+k[0],k[1],eva)           

# Uncomment the line below to try your minimax_endgame_search on an
# AbstractGameState representing the ConnectFourBoard "NEARLY_OVER" from boards.py:

#pretty_print_dfs_type(minimax_endgame_search(state_NEARLY_OVER))


def minimax_search(state, heuristic_fn=always_zero, depth_limit=INF, maximize=True) :
    "Performs standard minimax search.  Same return type as dfs_maximizing."
    if state.is_game_over():
        return ([state,],state.get_endgame_score(),1)
    else:
        if depth_limit == 0:
            return ([state,],heuristic_fn(state.get_snapshot(),maximize),1)
        else:
            if maximize:
                nextstate = state.generate_next_states()
                best = nextstate[0]
                eva = 0
                for i in nextstate:
                    k = minimax_search(i,heuristic_fn,depth_limit-1,False)
                    eva += k[2]
                    if k[1] > minimax_search(best,heuristic_fn,depth_limit-1,False)[1]:
                        best = i
                k = minimax_search(best,heuristic_fn,depth_limit-1,False)
                return ([state,]+k[0],k[1],eva)
            else:
                nextstate = state.generate_next_states()
                best = nextstate[0]
                eva = 0
                for i in nextstate:
                    k = minimax_search(i,heuristic_fn,depth_limit-1,True)
                    eva += k[2]
                    if k[1] < minimax_search(best,heuristic_fn,depth_limit-1,True)[1]:
                        best = i
                k = minimax_search(best,heuristic_fn,depth_limit-1,True)
                return ([state,]+k[0],k[1],eva) 

# Uncomment the line below to try minimax_search with "BOARD_UHOH" and
# depth_limit=1.  Try increasing the value of depth_limit to see what happens:

#pretty_print_dfs_type(minimax_search(state_UHOH, heuristic_fn=heuristic_connectfour, depth_limit=1))


def minimax_search_alphabeta(state, alpha=-INF, beta=INF, heuristic_fn=always_zero,
                             depth_limit=INF, maximize=True) :
    "Performs minimax with alpha-beta pruning.  Same return type as dfs_maximizing."
    if state.is_game_over():
        return ([state,],state.get_endgame_score(maximize),1)
    else:
        if depth_limit == 0:
            return ([state,],heuristic_fn(state.get_snapshot(),maximize),1)
        else:
            if maximize:
                bestval = alpha
                nextstate = state.generate_next_states()
                eva = 0
                besttup = minimax_search_alphabeta(nextstate[0],bestval,beta,heuristic_fn,depth_limit-1,False)
                for i in nextstate:
                    k = minimax_search_alphabeta(i,bestval,beta,heuristic_fn,depth_limit-1,False)
                    eva += k[2]
                    if k[1] > bestval:
                        best = i
                        besttup = k
                        bestval = k[1]
                    if beta <= bestval:
                        break

                return ([state,]+besttup[0],bestval,eva)
            else:
                bestval = beta
                nextstate = state.generate_next_states()
                eva = 0
                besttup = minimax_search_alphabeta(nextstate[0],alpha,bestval,heuristic_fn,depth_limit-1,True)
                for i in nextstate:
                    k = minimax_search_alphabeta(i,alpha,bestval,heuristic_fn,depth_limit-1,True)
                    eva += k[2]
                    if k[1] < bestval:
                        best = i
                        besttup = k
                        bestval = k[1]
                    if alpha >= bestval:
                        break
                        
                return ([state,]+besttup[0],bestval,eva) 

# Uncomment the line below to try minimax_search_alphabeta with "BOARD_UHOH" and
# depth_limit=4.  Compare with the number of evaluations from minimax_search for
# different values of depth_limit.

#pretty_print_dfs_type(minimax_search_alphabeta(state_UHOH, heuristic_fn=heuristic_connectfour, depth_limit=4))


def progressive_deepening(state, heuristic_fn=always_zero, depth_limit=INF,
                          maximize=True) :
    """Runs minimax with alpha-beta pruning. At each level, updates anytime_value
    with the tuple returned from minimax_search_alphabeta. Returns anytime_value."""
    anytime_value = AnytimeValue()   # TA Note: Use this to store values.
    for i in range(1,depth_limit+1):
        anytime_value.set_value(minimax_search_alphabeta(state,-INF,INF,heuristic_fn,i,maximize))
        '''prevlevel = anytime_value.get_value()
        if maximize:
            if i%2 == 0:
                anytime_value.set_value(minimax_search_alphabeta(state,prevlevel[1],INF,heuristic_fn,i,maximize))
            else:
                anytime_value.set_value(minimax_search_alphabeta(state,-INF,prevlevel[1],heuristic_fn,i,not maximize))
        else:
            if i%2 == 0:
p                anytime_value.set_value(minimax_search_alphabeta(state,-INF,prevlevel[1],heuristic_fn,i,maximize))
            else:
                anytime_value.set_value(minimax_search_alphabeta(state,prevlevel[1],INF,heuristic_fn,i,not maximize))'''
    return anytime_value

# Uncomment the line below to try progressive_deepening with "BOARD_UHOH" and
# depth_limit=4.  Compare the total number of evaluations with the number of
# evaluations from minimax_search or minimax_search_alphabeta.

progressive_deepening(state_UHOH, heuristic_fn=heuristic_connectfour, depth_limit=4).pretty_print()


#### SURVEY ###################################################

NAME = "Sze Nga Wong"
COLLABORATORS = "Kelly Shen"
HOW_MANY_HOURS_THIS_LAB_TOOK = 10
WHAT_I_FOUND_INTERESTING = ""
WHAT_I_FOUND_BORING = ""
SUGGESTIONS = None


###########################################################
### Ignore everything below this line; for testing only ###
###########################################################

# The following lines are used in the tester. DO NOT CHANGE!

def wrapper_connectfour(board_array, players, whose_turn = None) :
    board = ConnectFourBoard(board_array = board_array,
                             players = players,
                             whose_turn = whose_turn)
    return AbstractGameState(snapshot = board,
                             is_game_over_fn = is_game_over_connectfour,
                             generate_next_states_fn = next_boards_connectfour,
                             endgame_score_fn = endgame_score_connectfour_faster)

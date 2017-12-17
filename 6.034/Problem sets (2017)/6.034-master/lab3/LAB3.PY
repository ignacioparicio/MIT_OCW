from game_api import *
from boards import *
INF = float('inf')

def is_game_over_connectfour(board) :
    "Returns True if game is over, otherwise False."
    win = False

    # Check if four are contiguous
    for chain in board.get_all_chains(current_player=None):
        if len(chain) == 4:
            win = True

    # If board full, game over
    if board.count_pieces(current_player=None) == 42:
        return True
    # Elif a player has won (4 contiguous), game over
    elif win:
        return win
    # else game on
    else:
        return False

def next_boards_connectfour(board) :
    """Returns a list of ConnectFourBoard objects that could result from the
    next move, or an empty list if no moves can be made."""
    boards = []
    # Generate all seven possible boards for each column move, minus moves for full columns
    for col_number in range(0,7):
        # if not full column
        if not board.is_column_full(col_number):
            # add new board to boards
            boards.append(board.add_piece(col_number))

    # Return empty if game is over
    if is_game_over_connectfour(board):
        return []
    # else return possible move boards
    else: 
        return boards

def endgame_score_connectfour(board, is_current_player_maximizer) :
    """Given an endgame board, returns 1000 if the maximizer has won,
    -1000 if the minimizer has won, or 0 in case of a tie."""
    if is_current_player_maximizer:
        return -1000
    else:
        return 1000

def endgame_score_connectfour_faster(board, is_current_player_maximizer) :
    """Given an endgame board, returns an endgame score with abs(score) >= 1000,
    returning larger absolute scores for winning sooner."""
    if is_current_player_maximizer:
        return -1000 - (42 - board.count_pieces())
    else:
        return 1000 + (42 - board.count_pieces())

def heuristic_connectfour(board, is_current_player_maximizer) :
    """Given a non-endgame board, returns a heuristic score with
    abs(score) < 1000, where higher numbers indicate that the board is better
    for the maximizer."""
    def chain_heuristic_calculator(board, is_current_player_maximizer):
        score = 0
        for chain in board.get_all_chains(is_current_player_maximizer):
            if len(chain) == 1:
                score += 1
            elif len(chain) == 2:
                score += 10
            elif len(chain) == 3:
                score += 100
        return score

    # Heuristic is difference between min's and max's weighted score
    heuristic = chain_heuristic_calculator(board, is_current_player_maximizer) - chain_heuristic_calculator(board, not is_current_player_maximizer) 

    return heuristic




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
    paths = []

    def depth_expand(state, path):
        # for each child of parent state

        new_path = path[:]
        new_path.append(state)

        if state.is_game_over():
            paths.append(new_path)
            return True

        else:
            for child in state.generate_next_states():
                depth_expand(child, new_path)

    depth_expand(state, [])


    num_evaluations = 0
    path_scores = []
    for p in paths:
        path_score = p[-1].get_endgame_score(is_current_player_maximizer=True)
        path_scores.append(path_score)
        num_evaluations += 1 #len(path) - 1

    best_path_index = path_scores.index(max(path_scores))
    best_path = paths[best_path_index]
    best_score = max(path_scores)

    return [best_path, best_score, num_evaluations]




def minimax_endgame_search(state, maximize=True) :
    """Performs minimax search, searching all leaf nodes and statically
    evaluating all endgame scores.  Same return type as dfs_maximizing."""
    paths = []

    def depth_expand(state, path):
        # for each child of parent state

        new_path = path[:]
        new_path.append(state)

        if state.is_game_over():
            paths.append(new_path)
            return True

        else:
            for child in state.generate_next_states():
                depth_expand(child, new_path)

    # Get all the possible paths, store in paths = []
    depth_expand(state, [])


    def minimax_score(state, maximize):
        if state.is_game_over():
            return [state.get_endgame_score(maximize), state]
        else:
            if maximize:
                max_score = max([minimax_score(child, False)[0] for child in state.generate_next_states()])
                for child in state.generate_next_states():
                    if minimax_score(child, False)[1].get_endgame_score(maximize) == max_score:
                        max_state = child

                return [max_score, max_state]
            else:
                min_score = min([minimax_score(child, True)[0] for child in state.generate_next_states()])
                for child in state.generate_next_states():
                    if minimax_score(child, True)[1].get_endgame_score(maximize) == min_score:
                        min_state = child

                return [min_score, min_state]

    # Get min/max scores at from leaves, as well as corresponding parent state
    score, end_node = minimax_score(state, maximize)[0], minimax_score(state, maximize)[1]

    num_evaluations = 0
    relevant_paths = []
    for p in paths:
        if p[-1].get_endgame_score(maximize) == score and p[-2] == end_node:
            relevant_paths.append(p)
        num_evaluations += 1

    return (relevant_paths[0], score, num_evaluations)

# Uncomment the line below to try your minimax_endgame_search on an
# AbstractGameState representing the ConnectFourBoard "NEARLY_OVER" from boards.py:

# pretty_print_dfs_type(minimax_endgame_search(state_NEARLY_OVER))


def minimax_search(state, heuristic_fn=always_zero, depth_limit=INF, maximize=True) :
    # "Performs standard minimax search.  Same return type as dfs_maximizing."
    paths = []

    def depth_expand(state, path):
        # for each child of parent state

        new_path = path[:]
        new_path.append(state)

        if state.is_game_over():
            paths.append(new_path)
            return True

        else:
            for child in state.generate_next_states():
                depth_expand(child, new_path)

    # Get all the possible paths, store in paths = []
    depth_expand(state, [])

    global depth
    depth = []

    def minimax_score(state, maximize):
        global depth
        if len(depth) == depth_limit:
            return [heuristic_fn(state), state]
            depth.append(1)
        elif state.is_game_over():
            return [state.get_endgame_score(maximize), state]
            depth.append(1)
        else:
            if maximize:
                depth += [1]
                max_score = max([minimax_score(child, False)[0] for child in state.generate_next_states()])
                for child in state.generate_next_states():
                    if minimax_score(child, False)[1].get_endgame_score(maximize) == max_score:
                        max_state = child

                return [max_score, max_state]
            else:
                depth += [1]
                min_score = min([minimax_score(child, True)[0] for child in state.generate_next_states()])
                for child in state.generate_next_states():
                    if minimax_score(child, True)[1].get_endgame_score(maximize) == min_score:
                        min_state = child

                return [min_score, min_state]

    # Get min/max scores at from leaves, as well as corresponding parent state
    score, end_node = minimax_score(state, maximize)[0], minimax_score(state, maximize)[1]

    num_evaluations = 0
    relevant_paths = []
    for p in paths:
        if p[-1].get_endgame_score(maximize) == score and p[-2] == end_node:
            relevant_paths.append(p)
        num_evaluations += 1

    return (relevant_paths[0], score, num_evaluations)



def minimax_search_alphabeta(state, alpha=-INF, beta=INF, heuristic_fn=always_zero,
                             depth_limit=INF, maximize=True) :
    "Performs minimax with alpha-beta pruning.  Same return type as dfs_maximizing."
    raise NotImplementedError

# Uncomment the line below to try minimax_search_alphabeta with "BOARD_UHOH" and
# depth_limit=4.  Compare with the number of evaluations from minimax_search for
# different values of depth_limit.

#pretty_print_dfs_type(minimax_search_alphabeta(state_UHOH, heuristic_fn=heuristic_connectfour, depth_limit=4))


def progressive_deepening(state, heuristic_fn=always_zero, depth_limit=INF,
                          maximize=True) :
    """Runs minimax with alpha-beta pruning. At each level, updates anytime_value
    with the tuple returned from minimax_search_alphabeta. Returns anytime_value."""
    anytime_value = AnytimeValue()   # TA Note: Use this to store values.
    raise NotImplementedError
    return anytime_value

# Uncomment the line below to try progressive_deepening with "BOARD_UHOH" and
# depth_limit=4.  Compare the total number of evaluations with the number of
# evaluations from minimax_search or minimax_search_alphabeta.

#progressive_deepening(state_UHOH, heuristic_fn=heuristic_connectfour, depth_limit=4).pretty_print()


#### SURVEY ###################################################

NAME = 'Laser Nite'
COLLABORATORS = 'nope'
HOW_MANY_HOURS_THIS_LAB_TOOK = 20
WHAT_I_FOUND_INTERESTING = 'finishing'
WHAT_I_FOUND_BORING = 'getting stuck on search algorithim implementations for hours and hours, implementing minimax but doing so really ****ily and then **** my life '
SUGGESTIONS = 'Get rid of super frustrating and pointlessly ambiguous test cases that say things like "Expected: List of [best_path, leaf_score, and evaluation_count] corresponding to minimax score when the first player is the maximizer." it would be way nicer to get actual expected values so the test actually has a use, ie. allows the programmer (me) to see where the algorithim is going wrong. There being no online tests for weeks sucked too.'


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

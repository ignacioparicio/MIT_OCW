from search import Edge, UndirectedGraph, do_nothing_fn, make_generic_search
import read_graphs

all_graphs = read_graphs.get_graphs()
GRAPH_0 = all_graphs['GRAPH_0']
GRAPH_1 = all_graphs['GRAPH_1']
GRAPH_2 = all_graphs['GRAPH_2']
GRAPH_3 = all_graphs['GRAPH_3']
GRAPH_FOR_HEURISTICS = all_graphs['GRAPH_FOR_HEURISTICS']

#Change this to True if you want to run additional local tests for debugging:
RUN_ADDITIONAL_TESTS = False

#### PART 1: Helper Functions #########################################

def path_length(graph, path):
    total_length = 0
    for node_index in range(len(path)-1):
        edge_length = graph.get_edge(path[node_index], path[node_index + 1]).length
        total_length += edge_length
    return total_length


def has_loops(path):
    unique_nodes = set(path)
    # if the set is shorter than the array, there must be duplicates that are getting eliminated by set()
    if len(unique_nodes) < len(path):
        return True
    else:
        return False

def extensions(graph, path):
    paths = []
    # For each next possible node in the graph, extend out the path
    for extended_node in graph.get_neighbors(path[-1]):
        extended_path = path + [extended_node]
        # If has loops don't append path
        if not has_loops(extended_path):
            paths.append(extended_path)
    return paths


def sort_by_heuristic(graph, goalNode, nodes):
    # sort the node based on heuristic to goal
    return sorted(nodes, key= lambda node: (graph.get_heuristic_value(node, goalNode), node))


# You can ignore the following line.  It allows generic_search (PART 3) to 
# access the extensions and has_loops functions that you defined in PART 1.
generic_search = make_generic_search(extensions, has_loops)  # DO NOT CHANGE

#### PART 2: Search Algorithms #########################################

# Note: Optionally, you may skip to Part 3: Generic Search,
# then complete Part 2 using your answers from Part 3.

def dfs(graph, startNode, goalNode):
    return generic_search(*generic_dfs)(graph, startNode, goalNode)


def bfs(graph, startNode, goalNode):
    return generic_search(*generic_bfs)(graph, startNode, goalNode)



def hill_climbing(graph, startNode, goalNode):
    return generic_search(*generic_hill_climbing)(graph, startNode, goalNode)


def best_first(graph, startNode, goalNode):
    return generic_search(*generic_best_first)(graph, startNode, goalNode)


def beam(graph, startNode, goalNode, beam_width):
    return generic_search(*generic_beam)(graph, startNode, goalNode, beam_width)

def branch_and_bound(graph, startNode, goalNode):
    return generic_search(*generic_branch_and_bound)(graph, startNode, goalNode)

def branch_and_bound_with_heuristic(graph, startNode, goalNode):
    return generic_search(*generic_branch_and_bound_with_heuristic)(graph, startNode, goalNode)


def branch_and_bound_with_extended_set(graph, startNode, goalNode):
    return generic_search(*generic_branch_and_bound_with_extended_set)(graph, startNode, goalNode)


def a_star(graph, startNode, goalNode):
    return generic_search(*generic_a_star)(graph, startNode, goalNode)


#### PART 3: Generic Search #######################################

# Define your custom path-sorting functions here.  
# Each path-sorting function should be in this form:

# def my_sorting_fn(graph, goalNode, paths):
#     # YOUR CODE HERE
#     return sorted_paths

def heuristic_path_sorting(graph, goalNode, paths):
    return sorted(paths, key= lambda path: (graph.get_heuristic_value(path[-1], goalNode), path))

def heuristic_and_edge_length_path_sorting(graph, goalNode, paths):
    return sorted(paths, key= lambda path: (graph.get_heuristic_value(path[-1], goalNode) + path_length(graph, path), path))

def path_length_agenda_sorting(graph, goalNode, paths):
    queue = []
    for path in paths:
        length = path_length(graph, path)
        path.append(length)

        queue.append(path)

    sorted_queue = sorted(queue, key= lambda path: path[-1])

    for path in sorted_queue:
        del path[-1]

    return sorted_queue

def path_length_and_heuristic_agenda_sorting(graph, goalNode, paths):
    queue = []
    for path in paths:
        length = path_length(graph, path)
        path.append(length)

        queue.append(path)

    sorted_queue = sorted(queue, key= lambda path: path[-1] + graph.get_heuristic_value(path[-2], goalNode) )

    for path in sorted_queue:
        del path[-1]

    return sorted_queue





def generic_best_first_sort_agenda_fn(graph, goalNode, paths):
    return do_nothing_fn(graph, goalNode, paths)

def generic_bfs_sort_new_paths_fn(graph, goalNode, paths):
    return do_nothing_fn(graph, goalNode, paths)

def generic_branch_and_bound_sort_agenda_fn(graph, goalNode, paths):
    return path_length_and_heuristic_agenda_sorting(graph, goalNode, paths)

def generic_branch_and_bound_with_extended_set_sort_agenda_fn(graph, goalNode, paths):
    return path_length_agenda_sorting(graph, goalNode, paths)

def generic_dfs_sort_new_paths_fn(graph, goalNode, paths):
    return do_nothing_fn(graph, goalNode, paths)

def generic_hill_climbing_sort_new_paths_fn(graph, goalNode, paths):
    return heuristic_path_sorting(graph, goalNode, paths)


# To create a search algorithm that 
#does not sort new paths, 
#adds paths to the front of the agenda, 
#does not sort the agenda, and 
#does not use an extended set, you can call generic_search like this:
# my_search_fn = generic_search(do_nothing_fn, True, do_nothing_fn, False)
#def generic_search(sort_result_fn, add_paths_to_front_of_agenda, sort_agenda_fn, use_extended_set):


generic_dfs = [do_nothing_fn, True, do_nothing_fn, False]

generic_bfs = [do_nothing_fn, False, do_nothing_fn, False]

generic_hill_climbing = [heuristic_path_sorting, True, do_nothing_fn, False]

generic_best_first = [do_nothing_fn, False, heuristic_path_sorting, False]

generic_branch_and_bound = [do_nothing_fn, False, path_length_agenda_sorting, False]

generic_branch_and_bound_with_heuristic = [heuristic_and_edge_length_path_sorting, False, path_length_and_heuristic_agenda_sorting, False]

generic_branch_and_bound_with_extended_set = [do_nothing_fn, False, path_length_agenda_sorting, True]

generic_a_star = [heuristic_and_edge_length_path_sorting, False, path_length_and_heuristic_agenda_sorting, True]

# Here is an example of how to call generic_search (uncomment to run):
#my_dfs_fn = generic_search(*generic_dfs)
#my_dfs_path = my_dfs_fn(GRAPH_2, 'S', 'G')
#print my_dfs_path

# Or, combining the first two steps:
#my_dfs_path = generic_search(*generic_dfs)(GRAPH_2, 'S', 'G')
#print my_dfs_path


### OPTIONAL: Generic Beam Search
# If you want to run local tests for generic_beam, change TEST_GENERIC_BEAM to True:
TEST_GENERIC_BEAM = True

# The sort_agenda_fn for beam search takes fourth argument, beam_width:
def my_beam_sorting_fn(graph, goalNode, paths, beam_width):
    queue = []
    for path in paths:
        length = path_length(graph, path)
        path.append(length)

        queue.append(path)

    sorted_queue = sorted(queue, key= lambda path: graph.get_heuristic_value(path[-2], goalNode) )

    for path in sorted_queue:
        del path[-1]

    return sorted_queue[0:beam_width]
    

generic_beam = [do_nothing_fn, False, my_beam_sorting_fn, False]

# Uncomment this to test your generic_beam search:
# print generic_search(*generic_beam)(GRAPH_2, 'S', 'G', beam_width=2)

#### PART 4: Heuristics ###################################################

def is_admissible(graph, goalNode):
    for node in graph.nodes:
        # If heuristic of node is greater than shortest path to goal from node
        if graph.get_heuristic_value(node, goalNode) > path_length(graph, branch_and_bound_with_extended_set(graph, node, goalNode)):
            return False
    return True
    

def is_consistent(graph, goalNode):
    error_count = 0
    for node in graph.nodes:
        neighbors = graph.get_neighbors(node)
        for node1 in neighbors:
            edge_length = graph.get_edge(node, node1).length
            heuristic_difference = abs(graph.get_heuristic_value(node, goalNode) - graph.get_heuristic_value(node1, goalNode))
            if heuristic_difference > edge_length:
                return False
    return True



### OPTIONAL: Picking Heuristics
# If you want to run local tests on your heuristics, change TEST_HEURISTICS to True:
TEST_HEURISTICS = False

# heuristic_1: admissible and consistent

[h1_S, h1_A, h1_B, h1_C, h1_G] = [None, None, None, None, None]

heuristic_1 = {'G': {}}
heuristic_1['G']['S'] = h1_S
heuristic_1['G']['A'] = h1_A
heuristic_1['G']['B'] = h1_B
heuristic_1['G']['C'] = h1_C
heuristic_1['G']['G'] = h1_G


# heuristic_2: admissible but NOT consistent

[h2_S, h2_A, h2_B, h2_C, h2_G] = [None, None, None, None, None]

heuristic_2 = {'G': {}}
heuristic_2['G']['S'] = h2_S
heuristic_2['G']['A'] = h2_A
heuristic_2['G']['B'] = h2_B
heuristic_2['G']['C'] = h2_C
heuristic_2['G']['G'] = h2_G


# heuristic_3: admissible but A* returns non-optimal path to G

[h3_S, h3_A, h3_B, h3_C, h3_G] = [None, None, None, None, None]

heuristic_3 = {'G': {}}
heuristic_3['G']['S'] = h3_S
heuristic_3['G']['A'] = h3_A
heuristic_3['G']['B'] = h3_B
heuristic_3['G']['C'] = h3_C
heuristic_3['G']['G'] = h3_G


# heuristic_4: admissible but not consistent, yet A* finds optimal path

[h4_S, h4_A, h4_B, h4_C, h4_G] = [None, None, None, None, None]

heuristic_4 = {'G': {}}
heuristic_4['G']['S'] = h4_S
heuristic_4['G']['A'] = h4_A
heuristic_4['G']['B'] = h4_B
heuristic_4['G']['C'] = h4_C
heuristic_4['G']['G'] = h4_G


#### SURVEY ###################################################

NAME = 'Laser Nite'
COLLABORATORS = 'None'
HOW_MANY_HOURS_THIS_LAB_TOOK = 7
WHAT_I_FOUND_INTERESTING = "overarching concepts, search methods"
WHAT_I_FOUND_BORING = "will update if time"
SUGGESTIONS = "implementation for beam wasn't clear, and the patch that pulls the path and agenda makers behaves strangely."

'''
def generic_best_first_sort_agenda_fn(graph, goalNode, paths):
    return path_length_agenda_sorting(graph, goalNode, paths)

def generic_bfs_sort_new_paths_fn(graph, goalNode, paths):
    return heuristic_path_sorting(graph, goalNode, paths)

def generic_branch_and_bound_sort_agenda_fn(graph, goalNode, paths):
    return path_length_agenda_sorting(graph, goalNode, paths)

def generic_branch_and_bound_with_extended_set_sort_agenda_fn(graph, goalNode, paths):
    return path_length_agenda_sorting(graph, goalNode, paths)

def generic_dfs_sort_new_paths_fn(graph, goalNode, paths):
    return paths


def sort_by_heuristic(graph, goalNode, paths):
    pass
'''

###########################################################
### Ignore everything below this line; for testing only ###
###########################################################

# The following lines are used in the tester. DO NOT CHANGE!

generic_dfs_sort_result_fn = generic_dfs[0]
generic_bfs_sort_result_fn = generic_bfs[0]
generic_hill_climbing_sort_result_fn = generic_hill_climbing[0]
generic_best_first_sort_result_fn = generic_best_first[0]
generic_branch_and_bound_sort_result_fn = generic_branch_and_bound[0]
generic_branch_and_bound_with_heuristic_sort_result_fn = generic_branch_and_bound_with_heuristic[0]
generic_branch_and_bound_with_extended_set_sort_result_fn = generic_branch_and_bound_with_extended_set[0]
generic_a_star_sort_result_fn = generic_a_star[0]

generic_dfs_sort_agenda_fn = generic_dfs[2]
generic_bfs_sort_agenda_fn = generic_bfs[2]
generic_hill_climbing_sort_agenda_fn = generic_hill_climbing[2]
generic_best_first_sort_agenda_fn = generic_best_first[2]
generic_branch_and_bound_sort_agenda_fn = generic_branch_and_bound[2]
generic_branch_and_bound_with_heuristic_sort_agenda_fn = generic_branch_and_bound_with_heuristic[2]
generic_branch_and_bound_with_extended_set_sort_agenda_fn = generic_branch_and_bound_with_extended_set[2]
generic_a_star_sort_agenda_fn = generic_a_star[2]
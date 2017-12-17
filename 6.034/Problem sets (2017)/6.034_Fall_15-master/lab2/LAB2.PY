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
    l = 0
    for i in range(len(path)-1):
        l += graph.get_edge(path[i],path[i+1]).length
    return l


def has_loops(path):
    i = set()
    for j in path:
        if j not in i:
            i.add(j)
        else:
            return True
    return False


def extensions(graph, path):
    m = graph.get_neighbors(path[-1])
    n = []
    for i in m:
        j = []
        for k in path:
            j.append(k)
        j.append(i)
        if not has_loops(j):
            n.append(j)
    return break_ties(n)


def sort_by_heuristic(graph, goalNode, nodes):
    k = sorted(nodes)
    return sorted(k, key = lambda x:graph.get_heuristic_value(x,goalNode))


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
    '''agenda = [[startNode]]
    notfound = True
    while notfound and (len(agenda) != 0):
        m = agenda.pop(0)
        k = extensions(graph,m)
        newk=[]
        for i in k:
            if not has_loops(i):
                newk.append(i)
            if i[-1] == goalNode:
                notfound = False
                path = i
        agenda = agenda + newk
    if notfound == True:
        return None
    else:
        return path'''
            
def hill_climbing(graph, startNode, goalNode):
    return generic_search(*generic_hill_climbing)(graph, startNode, goalNode)
    '''agenda = [[startNode]]
    notfound = True
    while notfound and (len(agenda) != 0):
        m = agenda.pop(0)
        k = extensions(graph,m)
        newk=[]
        for i in k:
            if not has_loops(i):
                newk.append(i)
            if i[-1] == goalNode:
                notfound = False
                path = i
        newk = sorted(newk,key = lambda x: graph.get_heuristic_value(x[-1],goalNode))
        agenda = newk + agenda
    if notfound == True:
        return None
    else:
        return path'''


def best_first(graph, startNode, goalNode):
    return generic_search(*generic_best_first)(graph, startNode, goalNode)
    '''agenda = [[startNode]]
    notfound = True
    while notfound and (len(agenda) != 0):
        m = agenda.pop(0)
        k = extensions(graph,m)
        newk=[]
        for i in k:
            if not has_loops(i):
                newk.append(i)
            if i[-1] == goalNode:
                notfound = False
                path = i
        agenda = newk + agenda
        agenda = sorted(agenda,key = lambda x: graph.get_heuristic_value(x[-1],goalNode))
    if notfound == True:
        return None
    else:
        return path'''

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


generic_dfs = [do_nothing_fn, True, do_nothing_fn, False]

generic_bfs = [do_nothing_fn, False, do_nothing_fn, False]

def sorting_hill(graph, goalNode, paths):
    m = sorted(paths)
    return sorted(m,key = lambda x: graph.get_heuristic_value(x[-1],goalNode))
generic_hill_climbing = [sorting_hill, True, do_nothing_fn, False]

def sorting_best(graph, goalNode, agenda):
    m = sorted(agenda)
    return sorted(m, key = lambda x: graph.get_heuristic_value(x[-1],goalNode))
generic_best_first = [do_nothing_fn, True, sorting_best, False]

def sorting_branch_extended(graph, goalNode, agenda):
    m = sorted(agenda)
    return sorted(m, key = lambda x: path_length(graph,x))
generic_branch_and_bound = [do_nothing_fn, True, sorting_branch_extended, False]

def sorting_branch_heuristic(graph, goalNode, agenda):
    m = sorted(agenda)
    return sorted(m, key = lambda x: path_length(graph,x) + graph.get_heuristic_value(x[-1],goalNode))
generic_branch_and_bound_with_heuristic = [do_nothing_fn, True, sorting_branch_heuristic, False]

generic_branch_and_bound_with_extended_set = [do_nothing_fn, True, sorting_branch_extended, True]

generic_a_star = [do_nothing_fn, True, sorting_branch_heuristic, True]

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

def break_ties(paths):
    return sorted(paths)
# The sort_agenda_fn for beam search takes fourth argument, beam_width:
def my_beam_sorting_fn(graph, goalNode, paths, beam_width):
    paths = sorted(paths)
    sorted_beam_agenda = sorted(paths, key = lambda x: len(x))
    if len(sorted_beam_agenda) == 0:
        return sorted_beam_agenda
    length = len(sorted_beam_agenda[0])
    b = True
    for i in sorted_beam_agenda:
        if len(i) != length:
            b = False
    if b:
        sorted_beam_agenda = sorted(paths, key = lambda x: graph.get_heuristic_value(x[-1],goalNode))
        sorted_beam_agenda = sorted_beam_agenda[:beam_width]
    return sorted_beam_agenda
    '''sorted_beam_agenda = sorted(paths, key = lambda x: graph.get_heuristic_value(x[-1],goalNode))
    if len(sorted_beam_agenda) == 0:
        return sorted_beam_agenda
    length = len(sorted_beam_agenda[0])
    b = True
    for i in sorted_beam_agenda:
        if len(i) != length:
            b = False
    if b:
        sorted_beam_agenda = sorted_beam_agenda[:beam_width]
    print sorted_beam_agenda
    return sorted_beam_agenda'''

"""    m = {n + 1 : 0 for n in range(len(graph.nodes))}
    for i in sorted_beam_agenda:
        m[len(i)] += 1
        if m[len(i)] > beam_width:
            sorted_beam_agenda.remove(i)"""

generic_beam = [do_nothing_fn, True, my_beam_sorting_fn, False]

# Uncomment this to test your generic_beam search:
print generic_search(*generic_beam)(GRAPH_2, 'S', 'G', beam_width=2)


#### PART 4: Heuristics ###################################################

def is_admissible(graph, goalNode):
    '''lnodes = graph.nodes
    b = True
    for i in lnodes:
        if graph.get_heuristic_value(i,goalNode):'''
    lnodes = graph.nodes
    if len(lnodes) == 0:
        return True
    dic = {i:1000000 for i in lnodes}
    unvisited = {i for i in lnodes}
    dic[goalNode] = 0
    current = goalNode
    m = True
    while m:
        unvisited.remove(current)
        for i in graph.get_neighbors(current):
            if i in unvisited:
                tentative = dic[current] + graph.get_edge(current,i).length
                if tentative < dic[i]:
                    dic[i] = tentative
        n = False
        x = 1000000
        for i in unvisited:
            if dic[i] < 1000000:
                n = True
            if dic[i] < x:
                current = i
                x = dic[i]
        m = n
    b = True
    for i in lnodes:
        if graph.get_heuristic_value(i,goalNode) > dic[i]:
            b = False
    return b


def is_consistent(graph, goalNode):
    m = graph.edges
    b = True
    for i in m:
        x = i.startNode
        y = i.endNode
        if i.length < abs(graph.get_heuristic_value(x,goalNode) - graph.get_heuristic_value(y,goalNode)):
            b = False
    return b


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

NAME = 'Sze Nga Wong'
COLLABORATORS = ''
HOW_MANY_HOURS_THIS_LAB_TOOK = 7
WHAT_I_FOUND_INTERESTING = ''
WHAT_I_FOUND_BORING = ''
SUGGESTIONS = None

generic_dfs_sort_new_paths_fn = generic_dfs[0]
generic_bfs_sort_new_paths_fn = generic_bfs[0]
generic_hill_climbing_sort_new_paths_fn = generic_hill_climbing[0]
generic_best_first_sort_new_paths_fn = generic_best_first[0]
generic_branch_and_bound_sort_new_paths_fn = generic_branch_and_bound[0]
generic_branch_and_bound_with_heuristic_sort_new_paths_fn = generic_branch_and_bound_with_heuristic[0]
generic_branch_and_bound_with_extended_set_sort_new_paths_fn = generic_branch_and_bound_with_extended_set[0]
generic_a_star_sort_new_paths_fn = generic_a_star[0]

generic_dfs_sort_agenda_fn = generic_dfs[2]
generic_bfs_sort_agenda_fn = generic_bfs[2]
generic_hill_climbing_sort_agenda_fn = generic_hill_climbing[2]
generic_best_first_sort_agenda_fn = generic_best_first[2]
generic_branch_and_bound_sort_agenda_fn = generic_branch_and_bound[2]
generic_branch_and_bound_with_heuristic_sort_agenda_fn = generic_branch_and_bound_with_heuristic[2]
generic_branch_and_bound_with_extended_set_sort_agenda_fn = generic_branch_and_bound_with_extended_set[2]
generic_a_star_sort_agenda_fn = generic_a_star[2]

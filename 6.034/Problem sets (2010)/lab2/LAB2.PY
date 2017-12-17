# Fall 2012 6.034 Lab 2: Search
#
# Your answers for the true and false questions will be in the following form.  
# Your answers will look like one of the two below:
#ANSWER1 = True
#ANSWER1 = False

# 1: True or false - Hill Climbing search is guaranteed to find a solution
#    if there is a solution
ANSWER1 = False

# 2: True or false - Best-first search will give an optimal search result
#    (shortest path length).
#    (If you don't know what we mean by best-first search, refer to
#     http://courses.csail.mit.edu/6.034f/ai3/ch4.pdf (page 13 of the pdf).)
ANSWER2 = False

# 3: True or false - Best-first search and hill climbing make use of
#    heuristic values of nodes.
ANSWER3 = True

# 4: True or false - A* uses an extended-nodes set.
ANSWER4 = True

# 5: True or false - Breadth first search is guaranteed to return a path
#    with the shortest number of nodes.
ANSWER5 = True

# 6: True or false - The regular branch and bound uses heuristic values
#    to speed up the search for an optimal path.
ANSWER6 = False

# Import the Graph data structure from 'search.py'
# Refer to search.py for documentation
from search import Graph

## Optional Warm-up: BFS and DFS
# If you implement these, the offline tester will test them.
# If you don't, it won't.
# The online tester will not test them.

def bfs(graph, start, goal):
    """
    Finds a path between start and goal node using breadth-first search.

    Parameters:
        graph: Graph
            The graph on which to carry out the search
        start: string
            Node number at which to start
        goal: string
            Node number at which to end

    Returns:
        A list of nodes from start to goal using breadth-first search,
        represented by a list of nodes (in strings), [n_1, n_2, ..., n_k]
        where there exists an edge from n_i to n_(i+1) in graph

        If there exists no path, then returns an empty list
    """
    
    if start == goal:
        return [start]
        
    visited = {start}
    # Agenda is a list of lists; inner lists are different paths being followed
    agenda = [[start]]
    
    while True:
        path = agenda.pop(0)
        
        for dest in graph.get_connected_nodes(path[-1]):            
            # Skip nodes already visited
            if dest in visited:
                continue            
            # If goal is reached, return the path
            if dest == goal:
                return path + [goal]
            # Else add 'dest' to 'path' and put it at the end of the agenda
            else:
                visited.add(dest)
                
                '''
                Note that this is the only difference between dfs and bfs with
                the current implementation; dfs adds new paths to the beginning
                of the agenda, bfs to the end
                '''     
                agenda = agenda + [path + [dest]]

    # If goal node is never reached, return an empty list
    return []    
        

## Once you have completed the breadth-first search,
## this part should be very simple to complete.
def dfs(graph, start, goal, agenda = [], path = []):
    """
    Finds a path between start and goal node using depth-first search.

    Parameters:
        graph: Graph
            The graph on which to carry out the search
        start: string
            Node number at which to start
        goal: string
            Node number at which to end

    Returns:
        A list of nodes from start to goal using depth-first search,
        represented by a list of nodes (in strings), [n_1, n_2, ..., n_k]
        where there exists an edge from n_i to n_(i+1) in graph

        If there exists no path, then returns an empty list
    """   
    
    if start == goal:
        return [start]
        
    extended_list = {start}
    # Agenda is a list of lists; inner lists are different paths being followed
    agenda = [[start]]
    
    while True:
        path = agenda.pop(0)
        
        for dest in graph.get_connected_nodes(path[-1]):            
            # Skip nodes already visited
            if dest in extended_list:
                continue      
            # If goal is reached, return the path
            if dest == goal:
                return path + [goal]
            # Else add 'dest' to 'path' and put it at beginning of the agenda
            else:
                extended_list.add(dest)
                
                '''
                Note that this is the only difference between dfs and bfs with
                the current implementation; dfs adds new paths to the beginning
                of the agenda, bfs to the end
                '''               
                agenda = [path + [dest]] + agenda

    # If goal node is never reached, return an empty list
    return []    

       
## Now we're going to add some heuristics into the search.  
## Remember that hill-climbing is a modified version of depth-first search.
## Search direction should be towards lower heuristic values to the goal.
def hill_climbing(graph, start, goal):
    """
    Finds a path between start and goal node using hill-climbing search.

    Parameters:
        graph: Graph
            The graph on which to carry out the search
        start: string
            Node number at which to start
        goal: string
            Node number at which to end

    Returns:
        A list of nodes from start to goal using hill-climbing search,
        represented by a list of nodes (in strings), [n_1, n_2, ..., n_k]
        where there exists an edge from n_i to n_(i+1) in graph

        If there exists no path, then returns an empty list
    """   
    
    if start == goal:
        return [start]
        
    # Agenda is a list of lists; inner lists are different paths being followed
    agenda = [[start]]
    
    while True:
        heuristic_dict = {}
        path = agenda.pop(0)
        
        # Build dict potential nodes -> heuristic
        for dest in graph.get_connected_nodes(path[-1]):            
            if dest in path:
                continue      
            if dest == goal:
                return path + [goal]
            heuristic_dict[dest] = graph.get_heuristic(dest, goal)
            
        # Get list of potential nodes sorted by heuristic (high -> low)
        sorted_nodes = sorted(heuristic_dict, key = heuristic_dict.get,
                              reverse = True)
        # Add to agenda (note that lower heuristics end up first in the agenda)
        if sorted_nodes != []:
            for node in sorted_nodes:
                agenda = [path + [node]] + agenda
    
    # If goal node is never reached, return an empty list
    return []  


# NOTE: best first search is not part of this problem set, added to practice
def best_first(graph, start, goal):
    """
    Finds a path between start and goal node using best-first search.

    Parameters:
        graph: Graph
            The graph on which to carry out the search
        start: string
            Node number at which to start
        goal: string
            Node number at which to end

    Returns:
        A list of nodes from start to goal using best-first search,
        represented by a list of nodes (in strings), [n_1, n_2, ..., n_k]
        where there exists an edge from n_i to n_(i+1) in graph

        If there exists no path, then returns an empty list
    """   
    
    if start == goal:
        return [start]
        
    # Agenda is a list of lists; inner lists are different paths being followed
    agenda = [[start]]
    # Set of invalid paths to avoid ending up in local heuristic minima
    invalid_paths = []
    
    while True:
        # Build dictionary of index of path -> heuristic
        heuristic_dict = {}
        for i in range(len(agenda)):
                heuristic_dict[i] = graph.get_heuristic(agenda[i][-1], goal)
        # Get a indices in the agenda sorted by heurictic (low -> high)
        sorted_indices = sorted(heuristic_dict, key = heuristic_dict.get)
        # Build sorted agenda
        sorted_agenda = [agenda[i] for i in sorted_indices]
        agenda = sorted_agenda
        # Get path with minimum heuristic, i.e. 'closest to goal'
        path = agenda[0]
        node = path[-1]
        
        invalid_path = True
        for dest in graph.get_connected_nodes(node):                
            # If goal is reached, return the path
            if dest == goal:
                return path + [goal]
            # Skip nodes in path
            if dest in path:
                continue
            # Skip if it leads to a path already explored
            if path + [dest] in agenda:
                continue
            # Skip invalid paths
            if (path + [dest]) in invalid_paths:
                continue
            # Else add 'dest' to 'path' and the path back in the agenda
            else:
                '''
                Note that this is the only difference between dfs and bfs with
                the current implementation; dfs adds new paths to the beginning
                of the agenda, bfs to the end
                '''               
                agenda += [path + [dest]]
                invalid_path = False
                break
            
        # If this point is reached, no node gets to a better heuristic
        # and hence we are trapped in an infinite loop. This is an invalid 
        if invalid_path:
            invalid_paths.append(path)
            agenda.pop(0)

    # If goal node is never reached, return an empty list
    return []

## Now we're going to implement beam search, a variation on BFS
## that caps the amount of memory used to store paths.  Remember,
## we maintain only k candidate paths of length n in our agenda at any time.
## The k top candidates are to be determined using the 
## graph get_heuristic function, with lower values being better values.
def beam_search(graph, start, goal, beam_width):
    """
    Finds a path between start and goal node using beam search.

    Parameters:
        graph: Graph
            The graph on which to carry out the search
        start: string
            Node number at which to start
        goal: string
            Node number at which to end
        beam_width: integer
            Number of paths at each level added to agenda

    Returns:
        A list of nodes from start to goal using beam search,
        represented by a list of nodes (in strings), [n_1, n_2, ..., n_k]
        where there exists an edge from n_i to n_(i+1) in graph

        If there exists no path, then returns an empty list
    """
    
    if start == goal:
        return [start]
        
    # Agenda is a list of lists; inner lists are different paths being followed
    agenda = [[start]]
    
    current_length = 1
    while True:
        
        # Create a list of possible paths (as tuples so that they can be keys)
        possible_paths = []
        paths = [path for path in agenda if len(path) == current_length]
        if len(paths) == 0:
            break
        
        reached_nodes = []       
        for path in paths:
            for dest in graph.get_connected_nodes(path[-1]):            
                # Skip nodes already visited
                if dest in path:
                    continue   
                # Skip is node reached by previous path
                if dest in reached_nodes:
                    continue
                # If goal is reached, return the path
                if dest == goal:
                    return list(path) + [goal]
                # Else add 'dest' to 'path' and put it in the tuple
                else:
                    possible_paths.append((tuple(path) + (dest,)))
                    reached_nodes += [dest]
        
        # Add to the agenda the best 'beam_width' paths (lowest heuritic)
        heuristic_dict = {path: graph.get_heuristic(path[-1], goal) for path \
                          in possible_paths}
        new_paths = sorted(heuristic_dict, key=heuristic_dict.get)[:beam_width]
        for path in new_paths:
            agenda = [list(path)] + agenda
        
        current_length += 1

    # If goal node is never reached, return an empty list
    return []    


## Now we're going to try optimal search.  The previous searches haven't
## used edge distances in the calculation.

## This function takes in a graph and a list of node names, and returns
## the sum of edge lengths along the path -- the total distance in the path.
def path_length(graph, node_names):
    if not graph.is_valid_path(node_names):
        raise ValueError
    distance = 0
    for i in range(len(node_names) - 1):
        distance += graph.get_edge(node_names[i], node_names[i + 1]).length
    return distance


def branch_and_bound(graph, start, goal):
    """
    Finds a path between start and goal node using branch and bound search.

    Parameters:
        graph: Graph
            The graph on which to carry out the search
        start: string
            Node number at which to start
        goal: string
            Node number at which to end

    Returns:
        A list of nodes from start to goal using branch and bound,
        represented by a list of nodes (in strings), [n_1, n_2, ..., n_k]
        where there exists an edge from n_i to n_(i+1) in graph

        If there exists no path, then returns an empty list
    """
    
    if start == goal:
        return [start]
        
    # Agenda is a list of lists; inner lists are different paths being followed
    agenda = [[start]]
    
    while True:
             
        # Sort agenda
        dist_dict = {tuple(path): path_length(graph, path) for path in agenda}
        agenda = [list(el) for el in sorted(dist_dict, key = dist_dict.get)]
        
        # Conditions for optimal path to have been found:
        #    1 - Goal reached in a path
        #    2 - Length of all other paths longer
        for path in agenda:
            if path[-1] == goal and \
               path_length(graph, path) <= min(dist_dict.values()):
                   return path
    
        # Extend nodes of shortest path
        path = agenda.pop(0)
        for dest in graph.get_connected_nodes(path[-1]):            
            # Skip nodes already visited
            if dest in path:
                continue   
            else:
                agenda += [path + [dest]]

    # If goal node is never reached, return an empty list
    return []    
    

def a_star(graph, start, goal):
    """
    Finds a path between start and goal node using A* search.

    Parameters:
        graph: Graph
            The graph on which to carry out the search
        start: string
            Node number at which to start
        goal: string
            Node number at which to end

    Returns:
        A list of nodes from start to goal using A*,
        represented by a list of nodes (in strings), [n_1, n_2, ..., n_k]
        where there exists an edge from n_i to n_(i+1) in graph

        If there exists no path, then returns an empty list
    """
    
    if start == goal:
        return [start]
      
    # Agenda is a list of lists; inner lists are different paths being followed
    agenda = [[start]]
    extended_nodes = {start}
    
    while True:
        
        # Sort agenda
        dist_dict = {tuple(path): path_length(graph, path) + \
                     graph.get_heuristic(path[-1], goal) for path in agenda}
        agenda = [list(el) for el in sorted(dist_dict, key = dist_dict.get)]
        
        #if len(agenda) == 0:
            #break
        
        # Conditions for optimal path to have been found:
        #    1 - Goal reached in a path
        #    2 - Length of all other paths longer
        for path in agenda:
            if path[-1] == goal and \
               path_length(graph, path) <= min(dist_dict.values()):
                   return path
    
        # Extend nodes of shortest path
        path = agenda.pop(0)
        for dest in graph.get_connected_nodes(path[-1]):            
            # Skip nodes already visited
            if dest in path:
                continue
            # Skip node if it is in the extended list
            elif dest in extended_nodes:
                continue
            else:
                agenda += [path + [dest]]
                extended_nodes.add(path[-1])

    # If goal node is never reached, return an empty list
    return []  

# Copying test to try to understand why it doesn't pass
# Final outcome: Gave up without finding out, test might be wrongly set up?    
from graphs import *
import random
# ----------------------------------------------------------------------------
def exp_graph(depth):
    g = Graph(["1"])
    goal = 1
    for d in range(depth):
        nodeids = list(range(2**(d+1), 2**(d+2)))
        goal = random.choice(nodeids)
        for nodeid in nodeids:
            parent = nodeid/2 # intentional integer division
            g.add_edge(str(parent), str(nodeid), 1)
    best_path = [goal]
    while goal > 0:
        goal = goal/2 # intentional integer division
        best_path.append(goal)
    goal = best_path[0]

    for nodeid in range(1,2**(depth+1)):
        distance = 0
        shared_parent = nodeid
        while shared_parent not in best_path:
            distance += 1
            shared_parent = shared_parent / 2 # intentional integer division
        g.set_heuristic(str(nodeid), str(goal), distance+best_path.index(shared_parent))
    return g
    
# ----------------------------------------------------------------------------   
#a_star_test_5_graph = exp_graph(11)
#print(a_star_test_5_graph)
##print(a_star(NEWGRAPH1, 'F', 'G')) 
#print(a_star_test_5_graph.edges)
#print(a_star(a_star_test_5_graph, '1.0', list(a_star_test_5_graph.heuristic.keys())[0])) 

## It's useful to determine if a graph has a consistent and admissible
## heuristic.  You've seen graphs with heuristics that are
## admissible, but not consistent.  Have you seen any graphs that are
## consistent, but not admissible?

def is_admissible(graph, goal):
    queue_to_check = [[goal]]  
    while True:
        path = queue_to_check.pop(-1)
        if not graph.get_heuristic(path[0], goal) <= path_length(graph, path):
            return False
        # Keep extending backwards from the goal
        for node in graph.get_connected_nodes(path[0]):            
            # Skip nodes already visited
            if node in path:
                continue
            queue_to_check.append([node] + path)
            
        # Return true if everything has been positively checked
        if len(queue_to_check) == 0:
        
def is_consistent(graph, goal):
    for edge in graph.edges:
        if not edge.length >= abs(graph.get_heuristic(edge.node1, goal) - 
                                  graph.get_heuristic(edge.node2, goal)):
            return False
    return True

is_admissible(NEWGRAPH1, 'G')

HOW_MANY_HOURS_THIS_PSET_TOOK = '7'
WHAT_I_FOUND_INTERESTING = '''Tracking the agenda to see how it develops under 
                              different search methods'''
WHAT_I_FOUND_BORING = '''A couple of tests were yielding incorrect without 
                         saying why'''

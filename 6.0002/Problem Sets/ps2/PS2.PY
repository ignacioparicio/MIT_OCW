# 6.0002 Problem Set 5
# Graph optimization
# Name: Ignacio Paricio
# Collaborators: None
# Time: 5h

#
# Finding shortest paths through MIT buildings
#
import unittest
from copy import deepcopy
from graph import Digraph, Node, WeightedEdge

#
# Problem 2: Building up the Campus Map
#
# Problem 2a: Designing your graph
#
# What do the graph's nodes represent in this problem? What
# do the graph's edges represent? Where are the distances
# represented?
#
# Answer: Nodes represent different buildings, and they are referred to with
# strings representing the building number. Edges are possible links
# between buildings, and contain 2 parameters representing the source and the
# destination nodes and 2 more parameters as weights: the total travel
# distance and the outside travel distance.


# Problem 2b: Implementing load_map
def load_map(map_filename):
    """
    Parses the map file and constructs a directed graph

    Parameters:
        map_filename : name of the map file

    Assumes:
        Each entry in the map file consists of the following four positive
        integers, separated by a blank space:
            From To TotalDistance DistanceOutdoors
        e.g.
            32 76 54 23
        This entry would become an edge from 32 to 76.

    Returns:
        a Digraph representing the map
    """

    # TODO
    print("Loading map from file...")
    
    # Import content
    with open(map_filename, 'r') as f:
        content = f.readlines()
    # Delete line breaks from list
    content = [x.strip() for x in content] 
    
    # Create and load data into Digraph
    mit_map = Digraph()
    for el in content:
        el = el.split()
        src = Node(el[0])
        dest = Node(el[1])
        total_distance = el[2]
        outdoor_distance = el[3]        
        # Try to add both src and dest node in case they are not yet in Digraph
        try:
            mit_map.add_node(src)
        except:
            pass        
        try:
            mit_map.add_node(dest)
        except:
            pass
        
        # Add edge between the nodes
        mit_map.add_edge(WeightedEdge(src,
                                      dest,
                                      total_distance,
                                      outdoor_distance))

    return mit_map
    
# Problem 2c: Testing load_map
# Include the lines used to test load_map below, but comment them out
#print(load_map('test_load_map.txt'))





#
# Problem 3: Finding the Shorest Path using Optimized Search Method
#
# Problem 3a: Objective function
#
# What is the objective function for this problem? What are the constraints?
#
# Answer: Minimize the total distance travelled. Constraints: can only move
# between nodes connected by edges

# Problem 3b: Implement get_best_path
def get_best_path(digraph, start, end, path, max_dist_outdoors, best_dist,
                  best_path):
    """
    Finds the shortest path between buildings subject to constraints.

    Parameters:
        digraph: Digraph instance
            The graph on which to carry out the search
        start: string
            Building number at which to start
        end: string
            Building number at which to end
        path: list composed of [[list of strings], int, int]
            Represents the current path of nodes being traversed. Contains
            a list of node names, total distance traveled, and total
            distance outdoors.
        max_dist_outdoors: int
            Maximum distance spent outdoors on a path
        best_dist: int
            The smallest distance between the original start and end node
            for the initial problem that you are trying to solve
        best_path: list of strings
            The shortest path found so far between the original start
            and end node.

    Returns:
        A tuple with the shortest-path from start to end, represented by
        a list of building numbers (in strings), [n_1, n_2, ..., n_k],
        where there exists an edge from n_i to n_(i+1) in digraph,
        for all 1 <= i < k and the distance of that path.

        If there exists no path that satisfies max_total_dist and
        max_dist_outdoors constraints, then return None.
    """
    # TODO
    path[0] += [start]
    prev_dist = path[1]
    prev_dist_outdoors = path[2]
    
    if not digraph.has_node(Node(start)) or not digraph.has_node(Node(end)):
        raise NameError('Node(s) given not found!')
    
    # Base-case for the recursion: if node is end node, return current path        
    elif Node(start) == Node(end):
        return [start], path[1]
    
    # Recursive-case: pre-filter non-valid edges and keep digging depth-first
    for edge in digraph.get_edges_for_node(Node(start)):
        
        dest = edge.get_destination().get_name()
                     
        # Skip edge if it goes back to a node already visited
        if dest in path[0]:
            continue
        
        # path[1] and path[2] are 'restarted' to ensure proper edge evaluation
        path[1] = prev_dist + edge.get_total_distance()
        path[2] = prev_dist_outdoors + edge.get_outdoor_distance()
        
        # Skip edge if it would lead to sub-optimal result
        if path[1] > best_dist:
            continue
        
        # Skip edge if it would violate the 'max distance outdoors' constraint
        if path[2] > max_dist_outdoors:
            continue
                
        # Passing "dest node" as new start, using deepcopy to avoid 
        # modifying the path (mutable list) is other variable scopes
        newPath, newPath_dist = get_best_path(digraph,
                                              dest,
                                              end,
                                              deepcopy(path),
                                              max_dist_outdoors,
                                              best_dist,
                                              best_path)  
            
        if  newPath_dist < best_dist:
            best_path = [start] + newPath
            best_dist = newPath_dist
            
    return (best_path, best_dist)

# Problem 3c: Implement directed_dfs
def directed_dfs(digraph, start, end, max_total_dist, max_dist_outdoors):
    """
    Finds the shortest path from start to end using a directed depth-first
    search. The total distance traveled on the path must not
    exceed max_total_dist, and the distance spent outdoors on this path must
    not exceed max_dist_outdoors.

    Parameters:
        digraph: Digraph instance
            The graph on which to carry out the search
        start: string
            Building number at which to start
        end: string
            Building number at which to end
        max_total_dist: int
            Maximum total distance on a path
        max_dist_outdoors: int
            Maximum distance spent outdoors on a path

    Returns:
        The shortest-path from start to end, represented by
        a list of building numbers (in strings), [n_1, n_2, ..., n_k],
        where there exists an edge from n_i to n_(i+1) in digraph,
        for all 1 <= i < k

        If there exists no path that satisfies max_total_dist and
        max_dist_outdoors constraints, then raises a ValueError.
    """
    # TODO
    
    best_path = get_best_path(digraph, start, end, [[], 0, 0],
                              max_dist_outdoors, max_total_dist, None)

    if best_path[0] is None:
        raise ValueError('No path was found for the given input.')

    return best_path[0]

# Mini-tests Ignacio   
#print(directed_dfs(load_map('test_load_map.txt'), 'a', 'c', 1e4, 1e4)) 
#print(directed_dfs(load_map('mit_map.txt'), '32', '66', 1e4, 1e4))
#print(directed_dfs(load_map('mit_map.txt'), '8', '50', 1e4, 0))
        
# ================================================================
# Begin tests -- you do not need to modify anything below this line
# ================================================================

class Ps2Test(unittest.TestCase):
    LARGE_DIST = 99999

    def setUp(self):
        self.graph = load_map("mit_map.txt")

    def test_load_map_basic(self):
        self.assertTrue(isinstance(self.graph, Digraph))
        self.assertEqual(len(self.graph.nodes), 37)
        all_edges = []
        for _, edges in self.graph.edges.items():
            all_edges += edges  # edges must be dict of node -> list of edges
        all_edges = set(all_edges)
        self.assertEqual(len(all_edges), 129)

    def _print_path_description(self, start, end, total_dist, outdoor_dist):
        constraint = ""
        if outdoor_dist != Ps2Test.LARGE_DIST:
            constraint = "without walking more than {}m outdoors".format(
                outdoor_dist)
        if total_dist != Ps2Test.LARGE_DIST:
            if constraint:
                constraint += ' or {}m total'.format(total_dist)
            else:
                constraint = "without walking more than {}m total".format(
                    total_dist)

        print("------------------------")
        print("Shortest path from Building {} to {} {}".format(
            start, end, constraint))

    def _test_path(self,
                   expectedPath,
                   total_dist=LARGE_DIST,
                   outdoor_dist=LARGE_DIST):
        start, end = expectedPath[0], expectedPath[-1]
        self._print_path_description(start, end, total_dist, outdoor_dist)
        dfsPath = directed_dfs(self.graph, start, end, total_dist, outdoor_dist)
        print("Expected: ", expectedPath)
        print("DFS: ", dfsPath)
        self.assertEqual(expectedPath, dfsPath)

    def _test_impossible_path(self,
                              start,
                              end,
                              total_dist=LARGE_DIST,
                              outdoor_dist=LARGE_DIST):
        self._print_path_description(start, end, total_dist, outdoor_dist)
        with self.assertRaises(ValueError):
            directed_dfs(self.graph, start, end, total_dist, outdoor_dist)

    def test_path_one_step(self):
        self._test_path(expectedPath=['32', '56'])

    def test_path_no_outdoors(self):
        self._test_path(
            expectedPath=['32', '36', '26', '16', '56'], outdoor_dist=0)

    def test_path_multi_step(self):
        self._test_path(expectedPath=['2', '3', '7', '9'])

    def test_path_multi_step_no_outdoors(self):
        self._test_path(
            expectedPath=['2', '4', '10', '13', '9'], outdoor_dist=0)

    def test_path_multi_step2(self):
        self._test_path(expectedPath=['1', '4', '12', '32'])

    def test_path_multi_step_no_outdoors2(self):
        self._test_path(
            expectedPath=['1', '3', '10', '4', '12', '24', '34', '36', '32'],
            outdoor_dist=0)

    def test_impossible_path1(self):
        self._test_impossible_path('8', '50', outdoor_dist=0)

    def test_impossible_path2(self):
        self._test_impossible_path('10', '32', total_dist=100)


if __name__ == "__main__":
    unittest.main()

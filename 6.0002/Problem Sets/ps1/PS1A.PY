###########################
# 6.0002 Problem Set 1a: Space Cows 
# Name:
# Collaborators:
# Time:

from ps1_partition import get_partitions
import time
from matplotlib import pyplot as plt
from matplotlib import style
style.use('fivethirtyeight')
import numpy as np

#================================
# Part A: Transporting Space Cows
#================================

# Problem 1
def load_cows(filename):
    """
    Read the contents of the given file.  Assumes the file contents contain
    data in the form of comma-separated cow name, weight pairs, and return a
    dictionary containing cow names as keys and corresponding weights as values.

    Parameters:
    filename - the name of the data file as a string

    Returns:
    a dictionary of cow name (string), weight (int) pairs
    """
    inFile = open(filename, 'r')
    cows_dict = {}
    for line in inFile:
        cows_dict[line.split(",")[0]] = int(line.split(",")[1].replace('\n',''))
    return cows_dict
    

# Problem 2
def greedy_cow_transport(cows,limit=10):
    """
    Uses a greedy heuristic to determine an allocation of cows that attempts to
    minimize the number of spaceship trips needed to transport all the cows. The
    returned allocation of cows may or may not be optimal.
    The greedy heuristic should follow the following method:

    1. As long as the current trip can fit another cow, add the largest cow that will fit
        to the trip
    2. Once the trip is full, begin a new trip to transport the remaining cows

    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    cows_dict = cows.copy()
    greedy_trips = []
    
    while len(cows_dict) > 0:
        
        space_available = limit
        cows_to_take = []
        
        for weight in sorted(cows_dict.values(), reverse = True):
            
            if weight <= space_available:
                space_available -= weight               
                # Identify and take cow based on weight (random if multiple)
                for cow in cows_dict:
                    if cows_dict[cow] == weight:
                        cows_to_take.append(cow)
                        cows_dict.pop(cow)
                        # Break to avoid deleting multiple cows if equal weight
                        break
                    
            # Handles case in which each item remaining > limit
            elif weight > limit:
                return greedy_trips
        
        greedy_trips.append(cows_to_take)
    
    # Return 'None' if no possible combinations whatsoever
    if len(greedy_trips) == 0:
        greedy_trips = None    
    return greedy_trips

# Problem 3
def brute_force_cow_transport(cows,limit=10):
    """
    Finds the allocation of cows that minimizes the number of spaceship trips
    via brute force.  The brute force algorithm should follow the following method:

    1. Enumerate all possible ways that the cows can be divided into separate trips 
        Use the given get_partitions function in ps1_partition.py to help you!
    2. Select the allocation that minimizes the number of trips without making any trip
        that does not obey the weight limitation
            
    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    valid_trip_combs = get_valid_trip_combinations(cows, limit)
    required_number_trips = 999999999999
    optimal_trips = None
    # Run through all potential trip combs. to get the minimum number required
    for comb in valid_trip_combs:
        if len(comb) < required_number_trips:
            required_number_trips = len(comb)
            optimal_trips = comb
    return optimal_trips           


def get_valid_trip_combinations(cows, limit):
    """
    Returns a list of lists with all potential valid trips to transport 
    a given set of cows. Overall list contains different possible trip
    combinations. Inner lists contain the detail of each trip.
    
    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    """
    valid_trip_combs = []
    for partition in get_partitions(cows.keys()):
        # get_partitions will return a list of lists
        # Each of the 'inner' lists contains the cow names for potential trips
        # Check that none of the trips exceeds the limit, otherwise discard
        valid_trip = True
        for trip in partition:
            total_space_used = 0
            for cow in trip:
                total_space_used += cows[cow]      
                # Break and move to next partition if any trip exceeds limit
                if total_space_used > limit:
                    valid_trip = False
                    # Don't need to assess the rest of the cows
                    break
            if not valid_trip:
                # Don't need to assess the rest of the trips in the partition
                break
        if valid_trip:
            valid_trip_combs.append(partition)
    return valid_trip_combs
    

        
# Problem 4
def compare_cow_transport_algorithms(cows, limit, n, toPrint = False):
    """
    Using the data from ps1_cow_data.txt and the specified weight limit, run your
    greedy_cow_transport and brute_force_cow_transport functions here. Use the
    default weight limits of 10 for both greedy_cow_transport and
    brute_force_cow_transport.
    
    Print out the number of trips returned by each method, and how long each
    method takes to run in seconds.

    Returns:
    Does not return anything.
    """
    sample_size = 1
    execution_time_brute_force = []
    execution_time_greedy = []
    
    for i in range(n):
        # Test brute_force
        start = time.time()
        brute_force_cow_transport(cows,limit)
        end = time.time()
        execution_time_brute_force.append(end - start)
        
        # Test brute_force
        start = time.time()
        greedy_cow_transport(cows,limit)
        end = time.time()
        execution_time_greedy.append(end - start)
    
    if toPrint:
        print('\n\nBrute force\n', '-' * 40,
              '\nAverage time taken: ',
               round(np.average(execution_time_brute_force), 4),
              '\nSt. dev.: ', round(np.std(execution_time_brute_force), 4),
              '\nList of times: ', execution_time_brute_force)
    
        print('\n\nGreedy\n', '-' * 40,
              '\nAverage time taken: ',
               round(np.average(execution_time_greedy), 4),
              '\nSt. dev.: ', round(np.std(execution_time_greedy), 4),
              '\nList of times: ', execution_time_greedy)
        
        





'''Tests Ignacio'''
# Compare algorithm efficiency 
cows = load_cows('ps1_cow_data.txt')
n = 10
#compare_cow_transport_algorithms (cows, limit, n, True)


#Simple test for single limit
#limit = 10
#print(cows)
#print('\n\nBrute force\n', '-' * 40,
#      '\nTrips required: ', len(brute_force_cow_transport(cows, limit)),
#      '\nTrips definition: ', brute_force_cow_transport(cows, limit))
#
#print('\n\nGreedy\n', '-' * 40,
#      '\nTrips required: ', len(greedy_cow_transport(cows, limit)),
#      '\nTrips definition: ', greedy_cow_transport(cows, limit))

      
def multi_tester(cows, limits):
    number_trips_brute_force = []
    number_trips_greedy = []
    limits_1 = []
    limits_2 = []
    
    for limit in limits:
        limits_1.append(limit - 0.15)
        limits_2.append(limit + 0.15)
        number_trips_brute_force.append(len(brute_force_cow_transport(cows, limit)))
        number_trips_greedy.append(len(greedy_cow_transport(cows, limit)))
        
    plt.bar(limits_1,
            number_trips_brute_force,
            label = 'Brute force',
            color = 'b',
            width = 0.3,
            align = 'center')
    plt.bar(limits_2,
            number_trips_greedy,
            label = 'Greedy',
            color = 'r',
            width = 0.3,
            align = 'center')
    plt.xlabel('Limit')
    plt.ylabel('Number of trips')
    plt.legend()
    plt.show()
    return None

# Test for multiple limits, plot results to bart chart
limits = [x for x in range(9,20)]
multi_tester(cows, limits)
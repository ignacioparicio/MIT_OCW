###########################
# 6.0002 Problem Set 1b: Space Change
# Name:
# Collaborators:
# Time:
# Author: charz, cdenise

#================================
# Part B: Golden Eggs
#================================

# Problem 1
def dp_make_weight(egg_weights, target_weight, memo = {}):
    """
    Find number of eggs to bring back, using the smallest number of eggs. Assumes there is
    an infinite supply of eggs of each weight, and there is always a egg of value 1.
    
    Parameters:
    egg_weights - tuple of integers, available egg weights sorted from smallest to largest value (1 = d1 < d2 < ... < dk)
    target_weight - int, amount of weight we want to find eggs to fit
    memo - dictionary, OPTIONAL parameter for memoization (you may not need to use this parameter depending on your implementation). Ignacio: using this argument as a dictionary with target weights as keys and a list containing
    all egg weights optimal for that target weight as values
    
    Returns: int, smallest number of eggs needed to make target weight
    """
# Note: this solution uses recursive programming but is actually not making
# use of dynamic programming. The logic in the while loop should be replaced
# by something more stupid that considers all possible eggs fitting and not
# only the biggest one. That way the 'memo' would be used!
    # I can use dynamic programming for cases in which the available weight
    # is something already seen
    min_eggs = target_weight
    
    if target_weight in memo:
        print('Memo call!')
        return memo[target_weight]
             
    elif target_weight == 1:
        memo[target_weight] = [target_weight]
        return memo[target_weight]
        
    elif target_weight == 0 or len(egg_weights) == 0:
        list_of_eggs = []
      
    for egg in egg_weights:
        if egg < target_weight:
            list_of_eggs = []
            list_of_eggs += [egg] + dp_make_weight(egg_weights, target_weight - egg, memo)
            if len(list_of_eggs) <= min_eggs:
                min_eggs = len(list_of_eggs)
                memo[target_weight] = list_of_eggs
    return list_of_eggs

# EXAMPLE TESTING CODE, feel free to add more if you'd like
if __name__ == '__main__':
    egg_weights = (1, 5, 10, 25, 27, 33, 35, 85)
#    egg_weights = (1, 5)
    n = 705
    print("Egg weights = (1, 5, 10, 25)")
    print("n = 99")
    print("Expected ouput: 9 (3 * 25 + 2 * 10 + 4 * 1 = 99)")
    listEggs = dp_make_weight(egg_weights, n)
    print("Actual output:", len(listEggs))
    print('List of eggs: \n', listEggs)
    print()
    
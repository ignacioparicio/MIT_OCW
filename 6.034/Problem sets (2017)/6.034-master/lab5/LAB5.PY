from classify import *
import math

### Data sets for the lab
## You will be classifying data from these sets.
senate_people = read_congress_data('S110.ord')
senate_votes = read_vote_data('S110desc.csv')

house_people = read_congress_data('H110.ord')
house_votes = read_vote_data('H110desc.csv')

last_senate_people = read_congress_data('S109.ord')
last_senate_votes = read_vote_data('S109desc.csv')


### Part 1: Nearest Neighbors
## An example of evaluating a nearest-neighbors classifier.
senate_group1, senate_group2 = crosscheck_groups(senate_people)
#evaluate(nearest_neighbors(hamming_distance, 1), senate_group1, senate_group2, verbose=1)

## Write the euclidean_distance function.
## This function should take two lists of integers and
## find the Euclidean distance between them.
## See 'hamming_distance()' in classify.py for an example that
## computes Hamming distances.

def euclidean_distance(list1, list2):
    dist = 0

    for i1, i2 in zip(list1, list2):
        dist += (i1 - i2)**2

    return dist**0.5

#Once you have implemented euclidean_distance, you can check the results:
#evaluate(nearest_neighbors(euclidean_distance, 1), senate_group1, senate_group2)

## By changing the parameters you used, you can get a classifier factory that
## deals better with independents. Make a classifier that makes at most 3
## errors on the Senate.

my_classifier = nearest_neighbors(euclidean_distance, 5)
# evaluate(my_classifier, senate_group1, senate_group2, verbose=1)

### Part 2: ID Trees
# print CongressIDTree(senate_people, senate_votes, homogeneous_disorder)

## Now write an information_disorder function to replace homogeneous_disorder,
## which should lead to simpler trees.

def information_disorder(yes, no):
    from math import log

    # For democrat, republican, independent
    def disorder(branch):
        total = 0
        for unique in set(branch):
            nbc = float(branch.count(unique))
            nb = float(len(branch))
            ratio = nbc/nb
            total += -ratio * log(ratio, 2)
        return total

    floaty = float(len(yes))
    floatn = float(len(no))
    yn = floaty + floatn

    yes_branch_disorder = floaty/yn * disorder(yes)
    no_branch_disorder = floatn/yn * disorder(no)

    average_disorder = yes_branch_disorder + no_branch_disorder

    return average_disorder



# print CongressIDTree(senate_people, senate_votes, information_disorder)
# evaluate(idtree_maker(senate_votes, homogeneous_disorder), senate_group1, senate_group2)

## Now try it on the House of Representatives. However, do it over a data set
## that only includes the most recent n votes, to show that it is possible to
## classify politicians without ludicrous amounts of information.

def limited_house_classifier(house_people, house_votes, n, verbose = False):
    house_limited, house_limited_votes = limit_votes(house_people,
    house_votes, n)
    house_limited_group1, house_limited_group2 = crosscheck_groups(house_limited)

    if verbose:
        print "ID tree for first group:"
        print CongressIDTree(house_limited_group1, house_limited_votes,
                             information_disorder)
        print
        print "ID tree for second group:"
        print CongressIDTree(house_limited_group2, house_limited_votes,
                             information_disorder)
        print

    return evaluate(idtree_maker(house_limited_votes, information_disorder),
                    house_limited_group1, house_limited_group2)


## Find a value of n that classifies at least 430 representatives correctly.
## Hint: It's not 10.
N_1 = 50
rep_classified = limited_house_classifier(house_people, house_votes, N_1)

## Find a value of n that classifies at least 90 senators correctly.
N_2 = 70
senator_classified = limited_house_classifier(senate_people, senate_votes, N_2)

## Now, find a value of n that classifies at least 95 of last year's senators correctly.
N_3 = 23
old_senator_classified = limited_house_classifier(last_senate_people, last_senate_votes, N_3)
print old_senator_classified


## The standard survey questions.
NAME = 'Laser Nite'
COLLABORATORS = 'None'
HOW_MANY_HOURS_THIS_LAB_TOOK = 3
WHAT_I_FOUND_INTERESTING = 'information disorder and k-nearest neighbors algorithim'
WHAT_I_FOUND_BORING = 'none'
SUGGESTIONS = 'None'


## This function is used by the tester; please don't modify it!
def eval_test(eval_fn, group1, group2, verbose = 0):
    """ Find eval_fn in globals(), then execute evaluate() on it """
    # Only allow known-safe eval_fn's
    if eval_fn in [ 'my_classifier' ]:
        return evaluate(globals()[eval_fn], group1, group2, verbose)
    else:
        raise Exception, "Error: Tester tried to use an invalid evaluation function: '%s'" % eval_fn

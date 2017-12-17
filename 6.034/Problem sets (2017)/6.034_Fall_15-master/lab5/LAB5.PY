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
    j = 0
    for item1, item2 in zip(list1, list2):
        j += (item1-item2)**2
    j = j**.5
    return j

#evaluate(nearest_neighbors(euclidean_distance, 1), senate_group1, senate_group2, verbose=1)

## By changing the parameters you used, you can get a classifier factory that
## deals better with independents. Make a classifier that makes at most 3
## errors on the Senate.

my_classifier = nearest_neighbors(euclidean_distance,5)
#evaluate(my_classifier, senate_group1, senate_group2, verbose=1)

### Part 2: ID Trees
#print CongressIDTree(senate_people, senate_votes, homogeneous_disorder)

## Now write an information_disorder function to replace homogeneous_disorder,
## which should lead to simpler trees.

def information_disorder(group1, group2):
    nt = len(group1) + len(group2)
    n1dem = 0.0
    n1rep = 0.0
    n2dem = 0.0
    n2rep = 0.0
    x = 0.0
    y = 0.0
    for i in group1:
        if i == "Democrat":
            n1dem += 1
        if i == "Republican":
            n1rep += 1
    for i in group2:
        if i == "Democrat":
            n2dem += 1
        if i == "Republican":
            n2rep += 1
    if n1dem > 0.0:
        x += (-n1dem) * math.log(n1dem/(n1dem+n1rep),2)
    if n1rep > 0.0:
        x += (-n1rep) * math.log(n1rep/(n1dem+n1rep),2)
    if n2dem > 0.0:
        y += (-n2dem) * math.log(n2dem/(n2dem+n2rep),2)
    if n2rep > 0.0:
        y += (-n2rep) * math.log(n2rep/(n2rep+n2dem),2)
    return (x+y)/nt
print information_disorder(["Democrat", "Republican"], ["Republican", "Democrat"])
#print CongressIDTree(senate_people, senate_votes, information_disorder)
#evaluate(idtree_maker(senate_votes, homogeneous_disorder), senate_group1, senate_group2)

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
N_1=44
rep_classified = limited_house_classifier(house_people, house_votes, N_1)

## Find a value of n that classifies at least 90 senators correctly.
N_2=67
senator_classified = limited_house_classifier(senate_people, senate_votes, N_2)

## Now, find a value of n that classifies at least 95 of last year's senators correctly.
N_3=23
old_senator_classified = limited_house_classifier(last_senate_people, last_senate_votes, N_3)

## The standard survey questions.
NAME = "Sze Nga Wong"
COLLABORATORS = ""
HOW_MANY_HOURS_THIS_LAB_TOOK = 7
WHAT_I_FOUND_INTERESTING = "The idea of applying ID trees on Senate is interesting."
WHAT_I_FOUND_BORING = "The lab instruction is long and wordy."
SUGGESTIONS = ""


## This function is used by the tester; please don't modify it!
def eval_test(eval_fn, group1, group2, verbose = 0):
    """ Find eval_fn in globals(), then execute evaluate() on it """
    # Only allow known-safe eval_fn's
    if eval_fn in [ 'my_classifier' ]:
        return evaluate(globals()[eval_fn], group1, group2, verbose)
    else:
        raise Exception, "Error: Tester tried to use an invalid evaluation function: '%s'" % eval_fn

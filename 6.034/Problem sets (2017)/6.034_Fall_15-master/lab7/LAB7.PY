# 6.034 Lab 7 2015: Boosting (Adaboost)

from math import log as ln
INF = float('inf')

# Helper function for pick_best_classifier and adaboost
def fix_roundoff_error(inp, n=15):
    """inp can be a number, a list of numbers, or a dict whose values are numbers.
    * If inp is a number: Rounds the number to the nth decimal digit to reduce
        previous Python roundoff error.  Returns a float.
    * If inp is a list of numbers: Rounds each number as above.  Does not modify
        the original list.
    * If inp is a dictionary whose values are numbers: Rounds each value as
        above.  Does not modify the original dictionary."""
    fix_val = lambda val: round(abs(val),n)*[-1,1][val>=0]
    if isinstance(inp, list): return map(fix_val, inp)
    if isinstance(inp, dict): return {key: fix_val(inp[key]) for key in inp}
    return fix_val(inp)


#### BOOSTING (ADABOOST) #######################################################

def initialize_weights(training_points):
    """Assigns every training point a weight equal to 1/N, where N is the number
    of training points.  Returns a dictionary mapping points to weights."""
    d = {}
    n = len(training_points)
    for i in training_points:
        d[i] = 1.0/n
    return d

def calculate_error_rates(point_to_weight, classifier_to_misclassified):
    """Given a dictionary mapping training points to their weights, and another
    dictionary mapping classifiers to the training points they misclassify,
    returns a dictionary mapping classifiers to their error rates."""
    d = {}
    for i in classifier_to_misclassified:
        misclassified_i = classifier_to_misclassified[i]
        temp = 0
        for j in misclassified_i:
            temp += point_to_weight[j]
        d[i] = temp
    return d

def pick_best_classifier(classifier_to_error_rate, use_smallest_error=True):
    """Given a dictionary mapping classifiers to their error rates, returns the
    best* classifier.  Best* means 'smallest error rate' if use_smallest_error
    is True, otherwise 'error rate furthest from 1/2'."""
    p = sorted(classifier_to_error_rate,key=str.lower)
    m = 1.0
    best = None
    if use_smallest_error:
        for i in p:
            if fix_roundoff_error(classifier_to_error_rate[i]) < fix_roundoff_error(m):
                m = fix_roundoff_error(classifier_to_error_rate[i])
                best = i
    else:
        m=0.0
        for i in p:
            if fix_roundoff_error(abs(classifier_to_error_rate[i] - .5)) > fix_roundoff_error(m):
                m = fix_roundoff_error(abs(classifier_to_error_rate[i] - .5))
                best = i
    return best

def calculate_voting_power(error_rate):
    """Given a classifier's error rate (a number), returns the voting power
    (aka alpha, or coefficient) for that classifier."""
    if error_rate == 0:
        return INF
    if float(error_rate) == 1.0:
        return -INF
    return .5 * ln((1-error_rate)/error_rate)

def is_good_enough(H, training_points, classifier_to_misclassified,
                   mistake_tolerance=0):
    """Given an overall classifier H, a list of all training points, a
    dictionary mapping classifiers to the training points they misclassify, and
    a mistake tolerance (the maximum number of allowed misclassifications),
    returns False if H misclassifies more points than the tolerance allows,
    otherwise True.  H is represented as a list of (classifier, voting_power)
    tuples."""
    amt_misclassified = 0
    for tp in training_points:
        correct = 0
        false = 0
        for (classifier,vp)in H:
            if tp in classifier_to_misclassified[classifier]:
                false += vp
            else:
                correct += vp
        if false >= correct:
            amt_misclassified += 1
    if amt_misclassified <= mistake_tolerance:
        return True
    return False

def update_weights(point_to_weight, misclassified_points, error_rate):
    """Given a dictionary mapping training points to their old weights, a list
    of training points misclassified by the current weak classifier, and the
    error rate of the current weak classifier, returns a dictionary mapping
    training points to their new weights.  This function is allowed (but not
    required) to modify the input dictionary point_to_weight."""
    for i in point_to_weight:
        if i in misclassified_points:
            point_to_weight[i] *= .5/error_rate
        else:
            point_to_weight[i] *= .5/(1-error_rate)
    return point_to_weight

def adaboost(training_points, classifier_to_misclassified,
             use_smallest_error=True, mistake_tolerance=0, max_num_rounds=INF):
    """Performs the Adaboost algorithm for up to max_num_rounds rounds.
    Returns the resulting overall classifier H, represented as a list of
    (classifier, voting_power) tuples."""
    point_to_weight = initialize_weights(training_points)
    H = []
    while max_num_rounds > 0:
        max_num_rounds -= 1
        classifier_to_error_rate = calculate_error_rates(point_to_weight,classifier_to_misclassified)
        best_classifier = pick_best_classifier(classifier_to_error_rate,use_smallest_error)
        voting_power = calculate_voting_power(classifier_to_error_rate[best_classifier])
        misclassified_points = classifier_to_misclassified[best_classifier]
        error_rate = classifier_to_error_rate[best_classifier]
        point_to_weight = update_weights(point_to_weight,misclassified_points,error_rate)
        if is_good_enough(H,training_points,classifier_to_misclassified,mistake_tolerance):
            return H
        if fix_roundoff_error(error_rate - .5) == fix_roundoff_error(0):
            return H
        H.append((best_classifier,voting_power))
    return H



#### SURVEY ####################################################################

NAME = "Sze Nga Wong"
COLLABORATORS = ""
HOW_MANY_HOURS_THIS_LAB_TOOK = 5
WHAT_I_FOUND_INTERESTING = ""
WHAT_I_FOUND_BORING = ""
SUGGESTIONS = None

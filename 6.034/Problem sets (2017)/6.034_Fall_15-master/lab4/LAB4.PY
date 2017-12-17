from constraint_api import *
from test_problems import get_pokemon_problem

#### PART 1: WRITE A DEPTH-FIRST SEARCH CONSTRAINT SOLVER

def has_empty_domains(csp) :
    "Returns True if the problem has one or more empty domains, otherwise False"
    k = csp.domains
    for i in k:
        if len(k[i]) == 0:
            return True
    return False

def check_all_constraints(csp) :
    """Return False if the problem's assigned values violate some constraint,
    otherwise True"""
    k = csp.constraints
    m = csp.assigned_values
    for i in k:
        if ((i.var1 in m) and (i.var2 in m)):
            if i.check(m[i.var1],m[i.var2]) == False:
                return False
    return True

def solve_constraint_dfs(problem):
    agenda = [problem]
    exten = 0
    while (len(agenda) != 0):
        k = agenda.pop(0)
        exten += 1
        if not has_empty_domains(k):
            if check_all_constraints(k):
                m = k.unassigned_vars
                if len(m) == 0:
                    return (k.assigned_values,exten)
                x = k.pop_next_unassigned_var()
                f = []
                for i in k.get_domain(x):
                    k_new = k.copy()
                    k_new.set_assigned_value(x,i)
                    f.append(k_new)
                agenda = f + agenda
    return (None,exten)


#### PART 2: DOMAIN REDUCTION BEFORE SEARCH

def eliminate_from_neighbors(csp, var) :
    x = csp.constraints_between(None,var)
    reduced = []
    for i in x:
        domaincopy = csp.domains[i.var1][:]
        for k in domaincopy:
            po = False
            for j in csp.domains[var]:
                po = (po or i.check(k,j))
            if po == False:
                csp.eliminate(i.var1,k)
                if len(csp.domains[i.var1]) == 0:
                    return None
                if i.var1 not in reduced:
                    reduced.append(i.var1)
    reduced.sort()
    return reduced

def domain_reduction(csp, queue=None) :
    """Uses constraints to reduce domains, modifying the original csp.
    If queue is None, initializes propagation queue by adding all variables in
    their default order.  Returns a list of all variables that were dequeued,
    in the order they were removed from the queue.  Variables may appear in the
    list multiple times.
    If a domain is reduced to size 0, quits immediately and returns None."""
    if queue == None:
        queue = list(csp.get_all_variables())
    result = []
    while len(queue) != 0:
        first = queue.pop(0)
        result.append(first)
        reduced = eliminate_from_neighbors(csp,first)
        if reduced == None:
            return None
        #if len(reduced) > 0:
        for i in reduced:
            if i not in queue:
                queue.append(i)
        #queue.sort()
    return result

# QUESTION 1: How many extensions does it take to solve the Pokemon problem
#    with dfs if you DON'T use domain reduction before solving it?

# Hint: Use get_pokemon_problem() to get a new copy of the Pokemon problem
#    each time you want to solve it with a different search method.
k = get_pokemon_problem()
ANSWER_1 = solve_constraint_dfs(k)[1]

# QUESTION 2: How many extensions does it take to solve the Pokemon problem
#    with dfs if you DO use domain reduction before solving it?
k = get_pokemon_problem()
domain_reduction(k)
ANSWER_2 = solve_constraint_dfs(k)[1]


#### PART 3: PROPAGATION THROUGH REDUCED DOMAINS

def solve_constraint_propagate_reduced_domains(problem) :
    """Solves the problem using depth-first search with forward checking and
    propagation through all reduced domains.  Same return type as
    solve_constraint_dfs."""
    agenda = [problem]
    exten = 0
    while (len(agenda) != 0):
        k = agenda.pop(0)
        exten += 1
        if not has_empty_domains(k):
            if check_all_constraints(k):
                m = k.unassigned_vars
                if len(m) == 0:
                    return (k.assigned_values,exten)
                x = k.pop_next_unassigned_var()
                f = []
                for i in k.get_domain(x):
                    k_new = k.copy()
                    k_new.set_assigned_value(x,i)
                    domain_reduction(k_new,[x])
                    f.append(k_new)
                agenda = f + agenda
    return (None,exten)

# QUESTION 3: How many extensions does it take to solve the Pokemon problem
#    with propagation through reduced domains? (Don't use domain reduction
#    before solving it.)
k = get_pokemon_problem()
ANSWER_3 = solve_constraint_propagate_reduced_domains(k)[1]


#### PART 4: PROPAGATION THROUGH SINGLETON DOMAINS

def domain_reduction_singleton_domains(csp, queue=None) :
    """Uses constraints to reduce domains, modifying the original csp.
    Only propagates through singleton domains.
    Same return type as domain_reduction."""
    if queue == None:
        queue = csp.get_all_variables()
    result = []
    while len(queue) != 0:
        first = queue.pop(0)
        result.append(first)
        reduced = eliminate_from_neighbors(csp,first)
        if reduced == None:
            return None
        if len(reduced) > 0:
            for i in reduced:
                if i not in queue:
                    if len(csp.get_domain(i)) == 1:
                        queue.append(i)
        queue.sort()
    return result

def solve_constraint_propagate_singleton_domains(problem) :
    """Solves the problem using depth-first search with forward checking and
    propagation through singleton domains.  Same return type as
    solve_constraint_dfs."""
    agenda = [problem]
    exten = 0
    while (len(agenda) != 0):
        k = agenda.pop(0)
        exten += 1
        if not has_empty_domains(k):
            if check_all_constraints(k):
                m = k.unassigned_vars
                if len(m) == 0:
                    return (k.assigned_values,exten)
                x = k.pop_next_unassigned_var()
                f = []
                for i in k.get_domain(x):
                    k_new = k.copy()
                    k_new.set_assigned_value(x,i)
                    domain_reduction_singleton_domains(k_new,[x])
                    f.append(k_new)
                agenda = f + agenda
    return (None,exten)

# QUESTION 4: How many extensions does it take to solve the Pokemon problem
#    with propagation through singleton domains? (Don't use domain reduction
#    before solving it.)
k = get_pokemon_problem()
ANSWER_4 = solve_constraint_propagate_singleton_domains(k)[1]


#### PART 5: FORWARD CHECKING

def propagate(enqueue_condition_fn, csp, queue=None) :
    """Uses constraints to reduce domains, modifying the original csp.
    Uses enqueue_condition_fn to determine whether to enqueue a variable whose
    domain has been reduced.  Same return type as domain_reduction."""
    if queue == None:
        queue = list(csp.get_all_variables())
    result = []
    while len(queue) != 0:
        first = queue.pop(0)
        result.append(first)
        reduced = eliminate_from_neighbors(csp,first)
        if reduced == None:
            return None
        #if len(reduced) > 0:
        for i in reduced:
            if i not in queue:
                if enqueue_condition_fn(csp,i):
                    queue.append(i)
        #queue.sort()
    return result


    if queue == None:
        queue = list(csp.get_all_variables())
    result = []
    while len(queue) != 0:
        first = queue.pop(0)
        result.append(first)
        reduced = eliminate_from_neighbors(csp,first)
        if reduced == None:
            return None
        #if len(reduced) > 0:
        for i in reduced:
            if i not in queue:
                queue.append(i)
        #queue.sort()
    return result
def condition_domain_reduction(csp, var) :
    """Returns True if var should be enqueued under the all-reduced-domains
    condition, otherwise False"""
    return True

def condition_singleton(csp, var) :
    """Returns True if var should be enqueued under the singleton-domains
    condition, otherwise False"""
    if len(csp.get_domain(var)) == 1:
        return True
    return False

def condition_forward_checking(csp, var) :
    """Returns True if var should be enqueued under the forward-checking
    condition, otherwise False"""
    return False


#### PART 6: GENERIC CSP SOLVER

def solve_constraint_generic(problem, enqueue_condition=None) :
    """Solves the problem, calling propagate with the specified enqueue
    condition (a function).  If enqueue_condition is None, uses DFS only.
    Same return type as solve_constraint_dfs."""
    agenda = [problem]
    exten = 0
    while (len(agenda) != 0):
        k = agenda.pop(0)
        exten += 1
        if not has_empty_domains(k):
            if check_all_constraints(k):
                m = k.unassigned_vars
                if len(m) == 0:
                    return (k.assigned_values,exten)
                x = k.pop_next_unassigned_var()
                f = []
                for i in k.get_domain(x):
                    k_new = k.copy()
                    k_new.set_assigned_value(x,i)
                    if enqueue_condition != None:                       
                        propagate(enqueue_condition,k_new,[x])
                    f.append(k_new)
                agenda = f + agenda
    return (None,exten)

# QUESTION 5: How many extensions does it take to solve the Pokemon problem
#    with DFS and forward checking, but no propagation? (Don't use domain
#    reduction before solving it.)
k = get_pokemon_problem()
ANSWER_5 = solve_constraint_generic(k,condition_forward_checking)[1]


#### PART 7: DEFINING CUSTOM CONSTRAINTS

def constraint_adjacent(m, n) :
    """Returns True if m and n are adjacent, otherwise False.
    Assume m and n are ints."""
    if (m - n == 1) or (n - m == 1):
        return True
    return False

def constraint_not_adjacent(m, n) :
    """Returns True if m and n are NOT adjacent, otherwise False.
    Assume m and n are ints."""
    return not constraint_adjacent(m,n)

def constraint_different(m,n):
    if m != n:
        return True
    return False

def all_different(variables) :
    """Returns a list of constraints, with one difference constraint between
    each pair of variables."""
    l = len(variables)
    li = []
    for i in range(l):
        for j in range(i+1,l):
            li.append(Constraint(variables[i],variables[j],constraint_different))
    return li


#### PART 8: MOOSE PROBLEM (OPTIONAL)

moose_problem = ConstraintSatisfactionProblem(["You", "Moose", "McCain",
                                               "Palin", "Obama", "Biden"])

# Add domains and constraints to your moose_problem here:


# To test your moose_problem AFTER implementing all the solve_constraint
# methods above, change TEST_MOOSE_PROBLEM to True:
TEST_MOOSE_PROBLEM = False


#### SURVEY ###################################################

NAME = "Sze Nga Wong"
COLLABORATORS = ""
HOW_MANY_HOURS_THIS_LAB_TOOK = 10
WHAT_I_FOUND_INTERESTING = "N/A"
WHAT_I_FOUND_BORING = "This lab is too tedious."
SUGGESTIONS = None


###########################################################
### Ignore everything below this line; for testing only ###
###########################################################

if TEST_MOOSE_PROBLEM:
    # These lines are used in the local tester iff TEST_MOOSE_PROBLEM is True
    moose_answer_dfs = solve_constraint_dfs(moose_problem.copy())
    moose_answer_propany = solve_constraint_propagate_reduced_domains(moose_problem.copy())
    moose_answer_prop1 = solve_constraint_propagate_singleton_domains(moose_problem.copy())
    moose_answer_generic_dfs = solve_constraint_generic(moose_problem.copy(), None)
    moose_answer_generic_propany = solve_constraint_generic(moose_problem.copy(), condition_domain_reduction)
    moose_answer_generic_prop1 = solve_constraint_generic(moose_problem.copy(), condition_singleton)
    moose_answer_generic_fc = solve_constraint_generic(moose_problem.copy(), condition_forward_checking)
    moose_instance_for_domain_reduction = moose_problem.copy()
    moose_answer_domain_reduction = domain_reduction(moose_instance_for_domain_reduction)
    moose_instance_for_domain_reduction_singleton = moose_problem.copy()
    moose_answer_domain_reduction_singleton = domain_reduction_singleton_domains(moose_instance_for_domain_reduction_singleton)

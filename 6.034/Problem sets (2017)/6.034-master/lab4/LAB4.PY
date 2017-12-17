from constraint_api import *
from test_problems import get_pokemon_problem

#### PART 1: WRITE A DEPTH-FIRST SEARCH CONSTRAINT SOLVER

def has_empty_domains(csp) :
    "Returns True if the problem has one or more empty domains, otherwise False"
    for variable in csp.domains:
        # if no values associated with a variable return True
        if len(csp.domains[variable]) == 0:
            return True
    return False

def check_all_constraints(csp) :
    """Return False if the problem's assigned values violate some constraint,
    otherwise True"""
    values = csp.assigned_values
    # Check every variable against every other variable
    for var1 in values:
        for var2 in values:
            # Through every constraint that applies to the two variables
            for constraint in csp.constraints_between(var1, var2):
                    # If the constraint fails
                    if not constraint.check(values[var1],values[var2]):
                        # Return False
                        return False
    # Otherwise return True, everything passed
    return True



def solve_constraint_dfs(problem) :
    """Solves the problem using depth-first search.  Returns a tuple containing:
    1. the solution (a dictionary mapping variables to assigned values), and
    2. the number of extensions made (the number of problems popped off the agenda).
    If no solution was found, return None as the first element of the tuple."""
    num_extensions = 0

    agenda = [problem]

    while len(agenda) > 0:
        csp = agenda.pop(0)
        num_extensions += 1
        if has_empty_domains(csp):
            # unsolvable problem
            pass
        else:
            # solve
            if not check_all_constraints(csp):
                # if constraint fails, go to next iteration of loop
                pass
            else:
                # if all variables assigned, return solution
                if len(csp.unassigned_vars) == 0:
                    return (csp.assigned_values, num_extensions)
                else:
                    new_problems = []
                    var = csp.pop_next_unassigned_var()
                    for val in csp.get_domain(var):
                        csp_new = csp.copy()
                        csp_new.set_assigned_value(var, val)
                        new_problems.append(csp_new)
                    agenda = new_problems + agenda

    # completely unsolvable then
    return (None, num_extensions)


#### PART 2: DOMAIN REDUCTION BEFORE SEARCH

def eliminate_from_neighbors(csp, var) :
    """Eliminates incompatible values from var's neighbors' domains, modifying
    the original csp.  Returns an alphabetically sorted list of the neighboring
    variables whose domains were reduced, with each variable appearing at most
    once.  If no domains were reduced, returns empty list.
    If a domain is reduced to size 0, quits immediately and returns None."""
    reduced_vars = []
    var_value = csp.get_domain(var)
    if len(var_value) > 1:
        # no domains reduced if more than one value
        return []
    else:
        # for each neighbor variable
        for neighbor_var in csp.get_all_variables():
            # for each constraint between variables
            for constraint in csp.constraints_between(var, neighbor_var):
                # for each possible value in neighbor variable domain
                domains_to_iterate = csp.get_domain(neighbor_var)[:]
                for neighbor_val in domains_to_iterate:
                    # If constraint fails, remove value from neighbor domain
                    # Also add variable to list of reduced
                    if not constraint.check(var_value[0], neighbor_val):
                        csp.eliminate(neighbor_var, neighbor_val)
                        if len(csp.get_domain(neighbor_var)) == 0 or len(csp.get_domain(var)) == 0:
                            return None
                        reduced_vars.append(neighbor_var)

    # Remove duplicates, sort alphabetically and return list of domain-reduced variables
    result = list(set(reduced_vars))
    result.sort()
    return result




def domain_reduction(csp, queue=None) :
    """Uses constraints to reduce domains, modifying the original csp.
    If queue is None, initializes propagation queue by adding all variables in
    their default order.  Returns a list of all variables that were dequeued,
    in the order they were removed from the queue.  Variables may appear in the
    list multiple times.
    If a domain is reduced to size 0, quits immediately and returns None."""
    csp_original = csp.copy()
    # Define queue
    if queue == None:
        queue = csp.get_all_variables()[:]
    else:
        # redundant for clarity
        queue = queue

    dequeued = []

    # While the queue still has unassigned variables
    while len(queue) > 0:
        # Pop off the first variabled
        var = queue.pop(0)
        dequeued.append(var)
        # For each neighbor variable
        for neighbor_var in csp.variables:
            # For each constraint between var and neighbor_var
            for constraint in csp.constraints_between(var, neighbor_var):
                # For each value in neighbor_var domain
                neighbor_var_domain = csp.get_domain(neighbor_var)[:]
                for neighbor_val in neighbor_var_domain:
                    # For each value in var domain
                    num_var_values = len(csp.get_domain(var))
                    constraint_counter = 0
                    for val in csp.get_domain(var):
                        # If it passes, fine
                        if constraint.check(val, neighbor_val):
                            pass
                        # otherwise, iterate counter, it failed
                        else:
                            constraint_counter += 1
                    # if every value fails, neighbor value should be removed from domain
                    # and neighbor var added to queue  
                    if constraint_counter == num_var_values:
                        csp.eliminate(neighbor_var, neighbor_val)

                        # If empty domain, exit
                        if len(csp.get_domain(neighbor_var)) == 0:
                            # csp is unsolvable
                            return None

                        # Add neighbor_val to the queue if not there
                        if not neighbor_var in queue:
                            queue.append(neighbor_var)

    return dequeued


# QUESTION 1: How many extensions does it take to solve the Pokemon problem
#    with dfs if you DON'T use domain reduction before solving it?

# Hint: Use get_pokemon_problem() to get a new copy of the Pokemon problem
#    each time you want to solve it with a different search method.

ANSWER_1 = 20

# QUESTION 2: How many extensions does it take to solve the Pokemon problem
#    with dfs if you DO use domain reduction before solving it?

ANSWER_2 = 6


#### PART 3: PROPAGATION THROUGH REDUCED DOMAINS

def solve_constraint_propagate_reduced_domains(problem) :
    """Solves the problem using depth-first search with forward checking and
    propagation through all reduced domains.  Same return type as
    solve_constraint_dfs."""
    num_extensions = 0

    agenda = [problem]

    while len(agenda) > 0:
        csp = agenda.pop(0)
        num_extensions += 1
        if has_empty_domains(csp):
            # unsolvable problem
            pass
        else:
            # solve
            if not check_all_constraints(csp):
                # if constraint fails, go to next iteration of loop
                pass
            else:
                # if all variables assigned, return solution
                if len(csp.unassigned_vars) == 0:
                    return (csp.assigned_values, num_extensions)
                else:
                    new_problems = []
                    var = csp.pop_next_unassigned_var()
                    for val in csp.get_domain(var):
                        csp_new = csp.copy()
                        csp_new.set_assigned_value(var, val)

                        # domain reduction
                        domain_reduction(csp_new, [var])

                        new_problems.append(csp_new)
                    agenda = new_problems + agenda

    # completely unsolvable then
    return (None, num_extensions)

# QUESTION 3: How many extensions does it take to solve the Pokemon problem
#    with propagation through reduced domains? (Don't use domain reduction
#    before solving it.)

ANSWER_3 = 7


#### PART 4: PROPAGATION THROUGH SINGLETON DOMAINS

def domain_reduction_singleton_domains(csp, queue=None) :
    """Uses constraints to reduce domains, modifying the original csp.
    Only propagates through singleton domains.
    Same return type as domain_reduction."""
    csp_original = csp.copy()
    # Define queue
    if queue == None:
        queue = csp.get_all_variables()[:]
    else:
        # redundant for clarity
        queue = queue

    dequeued = []

    # While the queue still has unassigned variables
    while len(queue) > 0:
        # Pop off the first variabled
        var = queue.pop(0)
        dequeued.append(var)
        # For each neighbor variable
        for neighbor_var in csp.variables:
            # For each constraint between var and neighbor_var
            for constraint in csp.constraints_between(var, neighbor_var):
                # For each value in neighbor_var domain
                neighbor_var_domain = csp.get_domain(neighbor_var)[:]
                for neighbor_val in neighbor_var_domain:
                    # For each value in var domain
                    num_var_values = len(csp.get_domain(var))
                    constraint_counter = 0
                    for val in csp.get_domain(var):
                        # If it passes, fine
                        if constraint.check(val, neighbor_val):
                            pass
                        # otherwise, iterate counter, it failed
                        else:
                            constraint_counter += 1
                    # if every value fails, neighbor value should be removed from domain
                    # and neighbor var added to queue  
                    if constraint_counter == num_var_values:
                        csp.eliminate(neighbor_var, neighbor_val)

                        # If empty domain, exit
                        if len(csp.get_domain(neighbor_var)) == 0:
                            # csp is unsolvable
                            return None

                        # Add neighbor_val to the queue if not there
                        if not neighbor_var in queue:
                            if len(csp.get_domain(neighbor_var)) == 1:
                                queue.append(neighbor_var)
    return dequeued

def solve_constraint_propagate_singleton_domains(problem) :
    """Solves the problem using depth-first search with forward checking and
    propagation through singleton domains.  Same return type as
    solve_constraint_dfs."""
    num_extensions = 0

    agenda = [problem]

    while len(agenda) > 0:
        csp = agenda.pop(0)
        num_extensions += 1
        if has_empty_domains(csp):
            # unsolvable problem
            pass
        else:
            # solve
            if not check_all_constraints(csp):
                # if constraint fails, go to next iteration of loop
                pass
            else:
                # if all variables assigned, return solution
                if len(csp.unassigned_vars) == 0:
                    return (csp.assigned_values, num_extensions)
                else:
                    new_problems = []
                    var = csp.pop_next_unassigned_var()
                    for val in csp.get_domain(var):
                        csp_new = csp.copy()
                        csp_new.set_assigned_value(var, val)

                        # domain reduction
                        domain_reduction_singleton_domains(csp_new, [var])

                        new_problems.append(csp_new)
                    agenda = new_problems + agenda

    # completely unsolvable then
    return (None, num_extensions)

# QUESTION 4: How many extensions does it take to solve the Pokemon problem
#    with propagation through singleton domains? (Don't use domain reduction
#    before solving it.)

ANSWER_4 = 8


#### PART 5: FORWARD CHECKING

def propagate(enqueue_condition_fn, csp, queue=None) :
    """Uses constraints to reduce domains, modifying the original csp.
    Uses enqueue_condition_fn to determine whether to enqueue a variable whose
    domain has been reduced.  Same return type as domain_reduction."""
    csp_original = csp.copy()
    # Define queue
    if queue == None:
        queue = csp.get_all_variables()[:]
    else:
        # redundant for clarity
        queue = queue

    dequeued = []

    # While the queue still has unassigned variables
    while len(queue) > 0:
        # Pop off the first variabled
        var = queue.pop(0)
        dequeued.append(var)
        # For each neighbor variable
        for neighbor_var in csp.variables:
            # For each constraint between var and neighbor_var
            for constraint in csp.constraints_between(var, neighbor_var):
                # For each value in neighbor_var domain
                neighbor_var_domain = csp.get_domain(neighbor_var)[:]
                for neighbor_val in neighbor_var_domain:
                    # For each value in var domain
                    num_var_values = len(csp.get_domain(var))
                    constraint_counter = 0
                    for val in csp.get_domain(var):
                        # If it passes, fine
                        if constraint.check(val, neighbor_val):
                            pass
                        # otherwise, iterate counter, it failed
                        else:
                            constraint_counter += 1
                    # if every value fails, neighbor value should be removed from domain
                    # and neighbor var added to queue  
                    if constraint_counter == num_var_values:
                        csp.eliminate(neighbor_var, neighbor_val)

                        # If empty domain, exit
                        if len(csp.get_domain(neighbor_var)) == 0:
                            # csp is unsolvable
                            return None

                        # Add neighbor_val to the queue if not there
                        if not neighbor_var in queue:
                            if enqueue_condition_fn(csp, neighbor_var):
                                queue.append(neighbor_var)

    return dequeued

def condition_domain_reduction(csp, var) :
    """Returns True if var should be enqueued under the all-reduced-domains
    condition, otherwise False"""
    return True

def condition_singleton(csp, var) :
    """Returns True if var should be enqueued under the singleton-domains
    condition, otherwise False"""
    if len(csp.get_domain(var)) == 1:
        return True
    else:
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

    num_extensions = 0

    agenda = [problem]

    while len(agenda) > 0:
        csp = agenda.pop(0)
        num_extensions += 1
        if has_empty_domains(csp):
            # unsolvable problem
            pass
        else:
            # solve
            if not check_all_constraints(csp):
                # if constraint fails, go to next iteration of loop
                pass
            else:
                # if all variables assigned, return solution
                if len(csp.unassigned_vars) == 0:
                    return (csp.assigned_values, num_extensions)
                else:
                    new_problems = []
                    var = csp.pop_next_unassigned_var()
                    for val in csp.get_domain(var):
                        csp_new = csp.copy()
                        csp_new.set_assigned_value(var, val)

                        if enqueue_condition != None:
                            # propogate variable reduction
                            propagate(enqueue_condition, csp_new, [var])

                        new_problems.append(csp_new)
                    agenda = new_problems + agenda

    # completely unsolvable then
    return (None, num_extensions)

# QUESTION 5: How many extensions does it take to solve the Pokemon problem
#    with DFS and forward checking, but no propagation? (Don't use domain
#    reduction before solving it.)

ANSWER_5 = 9


#### PART 7: DEFINING CUSTOM CONSTRAINTS

def constraint_adjacent(m, n) :
    """Returns True if m and n are adjacent, otherwise False.
    Assume m and n are ints."""
    if abs(m-n) == 1:
        return True
    else:
        return False

def constraint_not_adjacent(m, n) :
    """Returns True if m and n are NOT adjacent, otherwise False.
    Assume m and n are ints."""
    return not constraint_adjacent(m, n)

def all_different(variables) :
    """Returns a list of constraints, with one difference constraint between
    each pair of variables."""
    from itertools import combinations

    var_combinations = combinations(variables, 2)
    constraints_list = []

    for var1, var2 in var_combinations:
        constraint = Constraint(var1, var2, constraint_different)
        constraints_list.append(constraint)

    return constraints_list



#### PART 8: MOOSE PROBLEM (OPTIONAL)

moose_problem = ConstraintSatisfactionProblem(["You", "Moose", "McCain",
                                               "Palin", "Obama", "Biden"])

# Add domains and constraints to your moose_problem here:


# To test your moose_problem AFTER implementing all the solve_constraint
# methods above, change TEST_MOOSE_PROBLEM to True:
TEST_MOOSE_PROBLEM = False


#### SURVEY ###################################################

NAME = 'Laser Nite'
COLLABORATORS = 'None'
HOW_MANY_HOURS_THIS_LAB_TOOK = 9
WHAT_I_FOUND_INTERESTING = 'domain reduction'
WHAT_I_FOUND_BORING = 'getting stuck for hours because python makes lives changes to iteration while running a loop. Have to make copies of list.'
SUGGESTIONS = 'None'


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


# The following wrapper functions are used in the online tester. DO NOT CHANGE!

def wrapper_constraint(var1, var2, constraint_fn):
    return Constraint(var1, var2, constraint_fn)

def wrapper_CSP(variables, constraint_list, unassigned_vars, domains, assigned_values):
    csp = ConstraintSatisfactionProblem(variables)
    if all(map(isinstance_Constraint, constraint_list)):
        csp.constraints = constraint_list
    elif all([isinstance(c, (list, tuple)) for c in constraint_list]):
        csp.constraints = [wrapper_constraint(*c_args) for c_args in constraint_list]
    else:
        csp.constraints = constraint_list
    csp.unassigned_vars = unassigned_vars
    csp.domains = domains
    csp.assigned_values = assigned_values
    return csp

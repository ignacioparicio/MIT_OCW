from production import AND, OR, NOT, PASS, FAIL, IF, THEN, \
     match, populate, simplify, variables
from zookeeper import ZOOKEEPER_RULES

# This function, which you need to write, takes in a hypothesis
# that can be determined using a set of rules, and outputs a goal
# tree of which statements it would need to test to prove that
# hypothesis. Refer to the problem set (section 2) for more
# detailed specifications and examples.

# Note that this function is supposed to be a general
# backchainer.  You should not hard-code anything that is
# specific to a particular rule set.  The backchainer will be
# tested on things other than ZOOKEEPER_RULES.


def backchain_to_goal_tree(rules, hypothesis):
     
    antecedents = []
    # Get all rule consequents matching hypothesis
    for rule in rules:
        if match(rule.consequent()[0], hypothesis):
            antecedents.append(rule.antecedent())
    
    # Base case: if no antecedents, return hypothesis
    if len(antecedents) == 0:
        return hypothesis
        
    # Recursive case: if antecedents, keep backchaining recursively
    else:
        for antecedent_node in antecedents:
            n = len(antecedent_node)
            for i in range(n):
                # Replace each condition with OR(condition, antecedents leading to condition)
                antecedent_node[i] = OR(backchain_to_goal_tree(rules, antecedent_node[i]))
        
        result = simplify(OR([hypothesis] + antecedents))
                
        return populate_name(result, hypothesis)
        #return result
        
def populate_name(tree, hypothesis):
    # backchain_to_goal_tree returns full tree without substituting variable
    # names (e.g. (?x). This function populates names in the whole tree.

    #name = match("(?x) is an (?y)", hypothesis)['x']
    name = hypothesis.partition(' ')[0]
    
    for i in range(len(tree)):
        
        # Base case: condition (and NOT list of conditions) found
        if not isinstance(tree[i], list):
            tree[i] = populate(tree[i], {'x': name})
            
        # Recursive case: get list element and iterate through it
        else:
            tree[i] = populate_name(tree[i], hypothesis)
            
    return tree





# Here's an example of running the backward chainer - uncomment
# it to see it work:
#print(backchain_to_goal_tree(ZOOKEEPER_RULES, 'opus is a penguin'))

# TEST 11

#answer = backchain_to_goal_tree(ZOOKEEPER_RULES, 'alice is an albatross')

#result_bc_2 = OR('alice is an albatross',
#                 AND(OR('alice is a bird',
#                        'alice has feathers',
#                        AND('alice flies',
#                            'alice lays eggs')),
#                     'alice is a good flyer'))
#
#print(answer == result_bc_2)
#print(answer)

# TEST 12
print(backchain_to_goal_tree(ZOOKEEPER_RULES, 'geoff is a giraffe'))
#
#result_bc_3 = OR('geoff is a giraffe',
#                 AND(OR('geoff is an ungulate',
#                        AND(OR('geoff is a mammal',
#                               'geoff has hair',
#                               'geoff gives milk'),
#                            'geoff has hoofs'),
#                        AND(OR('geoff is a mammal',
#                               'geoff has hair',
#                               'geoff gives milk'),
#                            'geoff chews cud')),
#                     'geoff has long legs',
#                     'geoff has long neck',
#                     'geoff has tawny color',
#                     'geoff has dark spots'))

# TEST 13                     
#rules = [ IF( AND( '(?x) has (?y)',
#                        '(?x) has (?z)' ),
#                   THEN( '(?x) has (?y) and (?z)' ) ),
#               IF( '(?x) has rhythm and music',
#                   THEN( '(?x) could not ask for anything more' ) ) ]
#hypothesis = 'gershwin could not ask for anything more'
#
#print(backchain_to_goal_tree(rules, hypothesis))
#
#result_bc_4 = OR('gershwin could not ask for anything more',
#                 'gershwin has rhythm and music', 
#                 AND('gershwin has rhythm',
#                     'gershwin has music'))


    
#test = match("(?x) is a (?y)", "opus is a penguin")
#if pa:
#    print('Yes')
#print(match("(?x) is a (?y)", "opus is a penguin")['x'])
#print(populate("(?x) is a (?y)", { 'x': "John", 'y': "student" }))

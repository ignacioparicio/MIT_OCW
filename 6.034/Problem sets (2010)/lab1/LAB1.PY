# lab1.py 

#You should start here when providing the answers to Problem Set 1.
#Follow along in the problem set, which is at:
#http://ai6034.mit.edu/fall12/index.php?title=Lab_1

# Import helper objects that provide the logical operations
# discussed in class.
from production import IF, AND, OR, NOT, THEN, DELETE, forward_chain

## Section 1: Forward chaining ##

# Problem 1.2: Multiple choice

# Which part of a rule may change the data?
#    1. the antecedent
#    2. the consequent
#    3. both

ANSWER_1 = '2'

# A rule-based system about Monty Python's "Dead Parrot" sketch
# uses the following rules:
#
# rule1 = IF( AND( '(?x) is a Norwegian Blue parrot',
#                  '(?x) is motionless' ),
#             THEN( '(?x) is not dead' ) )
#
# rule2 = IF( NOT( '(?x) is dead' ),
#             THEN( '(?x) is pining for the fjords' ) )
#
# and the following initial data:
#
# ( 'Polly is a Norwegian Blue parrot',
#   'Polly is motionless' )
#

# Will this system produce the datum 'Polly is pining for the
# fjords'?  Answer 'yes' or 'no'.
ANSWER_2 = 'no'

# Which rule contains a programming error? Answer '1' or '2'.
ANSWER_3 = '2'

# If you're uncertain of these answers, look in tests.py for an
# explanation.


# In a completely different scenario, suppose we have the
# following rules list:
#
# ( IF( AND( '(?x) has feathers',  # rule 1
#            '(?x) has a beak' ),
#       THEN( '(?x) is a bird' ),
#   IF( AND( '(?y) is a bird',     # rule 2
#            '(?y) cannot fly',
#            '(?y) can swim' ),
#       THEN( '(?y) is a penguin' ) ) )
#
# and the following list of initial data:
#
# ( 'Pendergast is a penguin',
#   'Pendergast has feathers',
#   'Pendergast has a beak',
#   'Pendergast cannot fly',
#   'Pendergast can swim' )
#
# In the following questions, answer '0' if neither rule does
# what is asked.  After we start the system running, which rule
# fires first?

ANSWER_4 = '1'

# Which rule fires second?

ANSWER_5 = '0'


# Problem 1.3.1: Poker hands

# You're given this data about poker hands:
poker_data = ( 'two-pair beats pair',
               'three-of-a-kind beats two-pair',
               'straight beats three-of-a-kind',
               'flush beats straight',
               'full-house beats flush',
               'straight-flush beats full-house' )

# Fill in this rule so that it finds all other combinations of
# which poker hands beat which, transitively. For example, it
# should be able to deduce that a three-of-a-kind beats a pair,
# because a three-of-a-kind beats two-pair, which beats a pair.
transitive_rule = IF(AND('(?x) beats (?y)', '(?y) beats (?z)'),
                     THEN('(?x) beats (?z)'))

# You can test your rule like this:
# print(forward_chain([transitive_rule], poker_data))

# Here's some other data sets for the rule. The tester uses
# these, so don't change them.
TEST_RESULTS_TRANS1 = forward_chain([transitive_rule],
                                    [ 'a beats b', 'b beats c' ])
TEST_RESULTS_TRANS2 = forward_chain([transitive_rule],
  [ 'rock beats scissors', 
    'scissors beats paper', 
    'paper beats rock' ])
    

# Problem 1.3.2: Family relations

# First, define all your rules here individually. That is, give
# them names by assigning them to variables. This way, you'll be
# able to refer to the rules by name and easily rearrange them if
# you need to.

r0 = IF(OR('male (?x)', 'female (?x)'), THEN('same-identity (?x) (?x)'))

r1 = IF(AND('male (?x)', 'parent (?x) (?y)'), THEN('father (?x) (?y)'))

r2 = IF(AND('female (?x)', 'parent (?x) (?y)'), THEN('mother (?x) (?y)'))

r3 = IF(AND('male (?y)', 'parent (?x) (?y)'), THEN('son (?y) (?x)'))

r4 = IF(AND('female (?y)', 'parent (?x) (?y)'), THEN('daughter (?y) (?x)'))

r5 = IF(AND('female (?x)', 'parent (?z) (?x)', 'parent (?z) (?y)',
            NOT('same-identity (?x) (?y)')),
        THEN('sister (?x) (?y)'))
        
r6 = IF(AND('male (?x)', 'parent (?z) (?x)', 'parent (?z) (?y)',
            NOT('same-identity (?x) (?y)')),
        THEN('brother (?x) (?y)'))
        
r7 = IF(OR('sister (?x) (?y)', 'brother (?x) (?y)'), THEN('sibling (?x) (?y)'))

r8 = IF(AND('parent (?x) (?y)', 'parent (?u) (?v)',
            NOT('sibling (?y) (?v)'), 'sibling (?x) (?u)'),
        THEN('cousin (?y) (?v)'))
        
r9 = IF(AND('parent (?x) (?y)', 'parent (?y) (?z)'),
        THEN('grandparent (?x) (?z)'))
        
r10 = IF(AND('parent (?x) (?y)', 'parent (?y) (?z)'),
        THEN('grandchild (?z) (?x)'))

        
# Then, put them together into a list in order, and call it
# family_rules.
family_rules = [r0, r1, r2, r3, r4, r5, r6, r7, r8, r9, r10]

# Some examples to try it on:
# Note: These are used for testing, so DO NOT CHANGE
simpsons_data = ("male bart",
                 "female lisa",
                 "female maggie",
                 "female marge",
                 "male homer",
                 "male abe",
                 "parent marge bart",
                 "parent marge lisa",
                 "parent marge maggie",
                 "parent homer bart",
                 "parent homer lisa",
                 "parent homer maggie",
                 "parent abe homer")
                 
TEST_RESULTS_6 = forward_chain(family_rules,
                               simpsons_data,
                               verbose = False)
# You can test your results by uncommenting this line:
#print(forward_chain(family_rules, simpsons_data, verbose = True))

black_data = ("male sirius",
              "male regulus",
              "female walburga",
              "male alphard",
              "male cygnus",
              "male pollux",
              "female bellatrix",
              "female andromeda",
              "female narcissa",
              "female nymphadora",
              "male draco",
              "parent walburga sirius",
              "parent walburga regulus",
              "parent pollux walburga",
              "parent pollux alphard",
              "parent pollux cygnus",
              "parent cygnus bellatrix",
              "parent cygnus andromeda",
              "parent cygnus narcissa",
              "parent andromeda nymphadora",
              "parent narcissa draco")

# This should generate 14 cousin relationships, representing
# 7 pairs of people who are cousins:

black_family_cousins = [ 
    x for x in 
    forward_chain(family_rules, black_data, verbose=False) 
    if "cousin" in x ]

# To see if you found them all, uncomment this line:
#print(black_family_cousins)

# To debug what happened in your rules, you can set verbose=True
# in the function call above.

# Some other data sets to try it on. The tester uses these
# results, so don't comment them out.

TEST_DATA_1 = [ 'female alice',
                'male bob',
                'male chuck',
                'parent chuck alice',
                'parent chuck bob' ]
TEST_RESULTS_1 = forward_chain(family_rules, 
                               TEST_DATA_1, verbose=False)

TEST_DATA_2 = [ 'female a1', 'female b1', 'female b2', 
                'female c1', 'female c2', 'female c3', 
                'female c4', 'female d1', 'female d2', 
                'female d3', 'female d4',
                'parent a1 b1',
                'parent a1 b2',
                'parent b1 c1',
                'parent b1 c2',
                'parent b2 c3',
                'parent b2 c4',
                'parent c1 d1',
                'parent c2 d2',
                'parent c3 d3',
                'parent c4 d4' ]

TEST_RESULTS_2 = forward_chain(family_rules, 
                               TEST_DATA_2, verbose=False)

TEST_RESULTS_6 = forward_chain(family_rules,
                               simpsons_data,verbose=False)

## Section 2: Goal trees and backward chaining ##

# Problem 2 is found in backchain.py.

from backchain import backchain_to_goal_tree

##; Section 3: Survey ##
# Please answer these questions inside the double quotes.

HOW_MANY_HOURS_THIS_PSET_TOOK = '6'
WHAT_I_FOUND_INTERESTING = '''How outcomes actually seem "smart" when lengthy
                              or complicated input is given, despite using
                              the same code in the background'''
WHAT_I_FOUND_BORING = 'Developing the backchainer took way longer than expected'



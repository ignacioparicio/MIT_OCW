# -*- coding: utf-8 -*-
from production import IF, AND, OR, NOT, THEN, forward_chain
from data import *

#### Part 1: Multiple Choice #########################################

ANSWER_1 = '2'

ANSWER_2 = 'no'

ANSWER_3 = '2'

ANSWER_4 = '1'

ANSWER_5 = '0'


#### Part 2: Transitive Rule #########################################

transitive_rule = IF( AND('(?x) beats (?y)','(?y) beats (?z)'), THEN('(?x) beats (?z)') )

# You can test your rule by uncommenting these print statements:
#print forward_chain([transitive_rule], abc_data)
#print forward_chain([transitive_rule], poker_data)
#print forward_chain([transitive_rule], minecraft_data)


#### Part 3: Family Relations #########################################

# Define your rules here:
sel = IF( 'person (?x)' , THEN('self (?x) (?x)'))
sib_sib = IF( 'sibling (?x) (?y)' , THEN( 'sibling (?y) (?x)' ) )
chi_par = IF( 'child (?y) (?x)' , THEN( 'parent (?x) (?y)' ))
par_chi = IF( 'parent (?x) (?y)' , THEN( 'child (?y) (?x)' ))
cou_cou = IF( 'cousin (?x) (?y)' , THEN( 'cousin (?y) (?x)' ) )
gpa_gch = IF( 'grandparent (?y) (?x)' , THEN( 'grandchild (?x) (?y)' ))
gch_gpa = IF( 'grandchild (?y) (?x)' , THEN( 'grandparent (?x) (?y)' ))
sib = IF( AND(AND('parent (?x) (?y)','parent (?x) (?z)'),NOT ('self (?y) (?z)')), THEN('sibling (?y) (?z)') )
cou = IF( AND( AND('parent (?x) (?y)','parent (?z) (?w)'),'sibling (?x) (?z)' ), THEN('cousin (?y) (?w)') )
gpa = IF( AND('parent (?x) (?y)','parent (?y) (?z)'),THEN('grandparent (?x) (?z)'))


# Add your rules to this list:
family_rules = [sel,sib_sib,chi_par,par_chi,cou_cou,gpa_gch,gch_gpa,sib,cou,gpa]

# Uncomment this to test your data on the Simpsons family:
#print forward_chain(family_rules, simpsons_data, verbose=False)

# These smaller datasets might be helpful for debugging:
#print forward_chain(family_rules, sibling_test_data, verbose=True)
#print forward_chain(family_rules, grandparent_test_data, verbose=True)

# The following should generate 14 cousin relationships, representing 7 pairs
# of people who are cousins:
black_family_cousins = [ 
    relation for relation in 
    forward_chain(family_rules, black_data, verbose=False) 
    if "cousin" in relation ]

# To see if you found them all, uncomment this line:
#print black_family_cousins


#### Part 4: Backward Chaining #########################################

# Import additional methods for backchaining
from production import PASS, FAIL, match, populate, simplify, variables

def backchain_to_goal_tree(rules, hypothesis):
    temp = hypothesis
    l = []
    for i in rules:
        q = i.consequent()
        p = False
        for j in q:
            m = match(j,hypothesis)
            if (m != None):
                n = populate(i.antecedent(), m)
                l.append(n)
    if (len(l) == 0):
        return hypothesis
    for i in l:
        if isinstance(i,str):
            i = backchain_to_goal_tree(rules,i)
        else:
            x = len(i)
            for j in range(x):
                i[j] = backchain_to_goal_tree(rules,i[j])
        temp = simplify(OR(temp, i))
    return temp
        

# Uncomment this to run your backward chainer:
#print backchain_to_goal_tree(zookeeper_rules, 'opus is a penguin')


#### Survey #########################################

NAME = 'Sze Nga Wong'
COLLABORATORS = ''
HOW_MANY_HOURS_THIS_LAB_TOOK = 7
WHAT_I_FOUND_INTERESTING = 'I was stuck at how to obtain the individual elements in AND or OR but found out it is simply a list. It allows easy manipulation of the data.'
WHAT_I_FOUND_BORING = 'Nothing.'
SUGGESTIONS = None


###########################################################
### Ignore everything below this line; for testing only ###
###########################################################

# The following lines are used in the tester. DO NOT CHANGE!
transitive_rule_poker = forward_chain([transitive_rule], poker_data)
transitive_rule_abc = forward_chain([transitive_rule], abc_data)
transitive_rule_minecraft = forward_chain([transitive_rule], minecraft_data)
family_rules_simpsons = forward_chain(family_rules, simpsons_data)
family_rules_black = forward_chain(family_rules, black_data)
family_rules_sibling = forward_chain(family_rules, sibling_test_data)
family_rules_grandparent = forward_chain(family_rules, grandparent_test_data)
family_rules_anonymous_family = forward_chain(family_rules, anonymous_family_test_data)

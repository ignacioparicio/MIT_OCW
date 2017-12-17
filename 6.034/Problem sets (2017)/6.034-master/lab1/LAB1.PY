from production import IF, AND, OR, NOT, THEN, forward_chain
from data import *

#### Part 1: Multiple Choice #########################################

ANSWER_1 = '2'

ANSWER_2 = 'no'

ANSWER_3 = '2'

ANSWER_4 = '1'

ANSWER_5 = '0'


#### Part 2: Transitive Rule #########################################

transitive_rule = IF( AND('(?x) beats (?y)', '(?y) beats (?z)'), THEN( '(?x) beats (?z)' ) )

# You can test your rule by uncommenting these print statements:
# print forward_chain([transitive_rule], abc_data)
# print forward_chain([transitive_rule], poker_data)
# print forward_chain([transitive_rule], minecraft_data)

#### Part 3: Family Relations #########################################

# Define your rules here:

self_rule = IF('person (?x)', THEN('self (?x) (?x)'))

sibling_rule = IF( AND('parent (?x) (?y)', 'parent (?x) (?z)', NOT('self (?y) (?z)')), THEN('sibling (?y) (?z)', 'sibling (?z) (?y)'))

child_rule = IF( 'parent (?x) (?y)', THEN('child (?y) (?x)'))

cousin_rule = IF( AND('sibling (?x) (?y)', 'sibling (?y) (?x)', 'parent (?x) (?z)', 'parent (?y) (?a)', NOT('self (?z) (?a)')), 
				THEN('cousin (?z) (?a)', 'cousin (?a) (?z)') )

grand_rule = IF( AND('parent (?x) (?y)', 'parent (?y) (?z)'), THEN('grandparent (?x) (?z)', 'grandchild (?z) (?x)'))


# Add your rules to this list:
family_rules = [self_rule, sibling_rule, child_rule, cousin_rule, grand_rule]

# Uncomment this to test your data on the Simpsons family:
# print forward_chain(family_rules, simpsons_data, verbose=False)

# These smaller datasets might be helpful for debugging:
# print forward_chain(family_rules, sibling_test_data, verbose=True)
# print forward_chain(family_rules, grandparent_test_data, verbose=True)

# The following should generate 14 cousin relationships, representing 7 pairs
# of people who are cousins:
black_family_cousins = [ 
    relation for relation in 
    forward_chain(family_rules, black_data, verbose=False) 
    if "cousin" in relation ]

# To see if you found them all, uncomment this line:
# print black_family_cousins


#### Part 4: Backward Chaining #########################################

# Import additional methods for backchaining
from production import PASS, FAIL, match, populate, simplify, variables


'''
def backchain_to_goal_tree_old(rules, hypothesis):
    # go through each rule and gather rules with matching consequent in consequent_match_list
    consequent_match_list = []
    goal_tree = OR()
    antecedent_hypotheses = AND()
    for rule in rules:
    	# if any consequent matches append rule
    	# for consequent in THEN('(?x) is a giraffe', '(?x) is a zebra')
    	for consequent in rule.consequent():
    		# populate('(?x) is a giraffe', {x: Bobby}) -> 'Bobby is a giraffe'
    		matched = match(consequent, hypothesis)
    		if not matched == None:
	    		if populate(consequent, matched) == hypothesis:
	    			variables = match(consequent, hypothesis)
	    			# append.(['(?x) is a giraffe', {x: Bobby}, AND('(?x) is a bird', '(?x) is a good flyer')])
	    			consequent_match_list.append([consequent, variables, rule.antecedent()])
    
    	for consequent in rule.consequent():
	    	# Check for antecedents that match rule consequents 
	    	for x in consequent_match_list:
	    		# antecedent in rule.antecedent()
	    		if isinstance(x[2], str):
	    			ant = populate(x[2], x[1])
	    			antecedent_hypotheses.append(ant)
	    		else:
		    		for antecedent in x[2]:
		    			# populate('(?x) is a bird', {x:'Bobby'}) -> 'Bobby is a bird'
		    			ant = populate(antecedent, x[1])
		    			antecedent_hypotheses.append(ant)
		    # See if any antecedents are consequents, and if so recursively backchain until no antecedents are consequents
			for a in antecedent_hypotheses:
		    	# if a is a string, it's leaf that can be left
		    	if isinstance(a, str):
		    	# otherwise it's an expression that needs to be backwards chained on
		    	# ie the antecedent should be matched against consequents of rules
		    	# these second level antecedents should be an AND() alternative
		    	else:
		    		for rule in rule.consequent():
		    			pass

    return simplify(OR(hypothesis, antecedent_hypotheses))
'''

def backchain_to_goal_tree(rules, hypothesis):
	goal_tree = OR(hypothesis)
	consequent_match_list = []

	# check through each rule
	for rule in rules:
		# if any consequent matches append rule
		# for consequent in THEN('(?x) is a penguin', '(?x) is a zebra') -> '(?x) is a penguin'
		for consequent in rule.consequent():
			# match('(?x) is a penguin', 'opus is a penguin') -> {x:'opus'}
			matched_variable = match(consequent, hypothesis)
			# if the consequent matches the hypothesis
			if not matched_variable == None:
				# populate('(?x) is a penguin', {x: opus}) -> 'opus is a penguin'
				# if the consequent really does match the hypothesis
				consequent_matched = populate(consequent, matched_variable) 
				if consequent_matched == hypothesis:
					# store the appropriate matched consequent, variable, and associated antecedents from the rule in a list 
					variables = match(consequent, hypothesis)
					# append.(['(?x) is a penguin', {x: opus}, AND('(?x) is a bird', '(?x) does not fly')])
					# consequent_match_list.append([consequent, variables, rule.antecedent()])
					# go through each antecedent (or just the one if it is one)
					antecedents = rule.antecedent()
					# only one antecedent
					if isinstance(antecedents, str):
						if type(rule.antecedent()) is AND:
							and_a = AND()
							# associate antecedent with variable to form new hypothesis
							# populate('(?x) is a bird', {x: 'opus'}) -> 'opus is a bird'
							antecedent_matched = populate(antecedents, variables)
							# fill in goal tree AND() part with 'opus is a bird' 
							# now check if 'opus is a bird' as a new hypothesis generates antecedents and recursively act on
							and_a.append(backchain_to_goal_tree(rules, antecedent_matched))
							goal_tree.append(and_a)
						else:			
							# associate antecedent with variable to form new hypothesis
							# populate('(?x) is a bird', {x: 'opus'}) -> 'opus is a bird'
							antecedent_matched = populate(antecedents, variables)
							# fill in goal tree AND() part with 'opus is a bird' 
							# now check if 'opus is a bird' as a new hypothesis generates antecedents and recursively act on
							goal_tree.append(backchain_to_goal_tree(rules, antecedent_matched))
					# multiple antecedents
					else:
						if type(rule.antecedent()) is AND:
							and_a = AND()
							for antecedent in rule.antecedent():
								# associate antecedent with variable to form new hypothesis
								# populate('(?x) is a bird', {x: 'opus'}) -> 'opus is a bird'
								antecedent_matched = populate(antecedent, variables)
								# fill in goal tree AND() part with 'opus is a bird' 
								# now check if 'opus is a bird' as a new hypothesis generates antecedents and recursively act on
								and_a.append(backchain_to_goal_tree(rules, antecedent_matched))
								goal_tree.append(and_a)
						else:
							for antecedent in rule.antecedent():
								# associate antecedent with variable to form new hypothesis
								# populate('(?x) is a bird', {x: 'opus'}) -> 'opus is a bird'
								antecedent_matched = populate(antecedent, variables)
								# fill in goal tree AND() part with 'opus is a bird' 
								# now check if 'opus is a bird' as a new hypothesis generates antecedents and recursively act on
								goal_tree.append(backchain_to_goal_tree(rules, antecedent_matched))

	return simplify(goal_tree)


def backchain_test(rules, hypothesis):
    consequent_match_list = []
    goal_tree = OR()
    antecedent_hypotheses = AND()
    for rule in rules:
    	for consequent in rule.consequent():
    		if not match(consequent, hypothesis) == None:
    			print populate(consequent, match(consequent, hypothesis))
    return 'hello kitty'




# Uncomment this to run your backward chainer:
#print backchain_to_goal_tree(zookeeper_rules, 'opus is a penguin')


#### Survey #########################################

NAME = 'Laser Nite'
COLLABORATORS = 'The 85 billion neurons in my brain'
HOW_MANY_HOURS_THIS_LAB_TOOK = 7
WHAT_I_FOUND_INTERESTING = 'It was all pretty interesting, but wrangling out backchaining was pretty hard, took like 4-5 of the 7 hours, rewrote it a bunch of times cause wasnt doing effective recursive implementation which im not very familiar with. A lot to take in, plus considering edge cases. Probably shouldve just tried to simplify it down to consider no edge cases and then build up from there.'
WHAT_I_FOUND_BORING = 'nothing particularly, pretty good pset'
SUGGESTIONS = 'none'


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

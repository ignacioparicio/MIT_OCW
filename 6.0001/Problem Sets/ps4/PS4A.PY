# Problem Set 4A
# Name: Ignacio Paricio
# Collaborators:
# Time Spent: 1:00

def get_permutations(sequence):
    '''
    Enumerate all permutations of a given string

    sequence (string): an arbitrary string to permute. Assume that it is a
    non-empty string.  

    You MUST use recursion for this part. Non-recursive solutions will not be
    accepted.

    Returns: a list of all permutations of sequence

    Example:
    >>> get_permutations('abc')
    ['abc', 'acb', 'bac', 'bca', 'cab', 'cba']

    Note: depending on your implementation, you may return the permutations in
    a different order than what is listed here.
    '''
    
    # Base case
    if len(sequence) == 1:
        return [sequence]
    # Recursive case
    else:
        permutations = []
        perm_sub_sequence = get_permutations(sequence[1:])
        first_char = sequence[0]
        
        for element in perm_sub_sequence:
            # +1 to allow inserting at the end of the string
            for i in range(len(element)+1):
                permutations.append(element[0:i] + first_char + element[i:(len(element)+1)])
        permutations.sort()
        return permutations
                
        
if __name__ == '__main__':
    #EXAMPLE
    example_input = 'abc'
    print('Input:', example_input)
    print('Expected Output:', ['abc', 'acb', 'bac', 'bca', 'cab', 'cba'])
    print('Actual Output:', get_permutations(example_input))
    
#    # Put three example test cases here (for your sanity, limit your inputs
#    to be three characters or fewer as you will have n! permutations for a 
#    sequence of length n)


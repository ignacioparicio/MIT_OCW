# Problem Set 4C
# Name: Ignacio Paricio
# Collaborators:
# Time Spent: 0:30

import string
from ps4a import get_permutations

### HELPER CODE ###
def load_words(file_name):
    '''
    file_name (string): the name of the file containing 
    the list of words to load    
    
    Returns: a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    '''
    
    print("Loading word list from file...")
    # inFile: file
    inFile = open(file_name, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.extend([word.lower() for word in line.split(' ')])
    print("  ", len(wordlist), "words loaded.")
    return wordlist

def is_word(word_list, word):
    '''
    Determines if word is a valid word, ignoring
    capitalization and punctuation

    word_list (list): list of words in the dictionary.
    word (string): a possible word.
    
    Returns: True if word is in word_list, False otherwise

    Example:
    >>> is_word(word_list, 'bat') returns
    True
    >>> is_word(word_list, 'asdf') returns
    False
    '''
    word = word.lower()
    word = word.strip(" !@#$%^&*()-_+={}[]|\:;'<>?,./\")
    return word in word_list


### END HELPER CODE ###

WORDLIST_FILENAME = 'words.txt'

# you may find these constants helpful
VOWELS_LOWER = 'aeiou'
VOWELS_UPPER = 'AEIOU'
CONSONANTS_LOWER = 'bcdfghjklmnpqrstvwxyz'
CONSONANTS_UPPER = 'BCDFGHJKLMNPQRSTVWXYZ'

class SubMessage(object):
    def __init__(self, text):
        '''
        Initializes a SubMessage object
                
        text (string): the message's text

        A SubMessage object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        self.message_text = text
        self.valid_words = load_words(WORDLIST_FILENAME)
    
    def get_message_text(self):
        '''
        Used to safely access self.message_text outside of the class
        
        Returns: self.message_text
        '''
        return self.message_text

    def get_valid_words(self):
        '''
        Used to safely access a copy of self.valid_words outside of the class.
        This helps you avoid accidentally mutating class attributes.
        
        Returns: a COPY of self.valid_words
        '''
        valid_words = self.valid_words.copy()
        return valid_words
                
    def build_transpose_dict(self, vowels_permutation):
        '''
        vowels_permutation (string): a string containing a permutation of vowels (a, e, i, o, u)
        
        Creates a dictionary that can be used to apply a cipher to a letter.
        The dictionary maps every uppercase and lowercase letter to an
        uppercase and lowercase letter, respectively. Vowels are shuffled 
        according to vowels_permutation. The first letter in vowels_permutation 
        corresponds to a, the second to e, and so on in the order a, e, i, o, u.
        The consonants remain the same. The dictionary should have 52 
        keys of all the uppercase letters and all the lowercase letters.

        Example: When input "eaiuo":
        Mapping is a->e, e->a, i->i, o->u, u->o
        and "Hello World!" maps to "Hallu Wurld!"

        Returns: a dictionary mapping a letter (string) to 
                 another letter (string). 
        '''
        
        
        alph_lower = list(string.ascii_lowercase) # abcdefghijklmnopqrstuvwxyz
        
        transpose_dict ={}
        for char in alph_lower:
            if char in VOWELS_LOWER:
                transpose_dict[char] = vowels_permutation[VOWELS_LOWER.find(char)]
                transpose_dict[char.upper()] = vowels_permutation[VOWELS_LOWER.find(char)].upper()
            else:
                transpose_dict[char] = char
                transpose_dict[char.upper()] = char.upper()
        
        return transpose_dict

    def apply_transpose(self, transpose_dict):
        '''
        transpose_dict (dict): a transpose dictionary
        
        Returns: an encrypted version of the message text, based 
        on the dictionary
        '''

        transposed_message = []
        for element in list(self.get_message_text()):
            # Uses 'get' returning as default the same element as in the
            # original message in case it does not exist in the dictionary
            # (e.g. ' ', '.', ',' etc.)
            transposed_message.append(transpose_dict.get(element, element)) 
        
        return ''.join(transposed_message)
        
class EncryptedSubMessage(SubMessage):
    def __init__(self, text):
        '''
        Initializes an EncryptedSubMessage object

        text (string): the encrypted message text

        An EncryptedSubMessage object inherits from SubMessage and has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        SubMessage.__init__(self, text)

    def decrypt_message(self):
        '''
        Attempt to decrypt the encrypted message 
        
        Idea is to go through each permutation of the vowels and test it
        on the encrypted message. For each permutation, check how many
        words in the decrypted text are valid English words, and return
        the decrypted message with the most English words.
        
        If no good permutations are found (i.e. no permutations result in 
        at least 1 valid word), return the original string. If there are
        multiple permutations that yield the maximum number of words, return any
        one of them.

        Returns: the best decrypted message    
        
        Hint: use your function from Part 4A
        '''
        possible_comb = get_permutations('aeiou')
        possible_msg_dict = {}
        
        # Build all possible messages and store in a dict
        for comb in possible_comb:
            possible_msg_dict[comb] = self.apply_transpose(self.build_transpose_dict(comb))
    
        highest_valid_words = 0
        # Count valid words for possible message
        for comb in possible_msg_dict:
            number_valid_words = 0
            for word in possible_msg_dict[comb].split():
                if is_word(self.get_valid_words(), word):
                    number_valid_words += 1
                    
            if number_valid_words > highest_valid_words:
                highest_valid_words = number_valid_words
                best_decrypted_msg = possible_msg_dict[comb]
        
        return best_decrypted_msg
                    
                    
if __name__ == '__main__':

    # Example test case
    message = SubMessage("Hello World!")
    permutation = "eaiuo"
    enc_dict = message.build_transpose_dict(permutation)
    print("Original message:", message.get_message_text(), "Permutation:", permutation)
    print("Expected encryption:", "Hallu Wurld!")
    print("Actual encryption:", message.apply_transpose(enc_dict))
    enc_message = EncryptedSubMessage(message.apply_transpose(enc_dict))
    print("Decrypted message:", enc_message.decrypt_message())
    
    print('-' * 50)    
    
    message_2 = SubMessage("Sweeping an agile leopard")
    permutation = "iueoa"
    enc_dict = message_2.build_transpose_dict(permutation)
    print("Original message:", message_2.get_message_text(), "Permutation:", permutation)
    print("Encrypted message:", message_2.apply_transpose(enc_dict))
    enc_message_2 = EncryptedSubMessage(message_2.apply_transpose(enc_dict))
    print("Decrypted message:", enc_message_2.decrypt_message())
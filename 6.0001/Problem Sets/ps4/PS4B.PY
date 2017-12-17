# Problem Set 4B
# Name: Ignacio Paricio
# Collaborators:
# Time Spent: 1:15

import string

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
    word = word.strip(" !@#$%^&*()-_+={}[]|\:;'<>?,./\"")
    return word in word_list

def get_story_string():
    """
    Returns: a story in encrypted text.
    """
    f = open("story.txt", "r")
    story = str(f.read())
    f.close()
    return story

### END HELPER CODE ###

WORDLIST_FILENAME = 'words.txt'

class Message(object):
    def __init__(self, text):
        '''
        Initializes a Message object
                
        text (string): the message's text

        a Message object has two attributes:
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

    def build_shift_dict(self, shift):
        '''
        Creates a dictionary that can be used to apply a cipher to a letter.
        The dictionary maps every uppercase and lowercase letter to a
        character shifted down the alphabet by the input shift. The dictionary
        should have 52 keys of all the uppercase letters and all the lowercase
        letters only.        
        
        shift (integer): the amount by which to shift every letter of the 
        alphabet. 0 <= shift < 26

        Returns: a dictionary mapping a letter (string) to 
                 another letter (string). 
        '''
        alph_lower = list(string.ascii_lowercase) # abcdefghijklmnopqrstuvwxyz
        alph_upper = list(string.ascii_uppercase) # ABCDEFGHIJKLMNOPQRSTUVWXYZ
        
        shift_dict = {} 
        for char in alph_lower:
            if (shift + alph_lower.index(char)) < 26:
                shift_dict[char] = alph_lower[alph_lower.index(char) + shift]
            else:
                shift_dict[char] = alph_lower[alph_lower.index(char) + shift - 26]
                
        for char in alph_upper:
            if (shift + alph_upper.index(char)) < 26:
                shift_dict[char] = alph_upper[alph_upper.index(char) + shift]
            else:
                shift_dict[char] = alph_upper[alph_upper.index(char) + shift - 26]
                
        return shift_dict

    def apply_shift(self, shift):
        '''
        Applies the Caesar Cipher to self.message_text with the input shift.
        Creates a new string that is self.message_text shifted down the
        alphabet by some number of characters determined by the input shift        
        
        shift (integer): the shift with which to encrypt the message.
        0 <= shift < 26

        Returns: the message text (string) in which every character is shifted
             down the alphabet by the input shift
        '''
        shift_dict = self.build_shift_dict(shift)
        
        unciphered_message = list(self.get_message_text())
        ciphered_message = []
        
        for element in unciphered_message:
            # Uses 'get' returning as default the same element as in the
            # original message in case it does not exist in the dictionary
            # (e.g. ' ', '.', ',' etc.)
            ciphered_message.append(shift_dict.get(element, element)) 
        
        return ''.join(ciphered_message)
        

class PlaintextMessage(Message):
    def __init__(self, text, shift):
        '''
        Initializes a PlaintextMessage object        
        
        text (string): the message's text
        shift (integer): the shift associated with this message

        A PlaintextMessage object inherits from Message and has five attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
            self.shift (integer, determined by input shift)
            self.encryption_dict (dictionary, built using shift)
            self.message_text_encrypted (string, created using shift)

        '''
        Message.__init__(self, text)
        self.shift = shift
        self.encryption_dict = Message.build_shift_dict(self, shift)
        self.message_text_encrypted = Message.apply_shift(self, shift)

    def get_shift(self):
        '''
        Used to safely access self.shift outside of the class
        
        Returns: self.shift
        '''
        return self.shift

    def get_encryption_dict(self):
        '''
        Used to safely access a copy self.encryption_dict outside of the class
        
        Returns: a COPY of self.encryption_dict
        '''
        return self.encryption_dict

    def get_message_text_encrypted(self):
        '''
        Used to safely access self.message_text_encrypted outside of the class
        
        Returns: self.message_text_encrypted
        '''
        return self.message_text_encrypted

    def change_shift(self, shift):
        '''
        Changes self.shift of the PlaintextMessage and updates other 
        attributes determined by shift.        
        
        shift (integer): the new shift that should be associated with this message.
        0 <= shift < 26

        Returns: nothing
        '''
        current_shift = self.get_shift()
        self.shift = shift
        self.encryption_dict = Message.build_shift_dict(self, shift)
        self.message_text_encrypted = Message.apply_shift(self, shift)
        
        return 'Shift changed from {} to {}'.format(current_shift, shift)


class CiphertextMessage(Message):
    def __init__(self, text):
        '''
        Initializes a CiphertextMessage object
                
        text (string): the message's text

        a CiphertextMessage object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        Message.__init__(self, text)

    def decrypt_message(self):
        '''
        Decrypt self.message_text by trying every possible shift value
        and find the "best" one. We will define "best" as the shift that
        creates the maximum number of real words when we use apply_shift(shift)
        on the message text. If s is the original shift value used to encrypt
        the message, then we would expect 26 - s to be the best shift value 
        for decrypting it.

        Note: if multiple shifts are equally good such that they all create 
        the maximum number of valid words, you may choose any of those shifts 
        (and their corresponding decrypted messages) to return

        Returns: a tuple of the best shift value used to decrypt the message
        and the decrypted message text using that shift value
        '''
        #encrypted_msg = self.message_text
        possible_msg = {}
        best_message = None
        best_decryption_shift = None
        
        # Get a dictionary with decryption shifts as keys
        for shift in range(0,26):          
            possible_msg[shift] = self.apply_shift(shift)
            
        highest_valid_words = 0  
        # Count valid words for each shift                 
        for shift in range(0,26):           
            number_valid_words = 0
            for word in possible_msg[shift].split():
                if is_word(self.get_valid_words(), word):
                    number_valid_words += 1
                    
            # If there is a new highest number of valid words, then store     
            if number_valid_words > highest_valid_words:
                highest_valid_words = number_valid_words
                best_decryption_shift = shift
                best_message = possible_msg[shift]
        
        return best_decryption_shift, best_message
            
    

if __name__ == '__main__':

#    #Example test case (PlaintextMessage)
#    plaintext = PlaintextMessage('hello', 2)
#    print('Expected Output: jgnnq')
#    print('Actual Output:', plaintext.get_message_text_encrypted())
#
#    #Example test case (CiphertextMessage)
#    ciphertext = CiphertextMessage('jgnnq')
#    print('Expected Output:', (24, 'hello'))
#    print('Actual Output:', ciphertext.decrypt_message())

    #TODO: WRITE YOUR TEST CASES HERE

    #TODO: best shift value and unencrypted story 
#    my_message = PlaintextMessage('this is a Sample test', 0)
#    print('shift =', my_message.get_shift())
#    print('dict =', my_message.get_encryption_dict())
#    print('encrypted =', my_message.get_message_text_encrypted())
#    print(my_message.change_shift(1))
#    print('encrypted =', my_message.get_message_text_encrypted())
    my_decrypted_msg = CiphertextMessage('Xoqy Tzcfsm wg o amhvwqoz qvofoqhsf qfsohsr cb hvs gdif ct o acasbh hc vszd qcjsf ob wbgittwqwsbhzm dzobbsr voqy. Vs vog pssb fsuwghsfsr tcf qzoggsg oh AWH hkwqs pstcfs, pih vog fsdcfhsrzm bsjsf doggsr oqzogg. Wh vog pssb hvs hforwhwcb ct hvs fsgwrsbhg ct Sogh Qoadig hc psqcas Xoqy Tzcfsm tcf o tsk bwuvhg soqv msof hc sriqohs wbqcawbu ghirsbhg wb hvs komg, asobg, obr shvwqg ct voqywbu.')
    print(my_decrypted_msg.decrypt_message())
    
#    pass #delete this line and replace with your code here

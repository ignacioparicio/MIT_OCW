# Problem Set 2, hangman.py
# Name: 
# Collaborators:
# Time spent:

# Hangman Game
# -----------------------------------
# Helper code
# You don't need to understand this helper code,
# but you will have to know how to use the functions
# (so be sure to read the docstrings!)
import random
import string

WORDLIST_FILENAME = "words.txt"


def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print("  ", len(wordlist), "words loaded.")
    return wordlist



def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)
    
    Returns a word from wordlist at random
    """
    return random.choice(wordlist)

# end of helper code

# -----------------------------------

# Load the list of words into the variable wordlist
# so that it can be accessed from anywhere in the program
wordlist = load_words()


def is_word_guessed(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing; assumes all letters are
      lowercase
    letters_guessed: list (of letters), which letters have been guessed so far;
      assumes that all letters are lowercase
    returns: boolean, True if all the letters of secret_word are in letters_guessed;
      False otherwise
    '''
    # Get unique charts in the secret word
    secret_word_unique=list(set(secret_word))
    is_word_guessed=False
    for char in secret_word_unique:
        if not char in letters_guessed:
            return is_word_guessed
    is_word_guessed=True
    return is_word_guessed


def get_guessed_word(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters, underscores (_), and spaces that represents
      which letters in secret_word have been guessed so far.
    '''
    current_guess=[]
    for char in secret_word:
        if char in letters_guessed:
            current_guess.append(char)
        else:
            current_guess.append('_ ')
            
    # Transform list of letters into string and return it
    return ''.join(current_guess)


def get_available_letters(letters_guessed):
    '''
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which letters have not
      yet been guessed.
    '''
    import string
    
    available_letters=[]
    
    for char in string.ascii_lowercase:
        if char not in letters_guessed:
            available_letters.append(char)
    
    return ''.join(available_letters)


def hangman(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how manar
    r
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses

    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Remember to make
      sure that the user puts in a letter!
    
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
    
    Follows the other limitations detailed in the problem write-up.
    '''
    print('\n')
    print('Welcome to the game Hangman!')
    print('I am thinking of a word that is', len(secret_word), 'letters long.')
    print('\n')
    
    guesses=6
    warnings=3
    letters_guessed=[]
    previous_guessed_word=get_guessed_word(secret_word, letters_guessed)
    
    while guesses>0:
        
        print('-'*50)
        print('You have', guesses, 'guesses left.')
        print('Available letters:', get_available_letters(letters_guessed))
        new_letter=input('Please guess a letter: ').lower()
        
        
        # Handling for warnings if letter was already tried or if input is not valid
        if new_letter in letters_guessed and new_letter.isalpha():
            warnings-=1
            if warnings != 0:
                print('You already tried that letter! You have', warnings,
                      'warnings left before lossing a guess!')
            else:
                guesses-=1
                warnings=3
                print('You already tried that letter! You reached 3 warnings and',
                'lost a guess! You have', guesses,'guesses left')
            continue
        elif not new_letter.isalpha():
            warnings-=1
            if warnings != 0:
                print('That is not a valid letter! You have', warnings,
                      'warnings left before lossing a guess!')
            else:
                guesses-=1
                warnings=3
                print('That is not a valid letter! You reached 3 warnings and',
                'lost a guess! You have', guesses,'guesses left')
            continue           

        letters_guessed.append(new_letter)
        
        # Break if the user has won
        if is_word_guessed(secret_word, letters_guessed):
            print('\n')
            print('*'*70)
            print("Congratulations! You won! The secret word was'" + secret_word +"'")
            print("Your total score for this game is", len(secret_word)*guesses)
            print('*'*70,'\n')
            return None
        
        guessed_word=get_guessed_word(secret_word, letters_guessed)
        
        if guessed_word==previous_guessed_word:
            print('Oops! That letter is not in my word:', guessed_word)
            if new_letter in ('a', 'e', 'i', 'o', 'u'):
                guesses-=2
            else:
                guesses-=1
        else:
            print('Good guess:', guessed_word)
                            
        previous_guessed_word=guessed_word
    
    print('\n')
    print('*'*70)
    print("Game over! The secret word was '" + secret_word +"'")
    print('*'*70,'\n')           



# When you've completed your hangman function, scroll down to the bottom
# of the file and uncomment the first two lines to test
#(hint: you might want to pick your own
# secret_word while you're doing your own testing)


def match_with_gaps(my_word, other_word):
    '''
    my_word: string with _ characters, current guess of secret word
    other_word: string, regular English word
    returns: boolean, True if all the actual letters of my_word match the 
        corresponding letters of other_word, or the letter is the special symbol
        _ , and my_word and other_word are of the same length;
        False otherwise: 
    '''
    # Compare lengths taking out spaces in 'my_word' due to the '_ ' structure
    if not len(other_word) == (len(my_word) - my_word.count(' ')):
        return False
        
    # Get unique characters in my_word
    unique_chars = ''.join(set(my_word))

    counter_other_word = 0
    for char in my_word:
        # Skip spaces
        if char == ' ':
            continue
        else:
            # Case in which a letter is given
            if char != '_' and char != other_word[counter_other_word]:
                return False
            # Case in which there is a blank. Must not be a character already guessed
            elif char == '_' and other_word[counter_other_word] in unique_chars:
                return False
        counter_other_word += 1
    
    return True

def show_possible_matches(my_word):
    '''
    my_word: string with _ characters, current guess of secret word
    returns: nothing, but should print out every word in wordlist that matches my_word
             Keep in mind that in hangman when a letter is guessed, all the positions
             at which that letter occurs in the secret word are revealed.
             Therefore, the hidden letter(_ ) cannot be one of the letters in the word
             that has already been revealed.

    '''
    match_found = False
    for word in wordlist:
        if match_with_gaps(my_word, word):
            if match_found == False:
                print('Possible word matches are:', end = ' ')
            match_found = True            
            print(word, end = ' ')
    if match_found:
        print('')
    else:
        print('No matches found')
            

def hangman_with_hints(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses
    
    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Make sure to check that the user guesses a letter
      
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
      
    * If the guess is the symbol *, print out all words in wordlist that
      matches the current guessed word. 
    
    Follows the other limitations detailed in the problem write-up.
    '''
    print('\n')
    print('Welcome to the game Hangman! (with hints)')
    print("Playing this version, you can give '*' as an input to get hints!")
    print('I am thinking of a word that is', len(secret_word), 'letters long.')
    print('\n')
    
    guesses=6
    warnings=3
    letters_guessed=[]
    previous_guessed_word=get_guessed_word(secret_word, letters_guessed)
    
    while guesses>0:
        
        print('-'*50)
        print('You have', guesses, 'guesses left.')
        print('Available letters:', get_available_letters(letters_guessed))
        new_letter = input('Please guess a letter: ').lower()
        
        if new_letter == '*':
            show_possible_matches(previous_guessed_word)
            continue
        
        # Handling for warnings if letter was already tried or if input is not valid
        if new_letter in letters_guessed and new_letter.isalpha():
            warnings-=1
            if warnings != 0:
                print('You already tried that letter! You have', warnings,
                      'warnings left before lossing a guess!')
            else:
                guesses-=1
                warnings=3
                print('You already tried that letter! You reached 3 warnings and',
                'lost a guess! You have', guesses,'guesses left')
            continue
        elif not new_letter.isalpha():
            warnings-=1
            if warnings != 0:
                print('That is not a valid letter! You have', warnings,
                      'warnings left before lossing a guess!')
            else:
                guesses-=1
                warnings=3
                print('That is not a valid letter! You reached 3 warnings and',
                'lost a guess! You have', guesses,'guesses left')
            continue           

        letters_guessed.append(new_letter)
        
        # Break if the user has won
        if is_word_guessed(secret_word, letters_guessed):
            print('\n')
            print('*'*70)
            print("Congratulations! You won! The secret word was'" + secret_word +"'")
            print("Your total score for this game is", len(secret_word)*guesses)
            print('*'*70,'\n')
            return None
        
        guessed_word=get_guessed_word(secret_word, letters_guessed)
        
        if guessed_word==previous_guessed_word:
            print('Oops! That letter is not in my word:', guessed_word)
            if new_letter in ('a', 'e', 'i', 'o', 'u'):
                guesses-=2
            else:
                guesses-=1
        else:
            print('Good guess:', guessed_word)
                            
        previous_guessed_word=guessed_word
    
    print('\n')
    print('*'*70)
    print("Game over! The secret word was '" + secret_word +"'")
    print('*'*70,'\n')           



# When you've completed your hangman_with_hint function, comment the two similar
# lines above that were used to run the hangman function, and then uncomment
# these two lines and run this file to test!
# Hint: You might want to pick your own secret_word while you're testing.


if __name__ == "__main__":

    # To test part 2, comment out the pass line above and
    # uncomment the following two lines.
    
    #secret_word = choose_word(wordlist)
    #hangman(secret_word)

###############
    
    # To test part 3 re-comment out the above lines and 
    # uncomment the following two lines. 
    
    secret_word = choose_word(wordlist)
    hangman_with_hints(secret_word)
    
    
# ---------------------- TEST --------------------
    
#secret_word = 'apple'
#letters_guessed = ['e', 'i', 'k', 'p', 'r', 's']
#print('is_word_guessed = ', is_word_guessed(secret_word, letters_guessed) )
#print('get_guessed_word = ',get_guessed_word(secret_word, letters_guessed) )   
#print('get_available_letters =', get_available_letters(letters_guessed))
# -----------------------------------------------
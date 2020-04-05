# Problem Set 2
# Name: Paulo Quilao
# Collaborators: none
# Time spent: start: very long

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

    print(line)


def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)

    Returns a word from wordlist at random
    """
    return random.choice(wordlist)


def get_len_word(secretword):
    """
    secretword: string
    return: length of unique letters of secret word
    """
    unique_letters_secret_word = set(secret_word)
    len_secret_word = len(unique_letters_secret_word)
    return len_secret_word

# end of helper code

# -----------------------------------


# Load the list of words into the variable WORDLIST_FILENAME
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

    #  empty list to store every letter in secret_word
    secret_word_list = []
    #  loop for appending each letter to secret_word_list
    for letter in secret_word:
        secret_word_list.append(letter)

    #  empty list to store letters in secret_word_list to
    common_letters = []
    #  iterates each letter common in secret_word_list to passed argument letters_guessed
    for letter in secret_word:  # note that secret_word_list can also be used in this block
        if letter in letters_guessed:
            common_letters.append(letter)

    #  checks if sorted list of common letters and list of secret word have the same items
    if sorted(common_letters) == sorted(secret_word_list):
        return True
    else:
        return False


def get_guessed_word(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters, underscores (_), and spaces that represents
      which letters in secret_word have been guessed so far.
    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    #  every guessed letter will be concatenated to this string
    word = ''
    for letter in secret_word:
        if letter in letters_guessed:
            word += letter
        else:
            word += '_ '
    return word


def get_available_letters(letters_guessed):
    '''
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which letters have not
      yet been guessed.
    '''

    #  variable for letter a to z in lower case
    alphabet = string.ascii_lowercase
    #  string where available letters will be concatenated
    available_letters = ''

    for letter in alphabet:
        if letter not in letters_guessed:
            available_letters += letter
    return available_letters


def hangman(secret_word):
    '''
    secret_word: string, the secret word to guess.

    Starts up an interactive game of Hangman.

    * At the start of the game, let the user know how many
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

#  start guessing
    letters_guessed = []
    letters_guessed_clone = []
    len_secret_word = len(secret_word)
    # this variable is crucial so that letters_guessed_clone list will start storing values (letters) in the 2nd loop
    loop = 0
    num_guesses_remaining = 6
    warnings = 3
    print("Welcome to the game Hangman!")
    print("I am thinking of a word that is {} letters long.".format(len_secret_word))
    print("Accummulating three warnings will lose you a guess.\n")
    print("-------------------------------------------")

    while num_guesses_remaining > 0:
        print("Secret word:", secret_word)
        #  display number of guess/guesses
        if num_guesses_remaining > 1:
            print("You have {} guesses left. Good luck!".format(
                num_guesses_remaining))
        else:
            print("You have {} guess left. Good luck!".format(
                num_guesses_remaining))
        #  display available letters
        print("Available letters:", get_available_letters(letters_guessed))
        #  store user input to variable letter
        letter = str(input("Guess a letter: ")).lower()
        print()
        #  if input is valid, i.e. letters only
        if str.isalpha(letter):
            if len(letter) > 1:
                print("Please enter one letter at a time.")
            if len(letter) == 1:
                #  append single input letter
                letters_guessed.append(letter)
                #  check if a letter was correctly guessed
                #  check if correct letters were already entered by the user
                if letter in secret_word:
                    #  executes if a letter was guessed in the 1st loop, loop = 0
                    if loop == 0:
                        #  prints the guess letter for the 1st try
                        print("Good guess:", get_guessed_word(
                            secret_word, letters_guessed))
                    #  gets a warning if input letter was already entered
                    #  initialized in the 2nd loop since a guessed letter will always be present in the letters_guessed list
                    #  executes if a letter was guessed in the succeeding loops, 2nd to n
                    if loop >= 1:
                        #  previously entered letter is appended to letters_guessed_clone list
                        letters_guessed_clone.append(
                            letters_guessed[len(letters_guessed) - 2])
                        #  if the next input letter is in the letters_guessed_clone, it will flag a warning
                        if letter in letters_guessed_clone:
                            if warnings > 0:
                                warnings -= 1
                                print(
                                    "You have already guessed that letter.", end=" ")
                                if warnings == 1 or warnings == 0:
                                    print(
                                        "You now have {} warning left: ".format(warnings))
                                else:
                                    print(
                                        "You now have {} warnings left: ".format(warnings))
                                print("Word to guess:", get_guessed_word(
                                    secret_word, letters_guessed))
                            else:
                                num_guesses_remaining -= 1
                                print(
                                    "You have no warnings left. Sorry, you will lose a guess.")
                        else:
                            print("Good guess:", get_guessed_word(
                                secret_word, letters_guessed))
                #  wrong guess
                else:
                    print("Sorry, that letter is not in my word: ",
                          get_guessed_word(secret_word, letters_guessed))
                    #  lose 2 guesses if input letter is vowel and not in the secret word
                    if letter in "aeiou":
                        num_guesses_remaining -= 2
                        print(
                            "You entered a vowel letter, that will cost you 2 guesses.")
                    #  lose 1 guess if input letter is consonant and not in the secret word
                    else:
                        num_guesses_remaining -= 1
                        print(
                            "You entered a consonant letter, you will lose a guess.")
        #  extra warnings
        #  gets a warning if nonalphabet character was entered.
        if not str.isalpha(letter):
            if warnings > 0:
                warnings -= 1
                print("Invalid input. Please enter letters only.", end=" ")
                if warnings == 1 or warnings == 0:
                    print("You now have {} warning left: ".format(warnings))
                else:
                    print("You now have {} warnings left: ".format(warnings))
                print("Word to guess:", get_guessed_word(
                    secret_word, letters_guessed))
            else:
                num_guesses_remaining -= 1
                print("You have no warnings left. Sorry, you will lose a guess.")
        #  lose a guess if commited three warnings
        if warnings < 0:
            num_guesses_remaining -= 1
            print("You have no warnings left. Sorry, you will lose a guess.")
        #  check if the word is already guessed
        if is_word_guessed(secret_word, letters_guessed):
            print("\nCongrats! You guessed my word.")
            print("Your total score: {}".format(
                num_guesses_remaining * get_len_word(secret_word)))
            break
        #  increment loop by 1
        loop += 1
        #  next guess
        print("-------------------------------------------")
    #  number of guesses is equal to zero
    else:
        print("Sorry you ran out of guesses. The word is {}.".format(secret_word))


# When you've completed your hangman function, scroll down to the bottom
# of the file and uncomment the first two lines to test
#(hint: you might want to pick your own
# secret_word while you're doing your own testing)


# -----------------------------------


def match_with_gaps(my_word, other_word):
    '''
    my_word: string with _ characters, current guess of secret word
    other_word: string, regular English word
    returns: boolean, True if all the actual letters of my_word match the
        corresponding letters of other_word, or the letter is the special symbol
        _ , and my_word and other_word are of the same length;
        False otherwise:
    '''

    my_word = my_word.replace(" ", "")
    test_word = ""
    #  test for similarity in length
    if len(other_word) == len(my_word):
        #  test for similarity in characters and character position
        for char in other_word:
            if char in my_word:
                test_word += char
            else:
                test_word += "_"
    else:
        return False
    #  test for similaroty between other_word and secret_word
    with_sim_char = False
    #  get the index of character "_"
    hidden_letter_index = [pos for pos,
                           char in enumerate(test_word) if char == "_"]
    #  if secret_word and other_word have the same unreaveled characters, not valid for possible matches
    for i in hidden_letter_index:
        if other_word[i] == secret_word[i]:
            with_sim_char = True
    #  test for similarity between my_word and other_word, and other_word and secret_word
    if test_word == my_word and with_sim_char == False:
        return True
    else:
        return False


def show_possible_matches(my_word):
    '''
    my_word: string with _ characters, current guess of secret word
    returns: nothing, but should print out every word in wordlist that matches my_word
             Keep in mind that in hangman when a letter is guessed, all the positions
             at which that letter occurs in the secret word are revealed.
             Therefore, the hidden letter(_) cannot be one of the letters in the word
             that has already been revealed.

    '''
    #  list to store possible matches
    possible_matches = []
    #  iterate each word in the list wordlist
    for other_word in wordlist:
        #  each matched word is stored in the list possible_mataches
        if match_with_gaps(my_word, other_word):
            possible_matches.append(other_word)
    #  inform the user if no match was found
    if len(possible_matches) > 1:
        print("Possible words are:")
        #  display mactched words in a string manner
        print(" ".join(possible_matches))
    else:
        print("Sorry, no matches found.")


def hangman_with_hints(secret_word):
    '''
    secret_word: string, the secret word to guess.

    Starts up an interactive game of Hangman.

    * At the start of the game, let the user know how many
      letters the secret_word contains and how many guesses s / he starts with.

    * The user should start with 6 guesses

    * Before each round, you should display to the user how many guesses
      s / he has left and the letters that the user has not yet guessed.

    * Ask the user to supply one guess per round. Make sure to check that the user guesses a letter

    * The user should receive feedback immediately after each guess
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the
      partially guessed word so far.

    * If the guess is the symbol *, print out all words in wordlist that
      matches the current guessed word.

    Follows the other limitations detailed in the problem write - up.
    '''

    #  start guessing
    letters_guessed = []
    letters_guessed_clone = []
    len_secret_word = len(secret_word)
    #  trigger to show possible matches
    exemption = "*"
    # this variable is crucial so that letters_guessed_clone list will start storing values (letters) in the 2nd loop
    loop = 0
    num_guesses_remaining = 6
    warnings = 3
    print("Welcome to the game Hangman!")
    print("I am thinking of a word that is {} letters long.".format(len_secret_word))
    print("Accummulating three warnings will lose you a guess.\n")
    print("-------------------------------------------")

    while num_guesses_remaining > 0:
        # print("Secret word:", secret_word) #  uncomment for debugging
        #  display number of guess/guesses
        if num_guesses_remaining > 1:
            print("You have {} guesses left. Good luck!".format(
                num_guesses_remaining))
        else:
            print("You have {} guess left. Good luck!".format(
                num_guesses_remaining))
        #  display available letters
        print("Available letters:", get_available_letters(letters_guessed))
        #  store user input to variable letter
        letter = str(input("Guess a letter: ")).lower()
        #  if input is asterisk, show_possible_matches() function is executed
        if letter == "*":
            show_possible_matches(get_guessed_word(
                secret_word, letters_guessed))
        print()
        #  if input is valid, i.e. letters only
        if str.isalpha(letter):
            if len(letter) > 1:
                print("Please enter one letter at a time.")
            if len(letter) == 1:
                #  append single input letter
                letters_guessed.append(letter)
                #  check if a letter was correctly guessed
                #  check if correct letters were already entered by the user
                if letter in secret_word:
                    #  executes if a letter was guessed in the 1st loop, loop = 0
                    if loop == 0:
                        #  prints the guess letter for the 1st try
                        print("Good guess:", get_guessed_word(
                            secret_word, letters_guessed))
                    #  gets a warning if input letter was already entered
                    #  initialized in the 2nd loop since a guessed letter will always be present in the letters_guessed list
                    #  executes if a letter was guessed in the succeeding loops, 2nd to n
                    if loop >= 1:
                        #  previously entered letter is appended to letters_guessed_clone list
                        letters_guessed_clone.append(
                            letters_guessed[len(letters_guessed) - 2])
                        #  if the next input letter is in the letters_guessed_clone, it will flag a warning
                        if letter in letters_guessed_clone:
                            if warnings > 0:
                                warnings -= 1
                                print(
                                    "You have already guessed that letter.", end=" ")
                                if warnings == 1 or warnings == 0:
                                    print(
                                        "You now have {} warning left: ".format(warnings))
                                else:
                                    print(
                                        "You now have {} warnings left: ".format(warnings))
                                print("Word to guess:", get_guessed_word(
                                    secret_word, letters_guessed))
                            else:
                                num_guesses_remaining -= 1
                                print(
                                    "You have no warnings left. Sorry, you will lose a guess.")
                        else:
                            print("Good guess:", get_guessed_word(
                                secret_word, letters_guessed))
                #  wrong guess
                else:
                    print("Sorry, that letter is not in my word: ",
                          get_guessed_word(secret_word, letters_guessed))
                    #  lose 2 guesses if input letter is vowel and not in the secret word
                    if letter in "aeiou":
                        num_guesses_remaining -= 2
                        print(
                            "You entered a vowel letter, that will cost you 2 guesses.")
                    #  lose 1 guess if input letter is consonant and not in the secret word
                    else:
                        num_guesses_remaining -= 1
                        print(
                            "You entered a consonant letter, you will lose a guess.")
        #  extra warnings
        #  gets a warning if nonalphabet character was entered.
        if not str.isalpha(letter) and letter != exemption:
            if warnings > 0:
                warnings -= 1
                print("Invalid input. Please enter letters only.", end=" ")
                if warnings == 1 or warnings == 0:
                    print("You now have {} warning left: ".format(warnings))
                else:
                    print("You now have {} warnings left: ".format(warnings))
                print("Word to guess:", get_guessed_word(
                    secret_word, letters_guessed))
            else:
                num_guesses_remaining -= 1
                print("You have no warnings left. Sorry, you will lose a guess.")
        #  lose a guess if commited three warnings
        if warnings < 0:
            num_guesses_remaining -= 1
            print("You have no warnings left. Sorry, you will lose a guess.")
        #  check if the word is already guessed
        if is_word_guessed(secret_word, letters_guessed):
            print("\nCongrats! You guessed my word.")
            print("Your total score: {}".format(
                num_guesses_remaining * get_len_word(secret_word)))
            break
        #  increment loop by 1
        loop += 1
        #  next guess
        print("-------------------------------------------")
    #  number of guesses is equal to zero
    else:
        print("Sorry you ran out of guesses. The word is {}.".format(secret_word))


# When you've completed your hangman_with_hint function, comment the two similar
# lines above that were used to run the hangman function, and then uncomment
# these two lines and run this file to test!
# Hint: You might want to pick your own secret_word while you're testing.


if __name__ == "__main__":
    # pass

    # To test part 2, comment out the pass line above and
    # uncomment the following two lines.

    #secret_word = choose_word(wordlist)
    # hangman(secret_word)

    ###############

    # To test part 3 re-comment out the above lines and
    # uncomment the following two lines.

    secret_word = choose_word(wordlist)
    hangman_with_hints(secret_word)

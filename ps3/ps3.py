# 6.0001 Problem Set 3
#
# The 6.0001 Word Game
# Created by: Kevin Luu <luuk> and Jenna Wiens <jwiens>
#
# Name          : Paulo Quilao
# Collaborators : none
# Time spent    : also very long

import math
import random
import string

VOWELS = 'aeiou'
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
HAND_SIZE = 7

SCRABBLE_LETTER_VALUES = {
    'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1,
    'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1, 'o': 1, 'p': 3, 'q': 10, 'r': 1,
    's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10, '*': 0  # '*' for wildcard
}

# -----------------------------------
# Helper code
# (you don't need to understand this helper code)

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
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.append(line.strip().lower())
    print("  ", len(wordlist), "words loaded.")
    return wordlist


def get_frequency_dict(sequence):
    """
    Returns a dictionary where the keys are elements of the sequence
    and the values are integer counts, for the number of times that
    an element is repeated in the sequence.

    sequence: string or list
    return: dictionary
    """

    # freqs: dictionary (element_type -> int)
    freq = {}
    for x in sequence:
        freq[x] = freq.get(x, 0) + 1
    return freq


# (end of helper code)
# -----------------------------------


#
# Problem #1: Scoring a word
#


def get_word_score(word, n):
    """
    Returns the score for a word. Assumes the word is a
    valid word.

    You may assume that the input word is always either a string of letters,
    or the empty string "". You may not assume that the string will only contain
    lowercase letters, so you will have to handle uppercase and mixed case strings
    appropriately.

        The score for a word is the product of two components:

        The first component is the sum of the points for letters in the word.
        The second component is the larger of:
            1, or
            7*wordlen - 3*(n-wordlen), where wordlen is the length of the word
            and n is the hand length when the word was played

        Letters are scored as in Scrabble; A is worth 1, B is
        worth 3, C is worth 3, D is worth 2, E is worth 1, and so on.

    word: string
    n: int >= 0
    returns: int >= 0
    """

    score = []
    for letter in word:
        # add lower() to standardize keys
        score.append(SCRABBLE_LETTER_VALUES[letter.lower()])

    sum_score = sum(score)
    first_component = sum_score
    second_component = (7 * len(word) - 3 * (n - len(word)))

    #  if 2nd component is greater than one, proceed to the given eq'n
    if second_component > 1:
        total_score = first_component * second_component

    #  if 2nd component is less than one, replace it with one (1)
    elif second_component <= 1:
        total_score = first_component * 1

    #  return value
    return total_score


#
# Make sure you understand how this function works and what it does!
#

def display_hand(hand):
    """
    Displays the letters currently in the hand.

    For example:
       display_hand({'a':1, 'x':2, 'l':3, 'e':1})
    Should print out something like:
       a x x l l l e
    The order of the letters is unimportant.

    hand: dictionary (string -> int)
    """

    for letter in hand.keys():
        for j in range(hand[letter]):
            print(letter, end=' ')      # print all on the same line
    print()                              # print an empty line


#
# Make sure you understand how this function works and what it does!
# You will need to modify this for Problem #4.
#

def deal_hand(n):
    """
    Returns a random hand containing n lowercase letters.
    ceil(n/3) letters in the hand should be VOWELS (note,
    ceil(n/3) means the smallest integer not less than n/3).

    Hands are represented as dictionaries. The keys are
    letters and the values are the number of times the
    particular letter is repeated in that hand.

    n: int >= 0
    returns: dictionary (string -> int)
    """

    num_vowels = int(math.ceil(n / 3))

    #  add asterisk as wildcard
    hand['*'] = 1
    hand = {}
    for i in range(num_vowels - 1):  # minus 1 to acct for wildcard
        x = random.choice(VOWELS)
        hand[x] = hand.get(x, 0) + 1
        #  can also be written as the following lines
        # hand.setdefault(x, 0)
        # hand[x] += 1

    for i in range(num_vowels, n):  # to ensure sum of values will always be equal to n
        x = random.choice(CONSONANTS)
        hand[x] = hand.get(x, 0) + 1

    #  print n for debugging
    '''total = 0
    for value in hand.values():
        total += value
    print("n:", total)'''
    return hand

#
# Problem #2: Update a hand by removing letters
#


def update_hand(hand, word):
    """
    Does NOT assume that hand contains every letter in word at least as
    many times as the letter appears in word. Letters in word that don't
    appear in hand should be ignored. Letters that appear in word more times
    than in hand should never result in a negative count; instead, set the
    count in the returned hand to 0 (or remove the letter from the
    dictionary, depending on how your code is structured).

    Updates the hand: uses up the letters in the given word
    and returns the new hand, without those letters in it.

    Has no side effects: does not modify hand.

    word: string
    hand: dictionary (string -> int)
    returns: dictionary (string -> int)
    """

    #  make a copy of the hand to prevent mutating the original hand
    hand_clone = hand.copy()
    #  iterate each letter in the passed word argument
    #  passed word will always be in lower case
    for letter in word.lower():
        #  if letter in the given hand dictionary
        if letter in hand_clone.keys():
            #  value for that letter will be deducted by one
            hand_clone[letter] -= 1

    #  removes negative values in hand_clone
    for letter in hand_clone:
        if hand_clone[letter] < 0:
            hand_clone[letter] = 0

    #  return updated copy of hand dict
    return hand_clone

#
# Problem #3: Test word validity
#


def is_valid_word(word, hand, word_list):
    """
    Returns True if word is in the word_list and is entirely
    composed of letters in the hand. Otherwise, returns False.
    Does not mutate hand or word_list.

    word: string
    hand: dictionary (string -> int)
    word_list: list of lowercase strings
    returns: boolean
    """

    #  convert word to lower case since word_list contains lower case strings
    word = word.lower()
    #  clone hand dictionary to retain original values in hand dict
    hand_clone = hand.copy()

    #  create a dictionary from letters in passed word
    word_dict = {}
    #  to compare values in hand dictionary
    for letter in word:
        #  ensure keys are in lower case
        word_dict.setdefault(letter.lower(), 0)
        word_dict[letter.lower()] += 1

    #  solution A block
    #  executes if passed word exists in word_list and doesn't have a wildcard (*)
    if word in word_list and word.find("*") == -1:
        #  iterate each letter in word
        for letter in word:
            #  chech if letter in hand dictionary
            if letter in hand:
                #  update values in hand_clone by subtracting values of word_dict from values of hand_clone
                hand_clone[letter] = hand_clone[letter] - word_dict[letter]
            # if letter in word is not in hand dictionary, return False
            else:
                return False

    #  solution B block
    #  executes if passed word is not in word_list and contains a wildcard (*)
    elif word not in word_list and word.find("*") != -1:
        #  any matched word between the passed word replaced with a vowel
        #  and a word from the word_list will be appended to this list
        matched_word = []
        in_wordlist = False
        #  iterate each vowel in VOWELS constant
        for vowel in VOWELS:
            #  replace '*' with a vowel
            word_replace = word.replace("*", vowel)
            #  check if the passed replaced word is in word_list
            if word_replace in word_list:
                #  append the mached word in the matched_word list
                matched_word.append(word_list[word_list.index(word_replace)])
                #  trigger execution of matched word
                in_wordlist = True
        #  no matched word means the passed word is not in the word_list
        if len(matched_word) == 0:
            return False
        #  executes if the word replaced with an actual vowel is in word_list
        if in_wordlist:
            for letter in word:
                if letter in hand:
                    hand_clone[letter] = hand_clone[letter] - word_dict[letter]
                # if letter in word is not in hand dictionary, return False
                else:
                    return False

    #  did not met above conditions(i.e. word not in word_list)
    else:
        return False

    #  return False if any value in hand dictionary is less than 0
    #  this means that the word is not entirely created by available letters in hand
    for value in hand_clone.values():
        if value < 0:
            return False
        else:
            return True

#
# Problem #5: Playing a hand
#


def calculate_handlen(hand):
    """
    Returns the length (number of letters) in the current hand.

    hand: dictionary (string-> int)
    returns: integer
    """
    total = 0
    for value in hand.values():
        total += value

    return total


def play_hand(hand, word_list):
    """
    Allows the user to play the given hand, as follows:

    * The hand is displayed.

    * The user may input a word.

    * When any word is entered (valid or invalid), it uses up letters
      from the hand.

    * An invalid word is rejected, and a message is displayed asking
      the user to choose another word.

    * After every valid word: the score for that word is displayed,
      the remaining letters in the hand are displayed, and the user
      is asked to input another word.

    * The sum of the word scores is displayed when the hand finishes.

    * The hand finishes when there are no more unused letters.
      The user can also finish playing the hand by inputing two
      exclamation points (the string '!!') instead of a word.

      hand: dictionary (string -> int)
      word_list: list of lowercase strings
      returns: the total score for the hand

    """

    #  starting point
    total_points = 0
    running = True

    while running:
        print("Current Hand: ", end="")
        display_hand(hand)
        word = str(
            input(("Enter a word, or \"!!\" to indicate you are finished: "))).lower()
        if word == "!!":
            break

        #  initializes when the user inputs a word
        hand = update_hand(hand, word)
        #  executes if the input word is valid
        if is_valid_word(word, hand, word_list):
            print("\"{0}\" earned {1} points.".format(
                word, get_word_score(word, calculate_handlen(hand))), end=" ")
            total_points += get_word_score(word, calculate_handlen(hand))
            print("Total points for this hand: {}".format(total_points))
            print()
        #  executes when the input word is invalid
        else:
            print("\"{}\" is not a valid word. Please choose another word.".format(word))
            print()

        #  terminates the loop if hand has no more letters
        if calculate_handlen(hand) == 0:
            print("Ran out of letters. Total score for this hand: {}".format(
                total_points))
            running = False

    return total_points

#
# Problem #6: Playing a game
#


#
# procedure you will use to substitute a letter in a hand
#

def substitute_hand(hand, letter):
    """
    Allow the user to replace all copies of one letter in the hand (chosen by user)
    with a new letter chosen from the VOWELS and CONSONANTS at random. The new letter
    should be different from user's choice, and should not be any of the letters
    already in the hand.

    If user provide a letter not in the hand, the hand should be the same.

    Has no side effects: does not mutate hand.

    For example:
        substitute_hand({'h':1, 'e':1, 'l':2, 'o':1}, 'l')
    might return:
        {'h':1, 'e':1, 'o':1, 'x':2} -> if the new letter is 'x'
    The new letter should not be 'h', 'e', 'l', or 'o' since those letters were
    already in the hand.

    hand: dictionary (string -> int)
    letter: string
    returns: dictionary (string -> int)
    """

    #  different key, same value
    hand_clone = hand.copy()

    #  initialize random search from a to z using a list comprehension
    #  this ensures that the random searching does not include the original letter
    #  and randomly-searched letter does not exist in the hand
    alphabet = string.ascii_lowercase
    sub_letter = random.choice(
        [char for char in alphabet if char != letter and char not in hand])

    for key in hand:
        if letter == key:
            if sub_letter not in hand:
                hand_clone[sub_letter[0]] = hand[key]
                del(hand_clone[letter])

    return hand_clone


def play_game(word_list):
    """
    Allow the user to play a series of hands

    * Asks the user to input a total number of hands

    * Accumulates the score for each hand into a total score for the
      entire series

    * For each hand, before playing, ask the user if they want to substitute
      one letter for another. If the user inputs 'yes', prompt them for their
      desired letter. This can only be done once during the game. Once the
      substitue option is used, the user should not be asked if they want to
      substitute letters in the future.

    * For each hand, ask the user if they would like to replay the hand.
      If the user inputs 'yes', they will replay the hand and keep
      the better of the two scores for that hand.  This can only be done once
      during the game. Once the replay option is used, the user should not
      be asked if they want to replay future hands. Replaying the hand does
      not count as one of the total number of hands the user initially
      wanted to play.

            * Note: if you replay a hand, you do not get the option to substitute
                    a letter - you must play whatever hand you just had.

    * Returns the total score for the series of hands

    word_list: list of lowercase strings
    """

    #  substitute count, once per game
    sub_count = 1
    #  replay count
    replay_count = 1
    #  gets hand and hand size
    num_hands = int(input(("Enter total nnumber of hands: ")))
    hand = deal_hand(HAND_SIZE)
    #  if replay is already used, used initial hand for substitute loop
    initial_hand = hand
    #  display current hand to the user
    print("Current Hand: ", end=""), display_hand(hand)
    #  total score for all hands
    overall_points = 0

    while num_hands >= 1:
        #  score for each hand
        total_points_hand = 0

        #  loop for substituting a letter in hand
        while sub_count >= 1:
            #  executes when replay option is already used
            #  this is necessary since replay loop won't be executed again
            #  but num_hands should always be deducted by 1 after each round
            if replay_count == 0:
                num_hands -= 1
                hand = deal_hand(HAND_SIZE)
                print()
                print("Current Hand: ", end=""), display_hand(hand)
            #  ask the user for substitute
            answer_sub = input(
                "Type 'yes' to substitute a letter, 'no' otherwise: ").lower()
            #  executes subsitute_hand() function with the passed letter
            if answer_sub == 'yes':
                sub_count -= 1
                letter = input("Which letter would you like to replace: ")
                hand = substitute_hand(hand, letter)
                break
            #  terminate the loop
            elif answer_sub == 'no':
                break

        #  executes when replay option is already used
        #  this is necessary since replay loop won't be executed again
        #  but num_hands should always be deducted by 1 after each round
        if replay_count == 0:
            num_hands -= 1
            hand = deal_hand(HAND_SIZE)

        print()
        hand_score = play_hand(hand, word_list)

        while replay_count >= 1:
            #  print series of hyphens as divider
            print("----------------------------------------------")
            replay = input(
                "Type 'yes' to replay the hand, 'no' otherwise: ").lower()
            if replay == 'no':
                #  executed if the player wished to sub a letter in the 1st round
                #  sub_count loop won't be executed again so another hand should be dealt for the user
                if sub_count == 0:
                    hand = deal_hand(HAND_SIZE)
                while sub_count >= 1:
                    #  create new hand
                    hand = deal_hand(HAND_SIZE)
                    #  display current hand to the user in case of substitution
                    print("Current Hand: ", end=""), display_hand(hand)
                    print()
                    #  ask the user for substitute
                    answer_sub = input(
                        "Type 'yes' to substitute a letter, 'no' otherwise: ").lower()
                    #  executes subsitute_hand() function with the passed letter
                    if answer_sub == 'yes':
                        sub_count -= 1
                        letter = input(
                            "Which letter would you like to replace: ")
                        hand = substitute_hand(hand, letter)
                        break

                    elif answer_sub == 'no':
                        break

                #  deduct number of hands by 1 since a new hand will be played
                num_hands -= 1
                print()
                #  new variable for the returned total score of play_hand function
                new_hand_score = play_hand(hand, word_list)

            #  retain number of hands but replay option won't be executed again
            elif replay == 'yes':
                print()
                #  new variable for the returned total score of play_hand function
                new_hand_score = play_hand(hand, word_list)
                replay_count -= 1
                #  deduct the initial hand but not the replayed hand
                num_hands -= 1
                break
        #  get overall points for all hands
        overall_points += max(hand_score, new_hand_score)

    print("--------------------------")
    print("Total score overall hands: {}".format(overall_points))

    return overall_points


#
# Build data structures used for entire session and play game
# Do not remove the "if __name__ == '__main__':" line - this code is executed
# when the program is run directly, instead of through an import statement
#
if __name__ == '__main__':
    word_list = load_words()
    play_game(word_list)

# Problem Set 4C
# Name: Paulo Quilao
# Collaborators: none
# Time Spent: lonf

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

    # print("Loading word list from file...")
    # inFile: file
    inFile = open(file_name, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.extend([word.lower() for word in line.split(' ')])
    # print("  ", len(wordlist), "words loaded.")
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
        word_list = self.valid_words

        return word_list.copy()

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

        transpose_dict = {}
        #  iterate each letter in both cases
        for case in (VOWELS_LOWER, VOWELS_UPPER, CONSONANTS_LOWER, CONSONANTS_UPPER):
            for letter in case:
                for vowel in vowels_permutation:
                    if vowel in case:
                        #  add vowels in the dictionary that are not yet mapped
                        if vowel not in transpose_dict.values():
                            transpose_dict.setdefault(letter, vowel)
                #  map consonant letters to respective case and letter
                else:
                    transpose_dict.setdefault(letter, letter)

        return transpose_dict

    def apply_transpose(self, transpose_dict):
        '''
        transpose_dict (dict): a transpose dictionary

        Returns: an encrypted version of the message text, based
        on the dictionary
        '''

        transposed_text = ""

        #  iterate each char in passed argument
        for char in self.message_text:
            #  if character in mapped dictionary,
            #  get the value of that key
            if char in transpose_dict:
                transposed_text += transpose_dict[char]
            #  for white spaces and punctuations marks (does not exist in the dict),
            #  concatenate it with the transposed text
            else:
                transposed_text += char

        return transposed_text


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

        #  get the list of valid words
        word_list = self.get_valid_words()

        #  list of permutations of "aeiou"
        vowels_permutation = get_permutations("aeiou")

        # list of transposed dictionary of different vowel permutations
        transpose_dict_list = []
        for perm in vowels_permutation:
            transpose_dict_list.append(self.build_transpose_dict(perm))

        transpose_boolean = []
        decrypt_list = []
        #  iterate each dictionary of mapped permutations
        for dict_perm in transpose_dict_list:
            decrypt_text = self.apply_transpose(dict_perm)
            for word in decrypt_text.split():
                #  if decrypted word is valid (i.e. in provided word list),
                #  append 1 to Boolean list (i.e. True), 0 (False) otherwise
                if is_word(word_list, word):
                    transpose_boolean.append(1)
                else:
                    transpose_boolean.append(0)
            #  get the total of Boolean values to determine number of valid words
            decrypt_list.append((sum(transpose_boolean), decrypt_text))
            #  delete previous item for the next mapped vowel permutation
            del(transpose_boolean[:])
            #  get the list with the highest number of words
            decrypt_best = max(decrypt_list)

        #  solution for encrypted words with more than one possible decrypted version
        #  or for encrypted valid words counted as one word (i.e. connected by hyphen)
        possible_dec_message = []
        for item in decrypt_list:
            #  compare the total number of valid words of each tuple (item in list)
            #  to the tuple with the highest number of valid words in decypt_best
            #  to avoid repetition of decrypted text, add the second condition
            if item[0] == decrypt_best[0] and item[1] not in possible_dec_message:
                #  append the decrypted message
                possible_dec_message.append(item[1])

        decrypt_string = ""
        for message in possible_dec_message:
            decrypt_string += ", " + message

        #  return second to max index
        #  since a space and comma are in indices 0 and 1, respectively
        return decrypt_string[2:]


if __name__ == '__main__':

    #  Example test case
    print("Example test cases:")
    message = SubMessage("Hello World!")
    permutation = "eaiuo"
    enc_dict = message.build_transpose_dict(permutation)
    print("Original message:", message.get_message_text(),
          "Permutation:", permutation)
    print("Expected encryption: Hallu Wurld!")
    print("Actual encryption:", message.apply_transpose(enc_dict))
    enc_message = EncryptedSubMessage(message.apply_transpose(enc_dict))
    print("Decrypted message:", enc_message.decrypt_message())

    # TODO: WRITE YOUR TEST CASES HERE
    print("--------------------------------------")
    # Test case 1
    # with uppercase vowel permutation
    message = SubMessage('hElLO WORld!')
    permutation = "UEIAO"
    enc_dict = message.build_transpose_dict(permutation)
    print("Original message: {0}, Permutation: {1}".format(
        message.get_message_text(), permutation))
    print("Expected encryption: hElLA WARld!")
    print("Actual encryption:", message.apply_transpose(enc_dict))
    enc_message = EncryptedSubMessage(
        message.apply_transpose(enc_dict))
    print("Decrypted message:", enc_message.decrypt_message())
    print("--------------------------------------")
    # Test case 2
    # with 3 individual valid words
    message = SubMessage('Telepathic Youthfully Zoologist!')
    permutation = "aioue"
    enc_dict = message.build_transpose_dict(permutation)
    print("Original message: {0}, Permutation: {1}".format(
        message.get_message_text(), permutation))
    print("Expected encryption: Tilipathoc Yuethfelly Zuulugost")
    print("Actual encryption:", message.apply_transpose(enc_dict))
    enc_message = EncryptedSubMessage(
        message.apply_transpose(enc_dict))
    print("Decrypted message:", enc_message.decrypt_message())
    print("--------------------------------------")
    #  Test case 3
    #  with 2 valid words connected as one 'unstressed-waterproof'
    message = SubMessage('unstressed-waterproof watersheds')
    permutation = "uoeia"
    enc_dict = message.build_transpose_dict(permutation)
    print("Original message: {0}, Permutation: {1}".format(
        message.get_message_text(), permutation))
    print("Expected encryption: anstrossod wutorpriif wutorshods")
    print("Actual encryption:", message.apply_transpose(enc_dict))
    enc_message = EncryptedSubMessage(
        message.apply_transpose(enc_dict))
    print("Decrypted message:", enc_message.decrypt_message())

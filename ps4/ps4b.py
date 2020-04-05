# Problem Set 4B
# Name: Paulo Quilao
# Collaborators:
# Time Spent: long

import string
import pprint
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
        valid_words_clone = self.valid_words.copy()

        return valid_words_clone

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
        assert (0 <= shift) and (shift <= 26), "Invalid shift value"

        alphabet_lower = string.ascii_lowercase
        alphabet_upper = string.ascii_uppercase
        mapping_letter = {}

        for case in (alphabet_lower, alphabet_upper):
            for letter in case:
                #  if index >= 26, get the absolute difference between index and 26
                #  to return counting from letter 'a'
                if (case.index(letter) + shift) >= 26:
                    mapping_letter[letter] = case[abs((case.index(
                        letter) + shift) - 26)]
                else:
                    mapping_letter[letter] = case[case.index(
                        letter) + shift]

        return mapping_letter

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
        shift_text = ""

        # calling the method defined in the class
        mapping_letter = self.build_shift_dict(shift)

        for char in self.message_text:
            if char in mapping_letter:
                shift_text += mapping_letter[char]
            else:
                shift_text += char

        return shift_text


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
        self.encryption_dict = self.build_shift_dict(shift)
        self.message_text_encrypted = self.apply_shift(shift)

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
        mapping_letter_copy = self.build_shift_dict(shift)
        #  returns a copy of built shift dictionary
        return mapping_letter_copy

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
        self.shift = shift
        self.encryption_dict = self.build_shift_dict(shift)
        self.message_text_encrypted = self.apply_shift(shift)


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
        #  get word_list from the class method
        word_list = self.get_valid_words()

        decrypt_boolean = []
        decrypt_list = []
        for s in range(26):
            decrypt_text = self.apply_shift(s)
            for word in decrypt_text.split():
                if is_word(word_list, word):
                    #  if valid word, append 1 [Boolean: True(1)]
                    decrypt_boolean.append(1)
                else:
                    #  if invalud word, append 0 [Boolean: False(0)]
                    decrypt_boolean.append(0)
            #  append the total valid words, shift value, and the decrypted text
            decrypt_list.append(
                (sum(decrypt_boolean), s, decrypt_text))
            #  delete the items in decrypt_boolean for the next shift value
            del(decrypt_boolean[:])
            #  get the decrypted text with the highest number of valid words
            decrypt_best_shift = max(decrypt_list)
        #  return items in decrypt_best_shift starting from 1 to 3
        #  since indices 1 and 2 denote for shift value and decrypted text, respectively
        return decrypt_best_shift[1:3]


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

    # TODO: WRITE YOUR TEST CASES HERE
    print("Test case for encrypting: ")
    plaintext = PlaintextMessage('handsome', 10)
    print('Expected Output: rkxncywo')
    print('Actual Output:', plaintext.get_message_text_encrypted())
    print("-----------------------------")
    print("Test case for decrypting: ")
    ciphertext = CiphertextMessage('rkxncywo')
    print('Expected Output:', (16, 'handsome'))
    print('Actual Output:', ciphertext.decrypt_message())
    print("-----------------------------")
    # TODO: best shift value and unencrypted story
    story = get_story_string()
    print("Encrypted Story:")
    pprint.pprint(story)
    cipher = CiphertextMessage(story)
    print("Decrypted Story (shift value, story):")
    pprint.pprint(cipher.decrypt_message())

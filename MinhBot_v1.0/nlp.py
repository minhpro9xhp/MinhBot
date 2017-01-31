import nltk
import math
from nltk.corpus import words
#  A dictionary of commands
_dict = words.words()
_char_list = []
_word_range_list = []


def initialize_dict_bookmark():
    _list = nltk.corpus.words.words()

    _sub_list = []
    _char = '0'
    for token in _list[:234938]:
        if token.lower()[0] != _char:

            _pos = _list.index(token)
            # print(str(_pos) + " - " + str(_list[_pos]) )
            if len(_sub_list) == 0:
                _sub_list.append(_pos)

            elif len(_sub_list) == 1:
                _sub_list.append(_pos - 1)

                _char_list.append(_char)
                _word_range_list.append(_sub_list)

                _sub_list = [_pos]

            _char = token.lower()
initialize_dict_bookmark()


def get_word_range(_char):
    for _chr in _char_list:
        if _chr == _char:
            _index = _char_list.index(_chr)

    return _word_range_list[_index]


def word_match(a, b):
    """
    if nltk.edit_distance(a, b) > 3: # sai chinh ta nhieu hon 3 chu
        return 500
    """

    # make sure that a is longer than b
    if len(a) < len(b):
        a, b = b, a
    # calculate difference between two words by sum of difference of each characterss
    distance = 0
    for i in range(len(b)):
        distance += (ord(a[i]) - ord(b[i])) ** 2
    for j in range(len(b), len(a)):
        distance += (ord(a[j]) - ord('A')) ** 2
    return math.sqrt(distance)


#  Find the exact index of str in dictionary if exist, or the nearest index that str is similar too
def get_smart_index_in_dictionary(str):
    _tmp_dict = []
    for i in range(get_word_range(str.lower()[0])[0], get_word_range(str.lower()[0])[1] + 1):
        _tmp_dict.append(_dict[i])
    if str in _tmp_dict: # str is existed word in dictionary
        return _dict.index(str)
    else:   # find the word in dictionary that most similar to str
        index = -1
        # max distance between longest english word and 'a' is about 312 so 500 will be okay !
        min_distance = 500
        for token in _tmp_dict:
            word_distance = word_match(str, token)
            if min_distance > word_distance:
                min_distance = word_distance
                index = _dict.index(token)
        return index


def word_similarity(a, b):
    #  Break sentence into list of words
    tokens_a = nltk.tokenize.word_tokenize(remove_punctuation(a))
    tokens_b = nltk.tokenize.word_tokenize(remove_punctuation(b))

    #  Create sentence vector from list of words
    vector_a = []
    vector_b = []

    for token in tokens_a:
        vector_a.append(get_smart_index_in_dictionary(token)+1)
    for token in tokens_b:
        vector_b.append(get_smart_index_in_dictionary(token)+1)

    # Making sure that tokens_a is longer than tokens_b
    if len(vector_a) < len(vector_b):
        vector_a, vector_b = vector_b, vector_a

    # calculate distance between two sentence vector
    shorter_length = len(vector_b)
    distance = 0
    for i in range(0, shorter_length):
        distance += (vector_b[i] - vector_a[i]) ** 2
    for j in range(shorter_length, len(vector_a)):
        distance += vector_a[j] ** 2

    distance = math.sqrt(distance)

    if distance <= 1:
        return 1
    else:
        return 1 / math.log2(distance)


def remove_punctuation(_str):
    new_string = ""
    for i in _str:
        if i.isalpha() or i == " ":
            new_string += i.lower()
    return new_string


def correct_sentence(_str):
    list_str = nltk.tokenize.word_tokenize(remove_punctuation(_str))
    vector_str = []
    for token in list_str:
        vector_str.append(get_smart_index_in_dictionary(token))

    corrected_sentence = ""
    for i in vector_str:
        corrected_sentence += dict[i] + " "
    return corrected_sentence


def isnumeric(s):
    '''returns True if string s is numeric'''
    return all(c in "0123456789.+-" for c in s) and any(c in "0123456789" for c in s)


def check_spelling(raw_str):
    return raw_str


def word_tokenize(s):
    return nltk.tokenize.word_tokenize(s)


# clean list keywords to make sure that there is no duplicate in list
def remove_duplicate_in_list(_list):
    tmp_keywords = []
    [tmp_keywords.append(x) for x in _list if x not in _list]
    return tmp_keywords

"""
Student information for this assignment:

Replace JOEL PAINE with your name.
On my/our honor, JOEL PAINE and <FULL NAME>, this
programming assignment is my own work and I have not provided this code to
any other student.

I have read and understand the course syllabus's guidelines regarding Academic
Integrity. I understand that if I violate the Academic Integrity policy (e.g.
copy code from someone else, have the code generated by an LLM, or give my
code to someone else), the case shall be submitted to the Office of the Dean of
Students. Academic penalties up to and including an F in the course are likely.

UT EID 1: jmp7356
UT EID 2:
"""
import sys

# the constant used to calculate the step size
STEP_SIZE_CONSTANT = 3


# DO NOT modify this function.
def is_prime(n):
    """
    Determines if a number is prime.

    pre: n is a positive integer.
    post: Returns True if n is prime, otherwise returns False.
    """
    if n == 1:
        return False

    limit = int(n**0.5) + 1
    div = 2
    while div < limit:
        if n % div == 0:
            return False
        div += 1
    return True


# DO NOT modify this function.
def hash_word(s, size):
    """
    Hashes a lowercase string to an index in a hash table.

    pre: s is a lowercase string, and size is a positive integer representing either
         hash table size or the constant for double hashing.
    post: Returns an integer index in the range [0, size - 1] where the string hashes to.
    """
    hash_idx = 0
    for c in s:
        letter = ord(c) - 96
        hash_idx = (hash_idx * 26 + letter) % size
    return hash_idx

def step_size(s):
    """
    Calculates step size for double hashing using STEP_SIZE_CONSTANT.

    pre: s is a lowercase string.
    post: Returns the calculated step size as an integer based on the provided string.
    """
    index = hash_word(s, STEP_SIZE_CONSTANT)
    step = STEP_SIZE_CONSTANT - (index % STEP_SIZE_CONSTANT)
    return step


def insert_word(s, hash_table):
    """
    Inserts a string into the hash table using double hashing for collision resolution.
    No duplicates are allowed.

    pre: s is a string, and hash_table is a list representing the hash table.
    post: Inserts s into hash_table at the correct index; resolves any collisions
          by double hashing.
    """
    index = hash_word(s, len(hash_table))
    step = step_size(s)

    if hash_table[index] == '':
        hash_table[index] = s
        return
    elif hash_table[index] == s:
        return  # duplicate

    i = 0
    while i < len(hash_table):
        new_index = (index + step) % len(hash_table)
        if hash_table[new_index] == '':
            hash_table[new_index] = s
            return
        elif hash_table[new_index] == s:
            return  # duplicate
        i += 1
        index = new_index

    return  # hash table is full or no space available

def find_word(s, hash_table):
    """
    Searches for a string in the hash table.
    Note: using the `in` operator is incorrect as that will be O(N). We want
          an O(1) time average time complexity using hashing.

    pre: s is a string, and hash_table is a list representing the hash table.
    post: Returns True if s is found in hash_table, otherwise returns False.
    """
    index = hash_word(s, len(hash_table))
    step = step_size(s)

    if hash_table[index] == s:
        return True
    # check collision
    i = 0
    while i < len(hash_table):
        new_index = (index + step) % len(hash_table)
        if hash_table[new_index] == s:
            return True
        elif hash_table[new_index] == '':
            return False

        i += 1
        index = new_index

    return False

def is_reducible(s, hash_table, hash_memo):
    """
    Determines if a string is reducible using a recursive check.

    pre: s is a lowercase string, hash_table is a list representing the hash table,
         and hash_memo is a list representing the hash table
         for memoization.
    post: Returns True if s is reducible (also updates hash_memo by
          inserting s if reducible), otherwise returns False.
    """

    def helper(s, hash_table, hash_memo):
        if not find_word(s, hash_table):
            return False
        if find_word(s, hash_memo):
            return True
        if len(s) == 1:
            if s in ['a', 'i', 'o']:
                return True
            return False

        reducible = False
        for i in range(len(s)):
            reduced = s[:i] + s[i+1:]
            if find_word(reduced, hash_table):
                if helper(reduced, hash_table, hash_memo):
                    reducible = True
                    break

        if reducible:
            insert_word(s, hash_memo)
            return True

        return False

    return helper(s, hash_table, hash_memo)


def get_longest_words(string_list):
    """
    Finds longest words from a list.

    pre: string_list is a list of lowercase strings.
    post: Returns a list of words in string_list that have the maximum length.
    """
    max_num = 0
    max_list = []
    for string in string_list:
        length = len(string)
        max_num = max(max_num, length)
    for string in string_list:
        if len(string) == max_num:
            max_list.append(string)

    return max_list





def main():
    """The main function that calculates the longest reducible words"""
    # create an empty word_list
    word_list = []
    # read words using input redirection
    for line in sys.stdin:
        word_list.append(line.strip())
    # where each line read from input()
    # should be a single word. Append to word_list
    # ensure each word has no trailing white space.

    # find length of word_list
    length = len(word_list)
    length *= 2
    while not is_prime(length):
        length += 1


    # determine prime number N that is greater than twice
    # the length of the word_list

    # create an empty hash_list
    # populate the hash_list with N blank strings
    hash_list = [''] * length

    # hash each word in word_list into hash_list
    for word in word_list:
        insert_word(word, hash_list)
    # for collisions use double hashing

    # create an empty hash_memo of size M
    m = .2 * len(word_list)
    m = int(m)
    while not is_prime(m):
        m += 1
    # we do not know a priori how many words will be reducible
    # let us assume it is 10 percent (fairly safe) of the words
    # then M is a prime number that is slightly greater than
    # 0.2 * size of word_list
    hash_memo = [''] * m

    # populate the hash_memo with M blank strings
    reducible_words = []
    # create an empty list reducible_words

    # for each word in the word_list recursively determine
    # if it is reducible, if it is, add it to reducible_words
    # as you recursively remove one letter at a time check
    # first if the sub-word exists in the hash_memo. if it does
    # then the word is reducible and you do not have to test
    # any further. add the word to the hash_memo.
    for word in word_list:

        if is_reducible(word, hash_list, hash_memo):
            reducible_words.append(word)

    # find the largest reducible words in reducible_words
    longest = get_longest_words(reducible_words)
    alpha = sorted(longest)
    for word in alpha:
        print(word)
    # print the reducible words in alphabetical order
    # one word per line


if __name__ == "__main__":
    main()

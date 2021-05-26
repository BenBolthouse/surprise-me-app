import string


def random_string(length):
    '''
    Returns a random string with lowercase letters and numbers of a specified
    length.
    '''

    letters = string.ascii_lowercase + string.ascii_numbers
    return (''.join(random.choice(letters) for i in range(length)))

from string import ascii_lowercase, ascii_numbers


def random_string(length):
    '''
    Returns a random string with lowercase letters and numbers of a specified
    length.
    '''

    letters = ascii_lowercase + ascii_numbers
    return (''.join(random.choice(letters) for i in range(length)))

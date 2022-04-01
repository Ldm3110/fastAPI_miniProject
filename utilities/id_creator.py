import random
import string


def create_id_unique(type_of_id):
    """
    Create a unique id
    :param type_of_id:
    'Comment-'for a new comment
    'User-' for the creator of the comment
    :return: unique id, for example 'User-gc8e82wb2b63jvvyegvi' or 'Comment-82kvq1afm0n0vaz8ihl1'
    """
    length = 10
    chars = string.ascii_lowercase + string.digits
    unique_id = type_of_id + ''.join(random.choice(chars) for _i in range(length))

    return unique_id

import random
import string


def generate_participation_code():
    letters = string.ascii_lowercase + '1234567890'
    return ''.join(random.choice(letters) for i in range(4))

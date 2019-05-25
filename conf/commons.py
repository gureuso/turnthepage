import posixpath
import random
import string
import datetime
import os


def get_random_string(length):
    return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(length))


def generate_filename(instance, filename):
    name, extension = os.path.splitext(filename)
    name = '{0}_{1}{2}'.format(instance.user.id, get_random_string(20), extension)
    dirname = datetime.datetime.now().strftime('%Y/%m/%d/')
    return posixpath.join(dirname, name)


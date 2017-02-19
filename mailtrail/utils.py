import os

def get_template(*args):
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), 'templates', *args)

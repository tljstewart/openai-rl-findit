import time

DEBUG = True

file = None


def create_log(name):
    global file
    file = open('data/3/test/' + name + '-data.csv', 'w')


def file_print(data):
    print(', '.join(map(str, data)), file=file)


def debug_print(msg):
    if DEBUG:
        print(msg)

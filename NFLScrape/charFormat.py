import unidecode
import re


def format_string(input_string):
    if input_string is not None:
        input_string = unidecode.unidecode(input_string)
        input_string = input_string.replace('%20', ' ')
        input_string = input_string.replace('-', ' ')
        input_string = input_string.replace('_', ' ')
        bad_chars = ['#', '?', '&', ';', '(', ')', '$', '!', '<', '>']
        for x in bad_chars:
            input_string = input_string.replace(x, '')


def stripBadChars(stringIn):
    delchars = ''.join(c for c in map(chr, range(256)) if not c.isalnum()).replace(' ', '')
    table = str.maketrans(dict.fromkeys(delchars))
    stringOut = stringIn.translate(table)
    return stringOut
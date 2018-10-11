import unidecode
import re

def format_string(input_string):
    if input_string is not None and not input_string.isdigit():
        input_string = unidecode.unidecode(str(input_string)).strip()
        bad_chars = ['#', '?', '&', ';', '(', ')', '$', '!', '<', '>']
        for x in bad_chars:
            input_string = input_string.replace(x, '')
    return input_string


def stripBadChars(stringIn):
    delchars = ''.join(c for c in map(chr, range(256)) if not c.isalnum()).replace(' ', '')
    table = str.maketrans(dict.fromkeys(delchars))
    stringOut = stringIn.translate(table)
    return stringOut


def format_number(input_string):
    if input_string is not None:
        input_string = unidecode.unidecode(input_string).strip()
        bad_chars = ['#', '?', '&', ';', '(', ')', '$', '!', '<', '>']
        for x in bad_chars:
            input_string = input_string.replace(x, '')


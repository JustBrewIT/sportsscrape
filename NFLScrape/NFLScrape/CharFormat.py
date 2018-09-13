

def stripBadChars(stringIn):
    delchars = ''.join(c for c in map(chr, range(256)) if not c.isalnum()).replace(' ', '')
    table = str.maketrans(dict.fromkeys(delchars))
    stringOut = stringIn.translate(table)
    return stringOut
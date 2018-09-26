import re


def convert_headers(input):
    if isinstance(input, dict):
        return {key.decode('utf-8'): convert_headers(value) for key, value in input.items()}
    elif isinstance(input, list):
        return ''.join([convert_headers(element) for element in input])
    elif isinstance(input, bytes):
        return input.decode('utf-8').replace(' ', '')
    else:
        return input


def extract_phone(text):
    try:
        return re.findall('(\d{3}[-.\s]\d{3}[-.\s]\d{4}|\(\d{3}\)\s*\d{3}[-.\s]\d{4}|\d{3}[-.\s]\d{4}(?=[^\d]))', text)[0]
    except:
        return None


def xstr(s):
    if s is None:
        return ''
    return str(s)



def conCo(x):
    sum = ''
    for i in range(len(x)):
        sum += x[i]+' '
    return sum

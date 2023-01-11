# Simple functions for proper word endings
# Male endings
def word_ending_male(_int: int = 0):
    d = _int % 10
    h = _int % 100
    if d == 1 and h != 11:
        s = ""
    elif 1 < d < 5 and not 11 < h < 15:
        s = "а"
    else:
        s = "ов"
    return s


# Female endings
def word_ending_female(_int: int = 0):
    d = _int % 10
    h = _int % 100
    if d == 1 and h != 11:
        s = "у"
    elif 1 < d < 5 and not 11 < h < 15:
        s = "ы"
    else:
        s = ""
    return s

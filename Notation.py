import math


def clamp_to(value, l):
    value += 1
    for index, item in enumerate(l):
        index2 = index + 1
        if index2 * 3 <= value <= (index2 * 3) + 3:
            return index
    return "couldn't clamp"


def notate(value, notation_list):
    if value < 1000:
        return value
    notation_index = int(math.log10(value))
    clamped_index = clamp_to(notation_index, notation_list)
    if not clamped_index == "couldn't clamp" and not clamped_index > len(notation_list):
        notation_value = value / 10**((clamped_index + 1) * 3)
        return ("%.2f" % notation_value) + notation_list[clamped_index]
    else:
        notation_value = value / 10**notation_index
        return ("%.2f" % notation_value) + "e" + str(notation_index)

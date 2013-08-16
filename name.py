#!/usr/bin/env python
"""
Names integers according to Chuquet, Conway-Wechsler
"""
zero = 'zero'

units = dict(enumerate(['', 'one', 'two', 'three', 'four', 'five', 'six',
                        'seven', 'eight', 'nine', 'ten', 'eleven', 'twelve']))

teens = units.copy()
teens.update({'suffix': 'teen', 3: 'thir', 5: 'fif'})

tens = teens.copy()
tens.update({'suffix': 'ty', 2: 'twen', 4: 'for', 8: 'eigh'})


# Conway-Wechsler dictionary (Miakinen Variant) (Extended Chuquet)
# aka 'échelle courte' (American Standard)
cwdict = {'low': {2: 'hundred', 3: 'thousand'},

          'ill': {0: 'n', 1:  'm', 2:  'b', 3: 'tr', 4: 'quadr', 5: 'quint',
                  6: 'sext', 7: 'sept', 8: 'oct', 9: 'non'},

          1:     {0: (set(), '',         set()),
                  1: (set(), 'un',       set()),
                  2: (set(), 'duo',      set()),
                  3: (set(), 'tre',      set('s')),
                  4: (set(), 'quattuor', set()),
                  5: (set(), 'quinqua',  set()),
                  6: (set(), 'se',       set('sx')),
                  7: (set(), 'septe',    set('mn')),
                  8: (set(), 'octo',     set()),
                  9: (set(), 'nove',     set('mn'))},

          10:    {10: (set('n'),    'deci',         set()),
                  20: (set('ms'),   'viginti',      set()),
                  30: (set('ns'),   'triginta',     set()),
                  40: (set('ns'),   'quadraginta',  set()),
                  50: (set('ns'),   'quinquaginta', set()),
                  60: (set('n'),    'sexaginta',    set()),
                  70: (set('n'),    'septuaginta',  set()),
                  80: (set('mx'),   'octoginta',    set()),
                  90: (set(),       'nonaginta',    set())},

          100:   {100: (set('nx'),  'centi',        set()),
                  200: (set('n'),   'ducenti',      set()),
                  300: (set('ns'),  'trecenti',     set()),
                  400: (set('ns'),  'quadringenti', set()),
                  500: (set('ns'),  'quingenti',    set()),
                  600: (set('n'),   'sescenti',     set()),
                  700: (set('n'),   'septingenti',  set()),
                  800: (set('mx'),  'octingenti',   set()),
                  900: (set(),      'nongenti',     set())}}

vowels = set('aeiou')


def name(number, precision=None):
    # convert to int
    try:
        number = int(number)
    except ValueError as e:
        raise e

    # round to precision
    if precision is not None:
        number = _round(number, precision)

    # convert to str
    number = str(number)

    # get sign
    sign = ''
    if number.startswith('-'):
        sign = 'negative'
        number = number[1:]

    # zero special-case
    if number == '0':
        name = zero
    else:
        # Name ones, tens, hundreds first, because they are peculiar.
        small_nums = low_nums(number)
        # Name large numbers (>=thousands); they follow nice rules.
        big_nums = high_nums(number)
        #print('small_nums: ' + small_nums)
        #print('big_nums: ' + big_nums)
        name = (big_nums + ' ' + small_nums).strip()
    words = _join([sign, name])
    print('output: {}'.format(words))
    return words


def _round(num, precision, base=10):
    import math
    k = base ** (math.floor(math.log(num, base)) + 1 - precision)
    num += k/2
    return int(num - num % k)


def orders(o, level=0):
    #print('new round of orders(), o={}'.format(o))
    # since o > 30, name_num > 27/3 = 9 but name_num < 1000
    # name_num refers to the indexing used in cwdict for one, ten, hun
    name_num = int((o - 3) / 3) % 1000
    if o < 2:
        return ''
    elif o <= 3 and level == 0:
        return cwdict['low'][o]
    elif o % 3 != 0:
        #probably raise error
        return None
    elif o <= 30:
        return illion_append(cwdict['ill'][name_num], level)  # e.g. 'b'+'illion'

    #mult_num = int(((o-3)/3)/1000)
    #print('in orders, name_num={}'.format(name_num))
    #get last three digits, assign their orders to u, t, h
    o_list = [int(c) for c in '0'+str(name_num)]
    u, t, h = o_list[-1] * 1, o_list[-2] * 10, o_list[-3] * 100

    #print('u={}, t={}, h={}'.format(u, t, h))
    try:
        ones = cwdict[1][u]
    except KeyError:
        ones = (set(), '', set())
    try:
        tens = cwdict[10][t]
    except KeyError:
        tens = (set(), '', set())
    try:
        huns = cwdict[100][h]
    except KeyError:
        huns = (set(), '', set())

    name = ones[1] + match_joiners(ones, tens) + tens[1] \
        + match_joiners(tens, huns) + huns[1]

    if o > 3003:
        #print('high order! o={}'.format(o))
        #print('current_name='+name)
        #print('name_num={}'.format(name_num))
        new_name_num = o-3

        return orders(int(str(int((o-3)/3))[:-3])*3+3, level + 1) + illion_append(name, level)
    else:
        #print(('level={}, o={}, name='+name).format(level, o))
        return illion_append(name, level)


def illion_append(s, level=0):
    if s == '':
        return s
    s = s[:-1] if s[-1:] in vowels else s
    return s + 'illi' if level > 0 else s + 'illion'


def match_joiners(left, right):
    """
    left should be dict entry joining from left
    right should be dict entry joining from right
    """

    if left[1] == 'tre' and 'x' in right[0]:
        # tres 's' match with 'x' case
        return 's'
    else:
        try:
            return left[2].intersection(right[0]).pop()
        except KeyError:
            return ''


def high_nums(s, o=0, scale='American'):

    if scale == 'American':
        grouping = 3
    # elif scale == 'Peletier':
    #     grouping = 3

    if o < 3:
        return high_nums(s[:-(3-o)], o=3, scale=scale)
    if s == '':
        return ''
    if o % grouping != 0:
        print('order not divisible by {} - o={}'.format(grouping, o))

    # skip all the zeros
    i = 1
    current_str = s[-grouping*i:]
    while current_str == '0' * grouping:
        i += 1
        o += grouping
        current_str = s[-grouping*i:-grouping*(i-1)]

    print("current_str: {}".format(current_str))
    current_name = low_nums(current_str, o=0, scale=scale)
    print("current_name: {}".format(current_name))

    return _join([high_nums(s[:-grouping*i], o+grouping, scale), current_name,
                  orders(o)])


def _join(l, delim=' '):
    """Join each str in l by delim, unless str is ''"""
    return delim.join(k for k in l if k != '')


def low_nums(s, o=0, scale='American'):
    """Name string s recursively.
    :param str s:
        String representation of decimal digits to be named
    :param int o:
        Recursive index; order of magnitude of the last digit of s.
    :param str scale:
        One of ['American', 'Peletier'].
    """
    if s == '' or (o > 2 and scale == 'American') or (o > 3 and scale == 'Peletier'):
        return ''

    if o == 0:
        # number of digits to deal with
        n_digits = 2
        # isolate last one or two digits (tens and ones columns)
        n = int(s[-n_digits:])
        if n == 0:
            # do not return 'zero' here, 'zero' is a special-case. We only say 
            # 'zero' when the whole number is exactly 0.
            name = ''
        elif n < 13:
            # Name the (one or two) digits in the ones and tens column by name
            # between 'one' and 'twelve'
            name = units[n]
        elif n < 20:
            # Name the (one or two) digits in the ones and tens column by name
            # between 'thirteen' and 'nineteen'
            name = teens[n % 10] + teens['suffix']
        else:  # n < 100
            # Name the compound number e.g. 'thirty-two' between 'twenty' and 
            # 'ninety-nine'
            name = _join([tens[int(n/10)] + tens['suffix'], low_nums(s[-1:])], '-')

    elif o == 2:
        # number of digits to deal with
        n_digits = 1
        # isolate last digit (hundreds column)
        n = int(s[-n_digits:])
        # name the hundreds e.g. 'one hundred'
        q = units[n]
        name = _join([q, cwdict['low'][2]]) if q else ''

    # elif o == 3 and scale == 'Peletier':
    #     n = int(s[-3:])
    #     return (low_nums(s[-3:], 0, scale) + ' ' + low_nums(s[:-3], 2, scale) + cwdict['low'][o]).strip()
    
    return _join([low_nums(s[:-n_digits], o+n_digits, scale), name])

if __name__ == '__main__':
    pass

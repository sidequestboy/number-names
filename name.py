"""
Names integers according to Chuquet, Conway-Wechsler
"""
zero = 'zero'

units = dict(enumerate(['', 'one', 'two', 'three', 'four', 'five', 'six',
                        'seven', 'eight', 'nine', 'ten', 'eleven', 'twelve']))

teens = units.copy()
teens.update({'postfix': 'teen', 3: 'thir', 5: 'fif'})

tens = teens.copy()
tens.update({'postfix': 'ty', 2: 'twen', 4: 'for', 8: 'eigh'})


# Conway-Wechsler dictionary (Miakinen Variant) (Extended Chuquet)
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


def name(number):
    #convert to str
    if type(number) is int:
        number = str(number)
        #print(number)
    else:
        try:
            number = str(int(number))
        except ValueError as e:
            print(e)
            return -1
    #print('input: '+number)
    sign = ''
    if number[0:1] == '-':
        number = number[1:]
        sign = 'negative '
    if number == '0':
        name = zero
    else:
        #deal with hundreds and units first
        small_nums = hunds(number[-3:], 0)
        big_nums = digits(number[:-3], 3)
        #print('small_nums: ' + small_nums)
        #print('big_nums: ' + big_nums)
        name = (big_nums + ' ' + small_nums).strip()
    words = sign + name
    print('output: {}'.format(words))
    return words


def orders(o, level=0):
    print('new round of orders(), o={}'.format(o))
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
    #
    name = ones[1] + match_joiners(ones, tens) + tens[1] \
        + match_joiners(tens, huns) + huns[1]

    if o > 3003:
        print('high order! o={}'.format(o))
        print('current_name='+name)
        print('name_num={}'.format(name_num))
        new_name_num = o-3


        return orders(int(str(int((o-3)/3))[:-3])*3+3, level + 1) + illion_append(name, level)
    else:
        print(('level={}, o={}, name='+name).format(level, o))
        return illion_append(name, level)

#def highorders(o, level=1):
#    """
#    for numbers higher than 10**3003 called from orders()
#    """
#    name_num = int((o - 3) / 3) % 1000




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

    if left[1] ==  'tre' and 'x' in right[0]:
        # tres 's' match with 'x' case
        return 's'
    else:
        try:
            return left[2].intersection(right[0]).pop()
        except KeyError:
            return ''


def digits(s, o):

    # o should be greater than or equal to 3
    if s == '' or o < 3:
        return ''
    if o % 3 != 0:
        print('order not divisible by 3 - o={}'.format(o))

    # isolate last three digits
    i = 1
    current_str = s[-3*i:]
    while current_str == '000':
        i += 1
        o += 3
        current_str = s[-3*i:-3*(i-1)]
    #print('k, getting hunds on s={}'.format(current_str))
    current_name = hunds(current_str)

    if current_name == '':
        #print("current_name == ''")
        newpart = digits(s[:-3*i], o+3)
    else:
        #print(o)
        #newpart = digits(s[:-3*i], o+3) + ' ' + hunds(s[-3*i:-3*(i-1)], 0) + ' ' \
        #    + orders(o)
        newpart = digits(s[:-3*i], o+3) + ' ' + current_name + ' ' + orders(o)
    return newpart.strip()


def hunds(s, o=0):

    if s == '':
        return s

    # isolate last two digits
    n = int(s[-2:])

    if o == 0:
        if n == 0:
            # do not return 'zero' here ('twenty zero' bug)
            return ''
        elif n < 13 and len(s) == 1:
            # do not recurse for this case
            return units[n]
        elif n < 13:
            name = units[n]
        elif n < 20:
            name = teens[n-10] + teens['postfix']
        else:  # n < 100
            name = tens[int(n/10)] + tens['postfix'] + ' ' + hunds(s[-1:], 0)
        return hunds(s[:-2], 2) + ' ' + name
    elif o == 2:
        if n < 10:
            name = units[n] + ' ' + cwdict['low'][o]
        return name


if __name__ == '__main__':
    assert name('4') == 'four'
    assert name('133') == 'one hundred thirty three'
    assert name('12') == 'twelve'
    assert name('101') == 'one hundred one'
    assert name('212') == "two hundred twelve"
    assert name('40') == 'forty'
    assert name('10000') == 'ten thousand'
    assert name('0') == 'zero'
    assert name('12373581926') == 'twelve billion three hundred seventy '\
        'three million five hundred eighty one thousand nine hundred '\
        'twenty six'
    assert name('123456789') == 'one hundred twenty three million four '\
        'hundred fifty six thousand seven hundred eighty nine'
    assert name('10000000000') == 'ten billion'
    print(name(int(10**30)))
    assert name(int(10**30)) == 'one nonillion'
    assert name(int(10**33)) == 'one decillion'
    assert name(int(10**36)) == 'one undecillion'
    assert name(int(10**39)) == 'one duodecillion'
    assert name(int(10**42)) == 'one tredecillion'
    assert name(int(10**45)) == 'one quattuordecillion'
    assert name(int(10**48)) == 'one quinquadecillion'
    assert name(int(10**49)) == 'ten quinquadecillion'
    name('123432316243546583726354657684736252434352627849587362542')
    assert name(str(10**303)) == 'one centillion'
    name('blah')
    name(-495859038387495058737262839405068674736232920384757670594736365363849505)
    #assert name(10**2421) == 'one sexoctingentillion'
    name(10**114)
    name('000000000000')
    assert name(10**1015) == 'ten septentrigintatrecentillion'


    assert name(10**3001) == 'ten novenonagintanongentillion'

    assert name(10**4000) == 'ten milliduotrigintatrecentillion'

    assert name(10**19683) == 'sextillisexagintaquingentillion'
    print('All ok')

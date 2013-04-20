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

          'ill': {6:  'm', 9:  'b', 12: 'tr', 15: 'quadr', 18: 'quint',
                  21: 'sext', 24: 'sept', 27: 'oct', 30: 'non'},

          'one': {0: ('',               set()),
                  1: ('un',             set()),
                  2: ('duo',            set()),
                  3: ('tre',            set('s')),
                  4: ('quattuor',       set()),
                  5: ('quinqua',        set()),
                  6: ('se',             set('sx')),
                  7: ('septe',          set('mn')),
                  8: ('octo',           set()),
                  9: ('nove',           set('mn'))},

          'ten': {10: ('deci',          set('n')),
                  20: ('viginti',       set('ms')),
                  30: ('triginta',      set('ns')),
                  40: ('quadraginta',   set('ns')),
                  50: ('quinquaginta',  set('ns')),
                  60: ('sexaginta',     set('n')),
                  70: ('septuaginta',   set('n')),
                  80: ('octoginta',     set('mx')),
                  90: ('nonaginta',     set())},

          'hun': {100: ('centi',        set('nx')),
                  200: ('ducenti',      set('n')),
                  300: ('trecenti',     set('ns')),
                  400: ('quadringenti', set('ns')),
                  500: ('quingenti',    set('ns')),
                  600: ('sescenti',     set('n')),
                  700: ('septingenti',  set('n')),
                  800: ('octingenti',   set('mx')),
                  900: ('nongenti',     set())}}

vowels = set('aeiou')


def name(number):
    #convert to str
    if type(number) is int:
        number = str(number)
    else:
        try:
            number = str(int(number))
        except ValueError as e:
            print(e)
            return -1

    if number == '0':
        return zero
    elif number[0:1] == '-':
        number = number[1:]
        sign = 'negative '
    else:
        sign = ''

    #deal with hundreds and units first
    small_nums = hunds(number[-3:], 0)
    big_nums = digits(number[:-3], 3)
    #print('small_nums: ' + small_nums)
    #print('big_nums: ' + big_nums)

    words = sign + (big_nums + ' ' + small_nums).strip()
    print(words)
    return words


def orders(o, level=0):
    #print('in orders(), o={}'.format(o))
    if o <= 3:
        return cwdict['low'][o]
    elif o % 3 != 0:
        #probably raise error
        return None
    elif o <= 30:
        return illion_append(cwdict['ill'][o])  # e.g. 'b'+'illion'

    # since o > 30, name_num > 27/3 = 9 but name_num < 1000
    # name_num refers to the indexing used in cwdict for one, ten, hun
    name_num = int((o - 3) / 3) % 1000
    #mult_num = int(((o-3)/3)/1000)
    #print('in orders, name_num={}'.format(name_num))
    #get last three digits, assign their orders to u, t, h
    o_list = [int(c) for c in '0'+str(name_num)]
    u, t, h = o_list[-1] * 1, o_list[-2] * 10, o_list[-3] * 100

    #print('u={}, t={}, h={}'.format(u, t, h))

    #
    if t:
        name = cwdict['one'][u][0] + match(u, 'ten', t) + cwdict['ten'][t][0]
    else:
        name = cwdict['one'][u][0] + match(u, 'hun', h) + cwdict['hun'][h][0]



    if level == 0 and o > 3003:
        return orders(int(o / 1000) + (o % 1000), level + 1) \
            + illion_append(name)
    elif o > 3003:
        return orders(int(o / 1000) + (o % 1000), level + 1) \
            + illion_append(name, illi=True)
    else:
        print(('line 122: level={}, o={}, name='+name).format(level, o))
        return illion_append(name)


def illion_append(s, illi=False):
    if s == '':
        return s
    s = s[:-1] if s[-1:] in vowels else s
    return s + 'illi' if illi else s + 'illion'


def match(u, label, val):

    if u == 3 and 'x' in cwdict[label][val][1]:
        # tres 's' match with 'x' case
        return 's'
    else:
        try:
            return cwdict['one'][u][1].intersection(cwdict[label][val][1]).pop()
        except KeyError:
            return ''


def digits(s, o):

    # o should be greater than or equal to 3
    if s == '' or o < 3:
        return ''

    # isolate last three digits
    h = hunds(s[-3:], 0)
    if h == '':
        newpart = digits(s[:-3], o+3)
    else:
        #print(o)
        newpart = digits(s[:-3], o+3) + ' ' + hunds(s[-3:], 0) + ' ' \
            + orders(o)
    return newpart.strip()


def hunds(s, o):

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
    assert name(int(10**30)) == 'one nonillion'
    assert name(int(10**33)) == 'one decillion'
    assert name(int(10**36)) == 'one undecillion'
    assert name(int(10**39)) == 'one duodecillion'
    assert name(int(10**42)) == 'one tredecillion'
    assert name(int(10**45)) == 'one quattuordecillion'
    assert name(int(10**48)) == 'one quinquadecillion'
    assert name(int(10**49)) == 'ten quinquadecillion'
    name('123432316243546583726354657684736252434352627849587362542')
    name(str(10**303))
    name('blah')
    name(-495859038387495058737262839405068674736232920384757670594736365363849505)
    name(10**2421)
    name(10**1015)
    print('All ok')

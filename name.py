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

loworders = {'postfix': '', 2: 'hundred', 3: 'thousand'}

#Chuquet
illions = {'postfix': 'illion', 6: 'm', 9: 'b', 12: 'tr', 15: 'quadr',
           18: 'quint', 21: 'sext', 24: 'sept', 27: 'oct', 30: 'non'}

#Conway-Wechsler
cwones = dict(enumerate(['', 'un', 'duo', 'tre', 'quattuor', 'quinqua', 'se',
                         'septe', 'octo', 'nove']))

cwones_suffixes = {0: [], 1: [], 2: [], 3: ['s'], 4: [], 5: [], 6: ['x', 's'],
                   7: ['m', 'n'], 8: [], 9: ['m', 'n']}

cwtens = {0: '', 10: 'deci', 20: 'viginti', 30: 'triginta', 40: 'quadraginta',
          50: 'quinquaginta', 60: 'sexaginta', 70: 'septuaginta',
          80: 'octoginta', 90: 'nonaginta'}

cwtens_prefixes = {0: [], 10: ['n'], 20: ['m', 's'], 30: ['n', 's'],
                   40: ['n', 's'], 50: ['n', 's'], 60: ['n'], 70: ['n'],
                   80: ['m', 'x'], 90: []}

cwhunds = {0: '', 100: 'centi', 200: 'ducenti', 300: 'trecenti',
           400: 'quadringenti', 500: 'quingenti', 600: 'sescenti',
           700: 'septingenti', 800: 'octingenti', 900: 'nongenti'}

cwhunds_prefixes = {0: [], 100: ['n', 'x'], 200: ['n'], 300: ['n', 's'],
                    400: ['n', 's'], 500: ['n', 's'], 600: ['n'], 700: ['n'],
                    800: ['m', 'x'], 900: []}

vowels = set('aeiou')


def name(number):

    if type(number) is int:
        number = str(number)

    if number == '0':
        return zero

    #deal with hundreds and units first
    small_nums = hunds(number[-3:], 0)
    big_nums = digits(number[:-3], 3)
    print('small_nums: ' + small_nums)
    print('big_nums: ' + big_nums)

    words = (big_nums + ' ' + small_nums).strip()
    print(words)
    return words


def orders(o, level=0):
    #print('in orders(), o={}'.format(o))
    if o <= 3:
        return loworders[o]
    elif o % 3 != 0:
        #probably raise error
        return None
    elif o <= 30:
        return illions[o] + illions['postfix']  # e.g. 'b'+'illion'

    name_num = int((o - 3) / 3) % 1000
    #mult_num = int(((o-3)/3)/1000)
    #print('in orders, name_num={}'.format(name_num))
    o_list = [int(c) for c in '0'+str(name_num)]
    u, t, h = o_list[-1] * 1, o_list[-2] * 10, o_list[-3] * 100

    #print('u={}, t={}, h={}'.format(u,t,h))
    if h == 0:
        name = cwones[u] + match(cwones_suffixes[u], cwtens_prefixes[t]) \
            + cwtens[t]
    else:
        name = cwones[u] + match(cwones_suffixes[u], cwhunds_prefixes[h])\
            + cwhunds[h]

    if level == 0 and o > 1000:
        return orders(int(o / 1000) + (o % 1000), level + 1) \
            + illion_append(name)
    elif o > 1000:
        return orders(int(o / 1000) + (o % 1000), level + 1) \
            + illion_append(name, illi=True)
    else:
        return illion_append(name)

def illion_append(s, illi=False):
    if s == '':
        return s
    s = s[:-1] if s[-1:] in vowels else s
    return s + 'illi' if illi else s + 'illion'

def match(units, l2):
    if units == ['s']:
        #tre case
        if 's' in l2:
            return 's'
        elif 'x' in l2:
            return 'x'
        else:
            return ''

    for suffix in units:
        if suffix in l2:
            return suffix
    #print('units: {} did not match'.format(units))
    #print('l2   : {}'.format(l2))
    return ''
    #raise error


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
        newpart = digits(s[:-3], o+3) + ' ' + hunds(s[-3:], 0) + ' ' + orders(o)
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
            print(hunds(s[-1:], 0))
            name = tens[int(n/10)] + tens['postfix'] + ' ' + hunds(s[-1:], 0)
            print(name)
        return hunds(s[:-2], 2) + ' ' + name
    elif o == 2:
        if n < 10:
            name = units[n] + ' ' + loworders[o]
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
    assert name(10**603) == 'one ducentillion'
    print('All ok')

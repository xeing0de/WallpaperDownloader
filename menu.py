def categories():
    print('Select categories one or more(Default 12):')
    print('1)General')
    print('2)Anime')
    print('3)People')

    category = input('Enter: ')
    uniq = set(category)

    if not uniq.issubset({'','1','2','3'}):
        print('Select only 1, 2 or 3')
        return categories()
    if category == '':
        return '110'
    else:
        flags = ''.join('1' if str(i) in uniq else '0' for i in range(1,4))
    return flags

def purity():
    print('Select purity one or more(Default 12):')
    print('1)SFW')
    print('2)Sketchy')
    print('3)NSFW')

    sel = input('Enter: ')
    uniq = set(sel)

    if not uniq.issubset({'1','2','3'}):
        print('Select only 1, 2 or 3')
        return purity()
    if sel == '':
        return '110'
    else:
        flags = ''.join('1' if str(i) in uniq else '0' for i in range(1,4))
    return flags

def ai_filter():
    print('AI filter(Default 1):')
    print('1)Turn')
    print('2)Off')
    choice = input('Enter: ')
    if choice in '12':
        return '1' if choice == '1' else '2'
    else:
        print('Select 1 or 2')
        return ai_filter()


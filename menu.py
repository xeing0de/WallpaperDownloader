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

    if not uniq.issubset({'','1','2','3'}):
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
    if choice in '12' and len(choise) <= 1:
        return '1' if choice == '1' or choise == '' else '2'
    else:
        print('Select 1 or 2')
        return ai_filter()

def sorting():
    print('Select type of sorting(Default Random):')
    print('1)Relevance  5)Favorites')
    print('2)Random     6)Toplist')
    print('3)Date added 7)Hot')
    print('4)Views')
    sort_type = {'1': 'relevance',
                 '2': 'random',
                 '3': 'date_added',
                 '4': 'views',
                 '5': 'favorites',
                 '6': 'toplist',
                 '7': 'hot'} 

    sort = input('Enter: ')
    if sort == '':
        return 'random'
    elif not sort in '1234567' or len(sort) > 1:
        print('Select only between 1-7')
        return sorting()
    return sort_type['sort']


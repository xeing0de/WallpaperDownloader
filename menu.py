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
    print('1)Turn 2)Off')
    choice = input('Enter: ')
    if choice in '12' and len(choice) <= 1:
        return '1' if choice == '1' or choice == '' else '2'
    else:
        print('Select 1 or 2')
        return ai_filter()

def sorting():
    print('Select type of sorting(default random):')
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
    return sort_type[sort]

def ratio():
    ratios = ['2560x1080','3440x1440','3840x1600','','',
              '1280x720','1600x900','1920x1080','2560x1440','3840x2160',
              '1280x800','1600x1000','1920x1200','2560x1600','3840x2400',
              '1280x960','1600x1200','1920x1440','2560x1920','3840x2880',
              '1280x1024','1600x1280','1920x1536','2560x2048','3840x3072']
    rtype = ['ultrawide','16:9','16:10','4:3','5:4']
    typ = {'1':'atleast','2':'resolutions'}
    print('Select resolution type(default atleast):')
    print('1)atleast 2)exactly\nadditional - 3)custom')
    custom = ''
    choice = input('Enter: ')
    uniq = set(choice)
    if (uniq.issubset({'','1','2','3'}) and not('1' in choice and '2' in choice)
    and choice != '3'):
        for i in range(5):
            print(rtype[i].ljust(9),end='| ')
            for j in range(i*5,5 + i*5):
                if ratios[j] != '':
                    print((str(j+1)+')'+ratios[j]).ljust(12),sep='',end='| ')
            print('\n'+'-'*80)
    else:
        print('Select only between 1-3')
        return ratio()

    if '3' in choice:
        print('Enter custom resolution: ',end='')
        custom = input()
        if custom == '':
            print('Custom is empty.')
            return ratio()
        if '1' in choice:
            if len(custom.split()) == 1:
                return typ['1'], custom
            else:
                print('Enter one.')
                return ratio()
    if '1' in choice:
        rezstring = input('Enter resolution: ')
    else:
        rezstring = input('Enter resolutions(separated by space): ')
    rez = rezstring.split()
    rez = ''.join(i for i in rez if i.isdigit() or i == ' ')
    if '1' in choice and len(rez) > 1:
        print('Too many screen resolutions, enter only one.')
        return ratio()
    else:
        back = ' '.join(ratios[int(i)] for i in rez)+custom
        return typ[choice.replace('3','')], back.replace(' ','%2C') 


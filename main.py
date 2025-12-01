import math
from pprint import pprint
from datetime import datetime, timedelta

tsoonifail = 'voistkonnad.txt'
tsooni_nr = 9
koduvõistkonna_nr = 5
algusaeg = '15:00'
algusaeg = datetime.strptime(algusaeg, "%H:%M")

berger5_1p1v = []
berger5_1p2v = []
berger5_2p1v = [(2, 5), (3, 4), (1, 2), (5, 3),
                (1, 4), (2, 3), (4, 5), (3, 1),
                (4, 2), (5, 1)]
berger5_2p2v = []

berger6_1p1v = []
berger6_1p2v = []
berger6_2p1v = [(2, 5), (3, 4), (1, 6), (5, 3),
                (1, 2), (6, 4), (3, 1), (4, 5),
                (2, 6), (1, 4), (2, 3), (6, 5),
                (4, 2), (3, 6), (5, 1)]

berger6_2p2v = [(2, 5), (3, 4), (1, 6), (5, 3),
                (1, 2), (6, 4), (4, 5), (2, 3),
                (2, 6), (1, 4), (3, 1), (6, 5),
                (4, 2), (3, 6), (5, 1)]


def loe_tsoon(tsoonifail, tsooni_nr):
    # sisend: tsoonifaili nimi, tsooni number
    # väljund: (linn, võistkonnad),
    # linn - tsooni linn
    # võistkonnad - järjend võistkondade nimedest antud tsoonis

    with open(tsoonifail, encoding='utf8') as f:
        on_tsoonis = False
        võistkonnad = []
        tsooni_linn = ''
        for rida in f:
            if not rida.strip():
                continue 
            elif rida.startswith('#'):
                (nr, linn) = rida.removeprefix('#').split(',')
                if int(nr) == tsooni_nr:
                    on_tsoonis = True
                    tsooni_linn = linn.strip()
                else:
                    on_tsoonis = False
            elif on_tsoonis:
                võistkonnad.append(rida.strip())
        return (tsooni_linn, võistkonnad)


def märgi_koduvõistkond(võistkonnad, koduvõistkond, kodu_nr):
    # sisend: võistkondade nimede järjend, koduvõistkonna nimi, kodu võistkonna nr, nt 5
    # väljund: võistkondade järjendis on liigutatud koduvõistkonna nimi positsioonile kodu_nr
    if võistkonnad[kodu_nr - 1] == koduvõistkond:
        return võistkonnad
    else:
        i = võistkonnad.index(koduvõistkond)
        võistkonnad[i] = võistkonnad[kodu_nr - 1]
        võistkonnad[kodu_nr - 1] = koduvõistkond
    return võistkonnad


def loo_võistluspaarid(berger, võistkonnad):
    # sisend:
    # berger - võistluspaaroide järjend
    # võistkonnad - võistkondade nimede järjend
    # väljund: võistkondade nimede paaride järjend
    
    võistlustabel = []
    
    kombinatsioonide_arv = math.perm(len(võistkonnad), 2) / math.factorial(2)
    try:
        if  kombinatsioonide_arv == len(berger):
 
             for (a, b) in berger:
                paar = (võistkonnad[a - 1], võistkonnad[b - 1])
                võistlustabel.append(paar)

        else:
            raise ValueError('Võistkondade arv ei klapi bergeri süsteemiga!')
    except ValueError as e:
        print(e)
        return -1
    except IndexError as e:
        print(a,b)
        return -1

    return võistlustabel


def kuva_võistlustabel(võistluspaarid, algusaeg, kakspäeva = True):
    print('1. päev')
    t = algusaeg
    for i, paar in enumerate(võistluspaarid):

        print(f'Mäng nr {i + 1}')
        if kakspäeva and i == len(võistluspaarid) // 2:
            print('2. päev')
            t = algusaeg
            
        if all(isinstance(x, list) for x in võistluspaarid):
            ((a, b), (c, d)) = paar
            print('1. väljak')
            print(f'{t.hour:02d}:{t.minute:02d}, {i + 1}. {a} - {b}')
            print('2. väljak')
            print(f'{t.hour:02d}:{t.minute:02d}, {i + 1}. {c} - {d}')
        elif all(isinstance(x, tuple) for x in võistluspaarid):
            (a, b) = paar
            print(f'{t.hour:02d}:{t.minute:02d}, {i + 1}. {a} - {b}')
        
        t = t + timedelta(hours=1, minutes=15)

def jaga_kaheks_väljakuks(võistluspaarid):
    võistlustabel = []
    mäng = []
    
    for i, paar in enumerate(võistluspaarid):
        mäng.append(paar)
        if i % 2:
            võistlustabel.append(mäng)
            mäng = []
    
    if len(mäng): # kuu on paaritu arv mänge siis lisa tühi mäng viimasele väljakule
        mäng.append(('', ''))
        võistlustabel.append(mäng)
    
    return võistlustabel

(linn, võistkonnad) = loe_tsoon(tsoonifail, tsooni_nr)
#märgi_koduvõistkond(võistkonnad, 'Rae SK I (M.S)', koduvõistkonna_nr)
võistluspaarid = loo_võistluspaarid(berger6_2p2v, võistkonnad)
#kuva_võistlustabel(võistluspaarid, True)
kuva_võistlustabel(jaga_kaheks_väljakuks(võistluspaarid), algusaeg, True)
#kuva_võistlustabel(võistluspaarid, algusaeg, True)

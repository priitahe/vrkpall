from pprint import pprint
from datetime import datetime, timedelta

tsoonifail = 'voistkonnad.txt'
tsooni_nr = 1
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
            rida = rida.strip()
        
            if not rida:  # kui on tühi rida
                continue 
            
            if rida.startswith('#'): # sellest reast algab tsoon
                tsoon_lst = rida.removeprefix('#').split(',')
                
                if len(tsoon_lst) == 2:
                    (nr, linn) = tsoon_lst
                    nr = int(nr)
                    linn = linn.strip
                else:
                    continue
                
                if nr == tsooni_nr:
                    on_tsoonis = True
                    tsooni_linn = linn
                else:
                    on_tsoonis = False

            elif on_tsoonis:
                 võistkonnad.append(rida)
        
        return (tsooni_linn, võistkonnad)


def märgi_koduvõistkond(võistkonnad, koduvõistkond, kodu_nr):
    # sisend: võistkondade nimede järjend, koduvõistkonna nimi, kodu võistkonna nr, nt 5
    # väljund: võistkondade järjendis on liigutatud koduvõistkonna nimi positsioonile kodu_nr
    nr = kodu_nr - 1
    
    try:
        i = võistkonnad.index(koduvõistkond)
    except ValueError:
        raise ValueError(f'Võistkonda {koduvõistkond} ei leitud!')
    
    võistkonnad[i], võistkonnad[nr] = (võistkonnad[nr], võistkonnad[i])
    return võistkonnad


def loo_võistluspaarid(berger, võistkonnad):
    # sisend:
    # berger - võistluspaaroide järjend
    # võistkonnad - võistkondade nimede järjend
    # väljund: võistkondade nimede paaride järjend
    
    n = len(võistkonnad)
    Cnnnn = n * (n - 1) // 2
    
    if Cnnnn != len(berger):
        print(f'Võistkondade arv ei klapi bergeri süsteemiga! berger {len(berger)}, võistkonnad {Cnnnn}')
        return -1
    
    võistlustabel = []

    for (a, b) in berger:
        try:
            paar = (võistkonnad[a - 1], võistkonnad[b - 1])
        except IndexError:
            raise(f'Vigased indeksid {a} ja {b}')
        
        võistlustabel.append(paar)
    
    return võistlustabel


def kuva_võistlustabel(võistluspaarid, algusaeg, kakspäeva = True):
    def aegstr():
        return f'{t.hour:02d}:{t.minute:02d}'
        
    print('1. päev')
    t = algusaeg
    
    for i, paar in enumerate(võistluspaarid):

        if kakspäeva and i == len(võistluspaarid) // 2:
            print('2. päev')
            t = algusaeg

        print(f'Mäng nr {i + 1}')
        
            
        if isinstance(paar, tuple) and len(paar) == 2:
            (a, b) = paar
            print(f'{aegstr()}, {i + 1}. {a} - {b}')

        elif isinstance(paar, list) and len(paar) == 2:
            ((a, b), (c, d)) = paar
            print('1. väljak')
            print(f'{aegstr()}, {i + 1}. {a} - {b}')
            print('2. väljak')
            print(f'{aegstr()}, {i + 1}. {c} - {d}')
        else:
            raise ValueError(f'Vigane paar: {paar}')
        
        t = t + timedelta(hours=1, minutes=15)

def jaga_kaheks_väljakuks(võistluspaarid):
    võistlustabel = []
    mäng = []
    
    for paar in võistluspaarid:
        mäng.append(paar)
        if len(mäng) == 2:
            võistlustabel.append(mäng)
            mäng = []
    
    if mäng: # kuu on paaritu arv mänge siis lisa tühi mäng viimasele väljakule
        mäng.append(('', ''))
        võistlustabel.append(mäng)
    
    return võistlustabel

(linn, võistkonnad) = loe_tsoon(tsoonifail, tsooni_nr)
#märgi_koduvõistkond(võistkonnad, 'Rae SK I (M.S)', koduvõistkonna_nr)
võistluspaarid = loo_võistluspaarid(berger5_2p1v, võistkonnad)
#kuva_võistlustabel(võistluspaarid, True)
kuva_võistlustabel(jaga_kaheks_väljakuks(võistluspaarid), algusaeg, True)
#kuva_võistlustabel(võistluspaarid, algusaeg, True)

from pprint import pprint
from datetime import datetime, timedelta
import tkinter as tk
from tkinter import ttk, messagebox
import random

tsoonifail = 'voistkonnad.txt'

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
        
            if not rida:  # kui on tühi rida, siis hüppa üle
                continue 
            
            if rida.startswith('#'): # sellest reast algab tsoon
                tsoon_lst = rida.removeprefix('#').split(',')
                
                if len(tsoon_lst) == 2: # kas tsooni rida on #nr,linn
                    (nr, linn) = tsoon_lst
                    nr = int(nr)
                    linn = linn.strip() # tundub, et siin peavad ka sulud olema
                else:
                    continue
                
                if nr == tsooni_nr:  #
                    on_tsoonis = True
                    tsooni_linn = linn
                else:
                    on_tsoonis = False

            elif on_tsoonis:
                 #eelamdame numbri ja sümbolid alguset, kui neid on 
                 #nt "1. Rae SK" -> "Rae SK"
                 puhastatud = rida .lstril("0123456789. )").strip()
                 if puhastatud:
                   võistkonnad.append(puhastatud)
        
        if not võistkonnad:
            raise ValueError(f'Tsooni {tsooni_nr} ei leitud või selles pole võistkonda')
        
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
    Cnnnn = n * (n - 1) // 2    # siia tuleb kirjutada valem faktoriaalidega, kui n = 1, siis vastus on 0, kuid peaks olema 1
    
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


def kuva_võistlustabel(võistluspaarid, algusaeg1, kakspäeva = True, algusaeg2 = None, mängu_kestus=timedelta(hours=1, minutes=15)):
    def aegstr():
        return f'{t.hour:02d}:{t.minute:02d}'
    if algusaeg2 is None: # I päeva alguse (datetime).kas neid tingimusi ei pea juurde panema
      algusaeg2 = algusaeg1 #samuti ka see
      
    print('1. päev')
    t = algusaeg1
    
    for i, paar in enumerate(võistluspaarid):

        if kakspäeva and i == len(võistluspaarid) // 2:
            print('2. päev')
            t = algusaeg2

        print(f'Mäng nr {i + 1}')
        
            
        if isinstance(paar, tuple) and len(paar) == 2: # kontrollib kas element on ennik (a, b)
            (a, b) = paar
            print(f'{aegstr()}, {i + 1}. {a} - {b}')

        elif isinstance(paar, list) and len(paar) == 2: # kontrollib kas element on järjend
            ((a, b), (c, d)) = paar
            print('1. väljak')
            print(f'{aegstr()}, {i + 1}. {a} - {b}')
            print('2. väljak')
            print(f'{aegstr()}, {i + 1}. {c} - {d}')
        else:
            raise ValueError(f'Vigane paar: {paar}')
        
        t = t + mängu_kestus

def kontrollo_järjestikuseid(võistluspaarid, kahepäevane):
  # kontrollib, kas mõnel on üle kahe järjestikuse mängu ühe päeva sees
  from collection import defaultdict

  tiimi_mängud = defaultdict(list)
  for i, paar in enumerate(võistluspaarid, start=1):
    if isinstance(paar, tuple):
      a, b = paar
      for t in (a, b):
        tiimi_mängud[t].append(i)
    elif isinstance(paar, list):
      for (a, b) in paar:
        for t in (a, b):
          tiimi_mängud[t].append(i)

    rikkumised = {}
    piir = len(võistluspaarid) // 2 if kahepäevane else len(võistluspaarid)

    for t, mängud in tiimi_mängud.items():
        päev1 = [m for m in mängud if m <= piir]
        päev2 = [m for m in mängud if m > piir]
        for päev, nimi in ((päev1, "I päev"), (päev2, "II päev")):
            järjest = 1
            for i in range(1, len(päev)):
                if päev[i] == päev[i - 1] + 1:
                    järjest += 1
                    if järjest > 2:
                        rikkumised[t] = f"rohkem kui 2 järjest ({nimi})"
                        break
                else:
                    järjest = 1

    return rikkumised

def jaga_kaheks_väljakuks(võistluspaarid):
    # grupeerib järjendi elemendid paarikaupa, tagastab järjendi, mille elemendid on
    # kahemelemendilised järjendid
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
def sea_koduvõistkond_väljakule_1(tabel, koduvõistkond):
    """
    Tagab, et kui ajaslotis on 2 mängu (2 väljakut),
    siis koduvõistkonna mäng on alati 1. väljakul.

    tabel – list, mille elemendid on:
      - kas tuple (a, b)  -> üks väljak
      - või list [(a, b), (c, d)] -> 2 väljakut samal ajal
    """
    uus_tabel = []

    for slot in tabel:
        # üksik mäng (ainult 1 väljak) – midagi vaja teha ei ole
        if isinstance(slot, tuple):
            uus_tabel.append(slot)
        elif isinstance(slot, list) and len(slot) == 2:
            m1, m2 = slot
            # kui koduvõistkond on ainult teises mängus, vahetame järjekorra
            if (koduvõistkond in m2) and (koduvõistkond not in m1):
                uus_tabel.append([m2, m1])
            else:
                uus_tabel.append(slot)
        else:
            # igaks juhuks
            uus_tabel.append(slot)

    return uus_tabel


from collections import defaultdict

def jaga_kaheks_väljakuks_piiranguga(võistluspaarid, max_järjest=2):
    """
    Jagab mängud ajas 'slotideks' nii, et:
      - igas slotis on 1 või 2 mängu (2 väljakut);
      - ükski võistkond ei mängi rohkem kui `max_järjest` slotis järjest.

    Tagastab sama formaati, mida kuva_võistlustabel ootab:
      [ (a,b), [ (c,d), (e,f) ], (g,h), ... ]
    """
    slots = []              # iga element: [mäng] või [mäng1, mäng2]
    team_slots = defaultdict(list)  # team -> slotide indeksid, kus ta mängib

    for match in võistluspaarid:
        a, b = match
        placed = False

        # proovime leida esimese sobiva sloti
        for s in range(len(slots) + 1):
            # kui jõuame uue slotini, lisame tühja
            if s == len(slots):
                slots.append([])

            # slot täis?
            if len(slots[s]) >= 2:
                continue

            # kas samas slotis juba mängib kumbki tiim?
            if any(a in m or b in m for m in slots[s]):
                continue

            def ok_for_team(team):
                prev = team_slots[team]
                if len(prev) < max_järjest:
                    return True
                # vaatame viimased max_järjest sloti + praeguse
                tail = prev[-max_järjest:] + [s]
                # kas need on järjestikused indeksid, nt [3,4,5] ?
                if len(tail) == max_järjest + 1:
                    if all(tail[i+1] - tail[i] == 1 for i in range(len(tail) - 1)):
                        return False
                return True

            if not (ok_for_team(a) and ok_for_team(b)):
                continue

            # sobib – paigutame siia
            slots[s].append(match)
            team_slots[a].append(s)
            team_slots[b].append(s)
            placed = True
            break

        if not placed:
            # kui ei leidnud ühtegi sobivat slotti
            # (väga harv juhus – paneme uude slotti ilma lisakontrollita)
            s = len(slots)
            slots.append([match])
            team_slots[a].append(s)
            team_slots[b].append(s)

    # teisendame slots struktuuri selleks, mida kuva_võistlustabel ootab
    tabel = []
    for slot in slots:
        if len(slot) == 1:
            tabel.append(slot[0])      # üks tuple
        elif len(slot) == 2:
            tabel.append(slot)         # list kahest tuple'ist
        else:
            raise ValueError("Ühes ajasammus on rohkem kui 2 mängu – midagi on viltu.")
    return tabel


def vali_berger_ja_väljakud(võistkondade_arv, võistluse_tüüp):
  # Valib: õige Bergeri tabeli (5 v 6 võistkonda, 2p1v alus), mitu väljakut (1v2), kas 1-v2-päevane.
  
  if võistkondade_arv == 5:
    berger = berger5_2p1v
    
  elif võistkondade_arv == 6:
    berger = berger6_2p1v
  else:
    raise ValueError("Toetatud on ainult 5 või 6 võistkonda.")
  kahel_väljakul = "kahel väljakul" in võistluse_tüüp
  kahepäevane = "kahepäevane" in võistluse_tüüp

  väljakuid = 2 if kahel_väjakul else 1
  
  return berger, väljakuid, kahepäevane
  
def genereeri_ajakava_gui(vanuseklass, kuupäev, võistluse_tüüp, algus1, algus2, võistkonnad, kodu_võistkond_nimi, asukoht="", värvid=None):
  if len(võistkonnad) not in (5, 6):
        raise ValueError("Praegu on toetatud ainult 5 või 6 võistkonnaga turniir.")
  try: 
    algus1_dt = datetime.strptime(f"{kuupäev} {algus1}", "%Y-%m-%d %H:%M")
  except ValueError:
    raise ValueError("I päeva algusaeg või kuupäev on vales formaadis (kasuta YYYY-MM-DD ja HH:MM).")

  try:
    algus2_dt = datetime.strptime(f"{kuupäev} {algus2}", "%Y-%m-%d %H:%M")
  except ValueError:
    algus2_dt = None

  if vanuseklass == "U16":
        mängu_kestus = timedelta(hours=1, minutes=15)
    else:  
        mängu_kestus = timedelta(hours=2)

  võistkonnad = võistkonnad[:]
  
  if kodu_võistkond_nimi.strip():
    if kodu_võistkond_nimi.strip() not in võistkonnad:
      raise ValueError("Koduvõistkond peab olema valitud võistkondade seas.")
       
    märgi_koduvõistkond(võistkonnad, kodu_võistkond_nimi.strip(), koduvõistkonna_nr)

  berger, väljakuid, kahepäevane = vali_berger_ja_väljakud(len(võistkonnad), võistluse_tüüp)

  võistluspaarid = loo_võistluspaarid(berger, võistkonnad)
  if võistluspaarid == -1:
    raise ValueError("Bergeri tabel ei klappinud võistkondade arvuga.")

  if väljakuid == 2:
    try: 
      tabel = jaga_kaheks_väljakuks_piiranguga(võistluspaarid, max_järjest=2)
    except ValueError:
      tabel = jaga_kaheks_väljakuks(võistluspaarid)
  else:
    tabel = võistluspaarid

  print()
  print("==========================================")
  if asukoht:
    print(f"Asukoht: {asukoht}")
  print(f"Kuupäev: {kuupäev}, vanuseklass: {vanuseklass}")
  print(f"Võistluse tüüp: {võistluse_tüüp}")
  print("Osalevad võistkonnad:")
  for v in võistkonnad:
    print(" - ", v)
  print("==========================================")
  
  
  if kahepäevane and algus2_dt is not None:
    kuva_võistlustabel(tabel, algus1_dt, kakspäeva=True, algusaeg2=algus2_dt, mängu_kestus=mängu_kestus)
  else:
    kuva_võistlustabel(tabel, algus1_dt, kakspäeva=False, mängu_kestus=mängu_kestus)

  rikkumised = kontrolli_järjestikuseid(tabel, kahepäevane) #kontrollib, et poleks rohkem kui 2 järjestikust mängu päevas
    if rikkumised:
        print("\n⚠️  Järjestikuste mängude piirangu rikkumised:")
        for t, põhjus in rikkumised.items():
            print(f" - {t}: {põhjus}")
    else:
        print("\n✅ Kõik võistkonnad vastavad järjestikuse mängu piirangule!")


def loo_gui(): #Sellega peaks siis saama luua akent ehk kasutajaliidest:valida vanuseklassi, sisestada kuupäeva, valida võistlsue tüüp 1/2päeva, 1/2väljakut), isestada päevade algusajad, koduvõistkonnanimi ning lõpuks geenereerida ajakava.
  root = tk.Tk()
  root.title("Võrkpalli võistluse ajakava")

    # --- ALLIKAVALIK: tsoonist vs käsitsi ---
  allikas_var = tk.StringVar(value="tsoon")

  ttk.Label(root, text="Võistkondade allikas:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
  ttk.Radiobutton(root, text="Loe tsoonifailist", variable=allikas_var, value="tsoon").grid(row=0, column=1, sticky="w")
  ttk.Radiobutton(root, text="Sisesta käsitsi", variable=allikas_var, value="käsitsi").grid(
      row=0, column=2, sticky="w")

    # tsooni number
  ttk.Label(root, text="Tsooni number (1–10):").grid(row=1, column=0, sticky="w", padx=5, pady=5)
  tsoon_spin = tk.Spinbox(root, from_=1, to=10, width=5)
  tsoon_spin.grid(row=1, column=1, sticky="w")

    # käsitsi võistkondade sisestus
  ttk.Label(root, text="Võistkonnad (üks rida = üks võistkond):").grid(row=2, column=0, columnspan=3, sticky="w", padx=5, pady=5)
  sisestus_box = tk.Text(root, height=6, width=50)
  sisestus_box.grid(row=3, column=0, columnspan=3, padx=5, pady=5)

    # Tkinteri muutujad
  vanuse_var = tk.StringVar(value="U16")
  kuupäev_var = tk.StringVar(value="2025-12-15")
  tüüp_var = tk.StringVar(value="kahepäevane kahel väljakul")
  algus1_var = tk.StringVar(value="10:00")
  algus2_var = tk.StringVar(value="10:00")
  kodu_var = tk.StringVar(value="")  # koduvõistkonna nimi (vaba tekst)

    # vanuseklass
  ttk.Label(root, text="Vanuseklass:").grid(row=4, column=0, sticky="w", padx=5, pady=5)
  ttk.Radiobutton(root, text="U16", variable=vanuse_var, value="U16").grid(row=4, column=1, sticky="w")
  ttk.Radiobutton(root, text="U18", variable=vanuse_var, value="U18").grid(row=4, column=2, sticky="w")
  ttk.Radiobutton(root, text="U20", variable=vanuse_var, value="U20").grid(row=4, column=3, sticky="w")

    # kuupäev
  ttk.Label(root, text="Võistluse kuupäev (YYYY-MM-DD):").grid(row=5, column=0, sticky="w", padx=5, pady=5)
  ttk.Entry(root, textvariable=kuupäev_var, width=15).grid(row=5, column=1, sticky="w")

    # võistluse tüüp
  ttk.Label(root, text="Võistluse tüüp:").grid(row=6, column=0, sticky="w", padx=5, pady=5)
  tüüp_combo = ttk.Combobox(
      root, textvariable=tüüp_var, values=[
          "ühepäevane ühel väljakul",
          "ühepäevane kahel väljakul",
          "kahepäevane ühel väljakul",
          "kahepäevane kahel väljakul",
      ], state="readonly", width=28)
  tüüp_combo.grid(row=6, column=1, sticky="w")

    # algusajad
  ttk.Label(root, text="Algusaeg I päeval (HH:MM):").grid(row=7, column=0, sticky="w", padx=5, pady=5)
  ttk.Entry(root, textvariable=algus1_var, width=8).grid(row=7, column=1, sticky="w")

  ttk.Label(root, text="Algusaeg II päeval (HH:MM):").grid(row=8, column=0, sticky="w", padx=5, pady=5)
  ttk.Entry(root, textvariable=algus2_var, width=8).grid(row=8, column=1, sticky="w")

    # koduvõistkond
  ttk.Label(root, text="Koduvõistkonna nimi:").grid(row=9, column=0, sticky="w", padx=5, pady=5)
  ttk.Entry(root, textvariable=kodu_var, width=30).grid(row=9, column=1, columnspan=2, sticky="w")


  
  #ajakava genereerimise nupp
  def nupp_genereeri():
    try:
      allikas = allikas_var.get()
      asukoht = ""

      if allikas == "tsoon":
        # loe valitud tsoon failist
        try:
          tsooni_nr = int(tsoon_spin.get())
        except ValueError:
          raise ValueError("Tsooni number peab olema täisarv 1–10.")
        linn, võistkonnad = loe_tsoon(tsoonifail, tsooni_nr)
        asukoht = f"Tsoon {tsooni_nr}, {linn}"
      else:
        # loe võistkonnad käsitsi sisestatud tekstist
        tekst = sisestus_box.get("1.0", tk.END).strip()
        read = tekst.splitlines()
        võistkonnad = []
        for rida in read:
          r = rida.strip()
          if not r:
            continue
        # eemaldame võimalikud numbrid algusest (kui kasutaja kleepis koos nr-ga)
          r = r.lstrip("0123456789. )").strip()
          if r:
            võistkonnad.append(r)
        #Asukoht = koduvõistkond, kui see on valitud
         kodu_nimi = kodu_var.get().strip()
         if kodu_nimi:
           asukoht = kodu_nimi
                
         else:
           asukoht = "Käsitsi sisestatud"

         if len(võistkonnad) == 0:
           raise ValueError("Võistkondi ei leitud. Kontrolli tsooni numbrit või sisestatud nimesid.")
         if len(võistkonnad) not in (5, 6):
           raise ValueError(f"Praegu on toetatud ainult 5 või 6 võistkonnaga turniir. Leiti: {len(võistkonnad)}.")

    
         värvid = {}
         for v in võistkonnad:
         # vali suvaline hele värv (pastell)
           r = random.randint(150, 255)
           g = random.randint(150, 255)
           b = random.randint(150, 255)
           värvid[v] = f'#{r:02x}{g:02x}{b:02x}'
      
         genereeri_ajakava_gui(vanuseklass=vanuse_var.get(), kuupäev=kuupäev_var.get(), võistluse_tüüp=tüüp_var.get(), algus1=algus1_var.get(), algus2=algus2_var.get(), valitud_võistkonnad=valitud_võistkonnad, kodu_võistkond_nimi=kodu_var.get())
         messagebox.showinfo("Valmis", "Ajakava genereeritud (vaata terminali väljundit).")
      except Exception as e:
        messagebox.showerror("Viga", str(e))
  ttk.Button(root, text="Genereeri ajakava", command=nupp_genereeri).grid(row=8, column=0, columnspan=2, pady=10)

  root.mainloop()

if __name__ == "__main__":
  loo_gui()

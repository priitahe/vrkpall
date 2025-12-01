from pprint import pprint
from datetime import datetime, timedelta
import tkinter as tk
from tkinter import ttk, messagebox

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
                 võistkonnad.append(rida)
        
        if not võistkonnad:
            raise ValueError(f'Tsooni ei leitud: {tsooni_nr}')
        
        return (tsooni_linn, võistkonnad)

def loe_koik_võistkonnad(tsoonifail):
    #Loeb failist KÕIK võistkonnad (kõikidest tsoonidest).
    võistkonnad = []
    with open(tsoonifail, encoding="utf8") as f:
        for rida in f:
            rida = rida.strip()
            if not rida:
                continue
            if rida.startswith("#"):
                # tsoonirida (#10, Tallinn jne) – selle jätame vahele
                continue
            võistkonnad.append(rida)
    return võistkonnad

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

def vali_berger_ja_väljakud(võistkondade_arv, võistluse_tüüp):
  ühepäevane = "ühepäevane" in võistluse_tüüp
  kahepäevane = "kahepäevane" in võistluse_tüüp
  kahel_väljakul = "kahel väljakul" in võistluse_tüüp 

  väljakuid = 2 if kahel_väljakul else 1

  if võistkondade_arv == 5:
    if kahepäevane and not kahel_väljakul:
      berger = berger5_2p1v
    elif kahepäevane and kahel_väljakul:
      berger = berger5_2p2v
    elif ühepäevane and not kahel_väljakul:
      berger = berger5_1p1v
    else:
      berger = berger5_1p2v
  elif võistkondade_arv == 6:
    if kahepäevane and not kahel_väljakul:
      berger = berger6_2p1v
    elif kahepäevane and kahel_väljakul:
      berger = berger6_2p2v
    elif ühepäevane and not kahel_väljakul:
      berger = berger6_1p1v
    else:
      berger = berger6_1p2v
  else:
    raise ValueError("Selles programmis on toetatud ainult 5 või 6 võistkonnaga.")

  if not berger:
    raise ValueError("Selle võistluse tüübi jaoks ei ole Bergeri tabelit (muutuja on tühi).")

  return berger, väljakuid, kahepäevane
  
def genereeri_ajakava_gui(vanuseklass, kuupäev, võistluse_tüüp, algus1, algus2, kodu_võistkond_nimi):
  if len(valitud_võistkonnad) not in (5, 6):
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

  võistkonnad = valitud_võistkonnad[:]
  
  if kodu_võistkond_nimi.strip():
    if kodu_võistkond_nimi.strip() not in võistkonnad:
      raise ValueError("Koduvõistkond peab olema valitud võistkondade seas.")
       
    märgi_koduvõistkond(võistkonnad, kodu_võistkond_nimi.strip(), koduvõistkonna_nr)

  berger, väljakuid, kahepäevane = vali_berger_ja_väljakud(len(võistkonnad), võistluse_tüüp)

  võistluspaarid = loo_võistluspaarid(berger, võistkonnad)
  if võistluspaarid == -1:
    raise ValueError("Bergeri tabel ei klappinud võistkondade arvuga.")

  if väljakuid == 2:
    tabel = jaga_kaheks_väljakuks(võistluspaarid)
  else:
    tabel = võistluspaarid

  print()
  print("==========================================")
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

def loo_gui(): #Sellega peaks siis saama luua akent ehk kasutajaliidest:valida vanuseklassi, sisestada kuupäeva, valida võistlsue tüüp 1/2päeva, 1/2väljakut), isestada päevade algusajad, koduvõistkonnanimi ning lõpuks geenereerida ajakava.
  try:
    kõik_võistkonnad = loe_koik_võistkonnad(tsoonifail)
  except Exception as e:
    print("Viga võistkondade lugemisel:", e)
    return 
  if not kõik_võistkonnad:
    print("Failist ei leitud ühtegi võistkonda.")
    return
    
  root = tk.Tk()
  root.title("Võrkpalli võistluse ajakava")

   #Tkinteri muutujad (hoiavad kasutaja sisestatud väärtusi)
  vanuse_var = tk.StringVar(value="U16")
  kuupäev_var = tk.StringVar(value="2025-12-15")
  tüüp_var = tk.StringVar(value="kahepäevane kahel väljakul")
  algus1_var = tk.StringVar(value="10:00")
  algus2_var = tk.StringVar(value="10:00")
  kodu_var = tk.StringVar(value=kõik_võistkonnad[0]) #vaikimisi esimene

   # võistkondade valik
  ttk.Label(root, text="Kõik võistkonnad (vali osalejad):").grid(row=0, column=0, columnspan=2, sticky="w", padx=5, pady=5)

  võistkonna_listbox = tk.Listbox(root, selectmode="extended", height=10, width=40)
  for nimi in kõik_võistkonnad:
    võistkonna_listbox.insert(tk.END, nimi)
  võistkonna_listbox.grid(row=1, column=0, columnspan=2, sticky="w", padx=5)

  #koduvõistkond
  ttk.Label(root, text="Koduvõistkonna nimi:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
  kodu_combo = ttk.Combobox(root, textvariable=kodu_var, values=võistkonnad, state="readonly", width=37)
  kodu_combo.grid(row=2, column=1, columnspan=3, sticky="w")

  
   #vanuseklass
  ttk.Label(root, text="Vanuseklass:").grid(row=3, column=0, sticky="w", padx=5, pady=5)
  ttk.Radiobutton(root, text="U16", variable=vanuse_var, value="U16").grid(row=3, column=1, sticky="w")
  ttk.Radiobutton(root, text="U18", variable=vanuse_var, value="U18").grid(row=3, column=2, sticky="w")
  ttk.Radiobutton(root, text="U20", variable=vanuse_var, value="U20").grid(row=3, column=3, sticky="w")

  #kuupäev
  ttk.Label(root, text="Võistluse kuupäev (YYYY-MM-DD):").grid(row=4, column=0, sticky="w", padx=5, pady=5)
  ttk.Entry(root, textvariable=kuupäev_var, width=12).grid(row=4, column=1, sticky="w")

  #võistluse tüüp
  ttk.Label(root, text="Võistluse tüüp:").grid(row=5, column=0, sticky="w", padx=5, pady=5)
  tüüp_combo = ttk.Combobox(root, textvariable=tüüp_var, values=["ühepäevane ühel väljakul", "ühepäevane kahel väljakul", "kahepäevane ühel väljakul", "kahepäevane kahel väljakul",], state="readonly", width=28)
  tüüp_combo.grid(row=5, column=1, columnspan=3, sticky="w")

  #algusajad
  ttk.Label(root, text="Algusaeg I päeval (HH:MM):").grid(row=6, column=0, sticky="w", padx=5, pady=5)
  ttk.Entry(root, textvariable=algus1_var, width=8).grid(row=6, column=1, sticky="w")

  ttk.Label(root, text="Algusaeg II päeval (HH:MM):").grid(row=7, column=0, sticky="w", padx=5, pady=5)
  ttk.Entry(root, textvariable=algus2_var, width=8).grid(row=7, column=1, sticky="w")

  
  #ajakava genereerimise nupp
  def nupp_genereeri():
    try:
      indeksid = võistkonna_listbox.curselection()
      if not indeksid:
        raise ValueError("Palun vali listist 5 või 6 võistkonda.")
      valitud_võistkonnad = [kõik_võistkonnad[i] for i in indeksid]
      
      genereeri_ajakava_gui(vanuseklass=vanuse_var.get(), kuupäev=kuupäev_var.get(), võistluse_tüüp=tüüp_var.get(), algus1=algus1_var.get(), algus2=algus2_var.get(), valitud_võistkonnad=valitud_võistkonnad, kodu_võistkond_nimi=kodu_var.get())
      messagebox.showinfo("Valmis", "Ajakava genereeritud (vaata terminali väljundit).")
    except Exception as e:
      messagebox.showerror("Viga", str(e))
  ttk.Button(root, text="Genereeri ajakava", command=nupp_genereeri).grid(row=8, column=0, columnspan=2, pady=10)

  root.mainloop()

if __name__ == "__main__":
  loo_gui()

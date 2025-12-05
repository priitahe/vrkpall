import csv
import io
import tkinter as tk
from tkinter import ttk, messagebox
from pprint import pprint
from datetime import datetime, timedelta
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, PageBreak
from reportlab.lib import colors


# BERGERI TABELID

berger = {
    '5_1p1v': [
        #1p
        (2, 5), (3, 4), (1, 2), (5, 3), (1, 4),
        (2, 3), (4, 5), (3, 1), (4, 2), (5, 1),
    ],
    '5_2p1v': [
        #1p
        (2, 5), (3, 4), (1, 2), (5, 3), (1, 4),
        #2p
        (2, 3), (4, 5), (3, 1), (4, 2), (5, 1),
    ],
    
    '5_1p2v': [
        #1p
        (2, 5), (3, 4),
        (1, 2), (5, 3),
        (1, 4), (2, 3),
        (4, 5), (3, 1),
        (4, 2), (5, 1),
    ],
    '5_2p2v': [
        #1p
        (2, 5), (3, 4),
        (1, 2), (5, 3),
        (1, 4), (2, 3),
        #2p
        (4, 5), (3, 1),
        (4, 2), (5, 1),
    ],
    

    '6_1p1v': [
        #1p
        (2, 5), (3, 4), (1, 6), (5, 3), (1, 2),
        (6, 4), (3, 1), (4, 5), (2, 6), (1, 4),
        (2, 3), (6, 5), (4, 2), (3, 6), (5, 1),
    ],
    '6_2p1v': [
        #1p
        (2, 5), (3, 4), (1, 6), (5, 3), (1, 2), (6, 4), (3, 1), (4, 5),
        #2p
        (2, 6), (1, 4), (2, 3), (6, 5), (4, 2), (3, 6), (5, 1),
    ],
    
    '6_1p2v': [
        #1p
        (2, 5), (3, 4),
        (1, 6), (5, 3),
        (1, 2), (6, 4),
        (4, 5), (2, 3),
        (2, 6), (1, 4),
        (3, 1), (6, 5),
        (4, 2), (3, 6),
        (5, 1),
    ],
    '6_2p2v': [
        #1p
        (2, 5), (3, 4),
        (1, 6), (5, 3),
        (1, 2), (6, 4),
        (4, 5), (2, 3),
        #2p
        (2, 6), (1, 4),
        (3, 1), (6, 5),
        (4, 2), (3, 6),
        (5, 1), 
    ],
}



# FAILIST LUGEMINE


def loe_tsoon(tsoonifail, tsooni_nr):
    """
    Loeb failist võistkondade nimed valitud tsoonis.
    
    Args:
        tsoonifail (str): Failinimi võistkondade nimedega.
            Tsooni algus on rida kujul '#10, Tallinn'.
            Järgmised read kuni järgmise tsoonini või faili lõpuni
            kuuluvad sellesse tsooni.
        tsooni_nr (int): Tsooni number.
        
    Returns:
        tuple[str, list[str]]:
            Paar (str, list[str]), kus
            - esimene element on linna nimi (str).
            - teine element võistkondade nimed (list[str]).
        
    Raises:
        ValueError: Kui tsooni_nr vastavat tsooni failis ei ole.
    
    """
    with open(tsoonifail, encoding='utf8') as f:
        def tsooni_päis(tsooni_str):
            """
                Loeb stringist tsooni numbri ja tsoonivõistluse linna.
            """
            (nr, linn) = tsooni_str
            return int(nr), linn.strip()
        
        on_tsoonis = False
        võistkonnad = []
        
        for rida in f:
            rida = rida.strip()
            if not rida:
                continue
            
            # Tsooni päis. Kui võimaliks alusta võistkondade järjendi loomist
            if rida.startswith('#'):
                if on_tsoonis:
                    break
                
                # Töötle tsooni rida
                tsoon_lst = rida.removeprefix('#').split(',')
                nr, linn = tsooni_päis(tsoon_lst)
                if nr == tsooni_nr:
                    on_tsoonis = True

            elif on_tsoonis:
                võistkonnad.append(rida)
        
        if not võistkonnad:
            raise ValueError(f'Tsooni {tsooni_nr} ei leitud või tsoonis pole võistkondi.')
        
        return linn, võistkonnad

# TURNIIRI LOOGIKA

def liiguta_koduvõistkond(võistkonnad, koduvõistkond, kodu_nr):
    """
        Liigutab koduvõistkonna nime antud positsiooni.    
    """
    nr = kodu_nr - 1
    
    try:
        i = võistkonnad.index(koduvõistkond)
    except ValueError:
        raise ValueError(f'Võistkonda "{koduvõistkond}" ei leitud!')
    
    võistkonnad[i], võistkonnad[nr] = (võistkonnad[nr], võistkonnad[i])
    return võistkonnad


def loo_võistluspaarid(berger, võistkonnad):
    """
        Moodustab võistkondade paarid Bergeri süsteemi alusel.
        
        Args:
            berger (list[tuple(int, int)]): Arvupaaride järjend, kus igas paaris on
                on indeksid + 1 võistkondade nimede järjendis.
            võistkonnad (list[str]): Võistkondade nimed.
            
        Returns:
            list[tuple(str, str)]
                list(Paar (str, str)): Võistkondade nimede paarid, kes
                    omavahel võistlevad
            
    """
    
    # kontrolli, kas mängude arv bergeri süsteemis klapib võistkondade 
    n_võistkonnad = len(võistkonnad)
    Cn_võistkonnad = n_võistkonnad * (n_võistkonnad - 1) // 2    
    if Cn_võistkonnad != len(berger):
        print(f'Võistkondade arv ei klapi Bergeri süsteemiga! berger {len(berger)}, võistkonnad {Cn_võistkonnad}')
        return -1
    
    # moodusta võistlustabel
    võistluspaarid = []
    for (a, b) in berger:
        try:
            paar = (võistkonnad[a - 1], võistkonnad[b - 1])
        except IndexError:
            raise ValueError(f'Vigased indeksid {a} ja {b}')
        
        võistluspaarid.append(paar)
    
    return võistluspaarid


def jaga_väljakutele(võistluspaarid, väljakute_arv):
    """
        Paaritud võistluspaarid esimesele väljakule ja paaris teisele väljakule.
        
        Args:
        
        Returns:
    # võtab: [paar1, paar2, paar3, ...]
    # teeb: [[paar1, paar2], [paar3, paar4], ...]

    # kui paaritu arv mänge, lisa viimane tühja paariga
    """
    if len(võistluspaarid) % 2:
        võistluspaarid.append(('', ''))
    
    väljakud = []
    if väljakute_arv == 1:
        väljakud = list(zip(võistluspaarid))
    elif väljakute_arv == 2:
        paaris = [võistluspaarid[i] for i in range (0, len(võistluspaarid), 2)]
        paaritud = [võistluspaarid[i] for i in range (1, len(võistluspaarid), 2)]
        väljakud = list(zip(paaris, paaritud))

    pprint(väljakud)
    return väljakud



def loo_võistlustabelid_järjend(võistluspaarid, algusajad, mängu_kestus=timedelta(hours=1, minutes=15)):
    """
        Moodustab võistlustabeli koos päisega
        võistlustabel = [
                            ['Jrk', '1. päev', 'KOHTUNIKUD', 'AEG'],
                            [1, 'võistkond A - võistkond B', 'Peeter', '11:00'],
                            [2, 'võistkond C - võistkond D', 'Pärtel', '12:00'],
                            [3, 'võistkond E - võistkond F', 'Kaarel', '13:00'],
                            ....
        ]
        võistlustabelid = [
                            võistlustabel,
                            võistlustabel,
                            võistlustabel,
        ]
    """
    def algusaeg(algusaeg_str):
        # loob aja objekti
        return datetime.strptime(algusaeg_str, "%H:%M")
    
    def aegstr(t):
        # loob aja stringi vormis HH:MM
        return f'{t.hour:02d}:{t.minute:02d}'
      
      
    for i, aeg in enumerate(algusajad):
        algusajad[i] = algusaeg(aeg)
        
    päevad  = []
    if len(algusajad) == 2:
        päevad.append(võistluspaarid[:len(võistluspaarid) // 2])
        päevad.append(võistluspaarid[len(võistluspaarid) // 2:])
    else:
        päevad = [võistluspaarid]

    võistlustabelid = []
    for pi, päev in enumerate(päevad, start=1):
        print('päevad')
        pprint(päev)
        for vi, väljak in enumerate(zip(*päev), start=1):
            print('väljak')
            pprint(väljak)
            võistlustabel = [['Jrk', f'{pi}. päev/{vi}. väljak', 'KOHTUNIKUD', 'AEG']]
            t = algusajad[pi - 1]        
            for i, (a, b) in enumerate(väljak, start=1):
                võistlustabel.append([i, f'{a} - {b}', '', f'{aegstr(t)}'])
                t = t + mängu_kestus
            võistlustabelid.append(võistlustabel)
            
    return võistlustabelid

# --------------------------------
# GUI
# --------------------------------

def loo_gui(võistluse_tüübid, mängu_kestused):

    def tsooni_str(tsooni_nr):
        linn, võistkonnad = loe_tsoon(tsoonifail, tsooni_nr)        
        return '\n'.join(võistkonnad)
    
    def on_spin():
        tsooni_nr = int(tsoon_spin.get())
        sisestus_box.delete("1.0", "end")
        sisestus_box.insert('1.0', tsooni_str(tsooni_nr))
    
    def on_click():
        nonlocal võistkonnad_käsitsi
        if allikas_var.get() == 'tsoon':
            võistkonnad_käsitsi = sisestus_box.get("1.0", tk.END).strip()
            tsoon_spin.config(state='normal')
            on_spin()
        elif allikas_var.get() == 'käsitsi':
            tsoon_spin.config(state='disabled')
            sisestus_box.delete("1.0", "end")
            sisestus_box.insert('1.0', võistkonnad_käsitsi)
    
    võistkonnad_käsitsi = ''
    võistlustabelid = []
    root = tk.Tk()
    root.title("Võrkpalli võistluse ajakava")
    root.configure(bg="#2e2e2e")
    style = ttk.Style()
    style.theme_use('clam')   
    style.configure("TLabel", background="#2e2e2e", foreground="#f0f0f0")
    style.configure("TFrame", background="#2e2e2e", foreground="#f0f0f0")
    style.configure("TButton", background="#3a3a3a", foreground="#f0f0f0")
    style.configure("TRadiobutton", background="#2e2e2e", foreground="#f0f0f0")
    style.configure("TRadiobutton", background="#2e2e2e", foreground="#f0f0f0")


    style.configure(
        "Flat.TEntry",
        relief = "flat",
        borderwidth=0,
        fieldbackground="#3a3a3a",
        foreground="#f0f0f0",
        background="#3a3a3a",
        insertbackground="#f0f0f0")
    style.configure("Flat.TCombobox",
        relief="flat",
        fieldbackground="#3a3a3a",
        background="#5a5a5a",
        foreground="#f0f0f0",
        arrowcolor="#f0f0f0")
    style.configure(
        "Flat.TSpinbox",
        relief="flat",
        borderwidth=0,
        padding=1,
        fieldbackground="#3a3a3a",
        background="#5a5a5a",
        foreground="#f0f0f0",
        arrowsize=15
    )
    
    style.map("TButton",
          background=[('active', '#505050')],
          foreground=[('active', '#ffffff')])
    style.map("TRadiobutton",
          background=[('active', '#3a3a3a')],
          foreground=[('active', '#ffffff')])
    style.map("Flat.TCombobox",
              fieldbackground=[('readonly', '#3a3a3a')],
              background=[('active', '#505050')],
              foreground=[('disabled', '#888')],
              arrowcolor=[('active', '#ffffff')])
    style.map(
        "Flat.TSpinbox",
        arrowcolor=[('active', 'green'), ('!active', 'lightgreen')]
    )
    # --- ALLIKAVALIK: tsoonist vs käsitsi ---
    allikas_var = tk.StringVar(value="tsoon")

    ttk.Label(root, text="Võistkondade allikas:").grid(
        row=0, column=0, sticky="w", padx=5, pady=5
    )
    
    tsoon_frame = ttk.Frame(root)
    tsoon_frame.grid(row=0, column=1, padx=0, pady=5, sticky="we")
    ttk.Radiobutton(tsoon_frame, text="Loe tsoonifailist", variable=allikas_var, value="tsoon", command=on_click).grid(
        row=0, column=0, sticky="w")
    ttk.Radiobutton(tsoon_frame, text="Sisesta käsitsi", variable=allikas_var, value="käsitsi", command=on_click).grid(
        row=0, column=1, sticky="w")

    # tsooni number
    ttk.Label(root, text="Tsooni number (1–10):").grid(
        row=1, column=0, sticky="w", padx=5, pady=5
    )
    tsoon_spin = ttk.Spinbox(root, from_=1, to=10, style="Flat.TSpinbox", width=5, command=on_spin)
    tsoon_spin.grid(row=1, column=1, sticky="w")
    tsoon_spin.set(1)

    # käsitsi võistkondade sisestus
    ttk.Label(root, text="Võistkonnad (üks rida = üks võistkond):").grid(
        row=2, column=0, columnspan=3, sticky="w", padx=5, pady=5
    )
    sisestus_box = tk.Text(root,
                           height=6,
                           bg="#3a3a3a",
                           fg="#f0f0f0",
                           insertbackground="#f0f0f0",
                           selectbackground="#505050",
                           selectforeground="#ffffff",
                           relief="flat",
                           borderwidth=0,
                           highlightthickness=0,
                           width=50)
    sisestus_box.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

    # Tkinteri muutujad
    vanuse_var = tk.StringVar(value="U16")
    kuupäev_var = tk.StringVar(value="2025-12-15")
    tüüp_var = tk.StringVar(value="ühepäevane ühel väljakul")
    algus1_var = tk.StringVar(value="10:00")
    algus2_var = tk.StringVar(value="10:00")
    kodu_var = tk.StringVar(value="")  # koduvõistkonna nimi (vaba tekst)

    # vanuseklass
    ttk.Label(root, text="Vanuseklass:").grid(row=4, column=0, sticky="w", padx=5, pady=5)
    vanuseklass_frame = ttk.Frame(root)
    vanuseklass_frame.grid(row=4, column=1, padx=0, pady=5, sticky="we")
    
    ttk.Radiobutton(vanuseklass_frame, text="U16", variable=vanuse_var, value="U16").grid(row=0, column=0, padx=5, pady=5)
    ttk.Radiobutton(vanuseklass_frame, text="U18", variable=vanuse_var, value="U18").grid(row=0, column=1, padx=5, pady=5)
    ttk.Radiobutton(vanuseklass_frame, text="U20", variable=vanuse_var, value="U20").grid(row=0, column=2, padx=5, pady=5)
    
    # kuupäev
    ttk.Label(root, text="Võistluse kuupäev (YYYY-MM-DD):").grid(
        row=5, column=0, sticky="w", padx=5, pady=5
    )
    ttk.Entry(root, textvariable=kuupäev_var, style="Flat.TEntry", width=15).grid(row=5, column=1, sticky="WE")

    # võistluse tüüp
    ttk.Label(root, text="Võistluse tüüp:").grid(row=6, column=0, sticky="WE", padx=5, pady=5)
    tüüp_combo = ttk.Combobox(
        root,
        textvariable=tüüp_var,
        values = list(võistluse_tüübid.keys()),
        state="readonly",
        style="Flat.TCombobox",
        width=32
    )
    tüüp_combo.grid(row=6, column=1, sticky="w")

    # algusaeg I päeval
    ttk.Label(root, text="Algusaeg I päeval (HH:MM):").grid(
        row=7, column=0, sticky="w", padx=5, pady=5
    )
    ttk.Entry(root, textvariable=algus1_var, style="Flat.TEntry", width=8).grid(row=7, column=1, sticky="WE")

    # algusaeg II päeval
    ttk.Label(root, text="Algusaeg II päeval (HH:MM):").grid(
        row=8, column=0, sticky="w", padx=5, pady=5
    )
    ttk.Entry(root, textvariable=algus2_var, style="Flat.TEntry", width=8).grid(row=8, column=1, sticky="WE")

    # koduvõistkonna nimi
    ttk.Label(root, text="Koduvõistkonna nimi:").grid(
        row=9, column=0, sticky="w", padx=5, pady=5
    )
    ttk.Entry(root, textvariable=kodu_var, style="Flat.TEntry", width=30).grid(row=9, column=1, sticky="WE")

    # täida teksti_kast failist loetud infoga
    # v]iks eraldada eraldi abifunktsiooni
    allikas = allikas_var.get()
    if allikas == "tsoon":
        try:
            tsooni_nr = int(tsoon_spin.get())
        except ValueError:
            raise ValueError("Tsooni number peab olema täisarv 1–10.")
        linn, võistkonnad = loe_tsoon(tsoonifail, tsooni_nr)
        sisestus_box.insert('1.0', '\n'.join(võistkonnad))
        
    def nupp_genereeri():
        nonlocal võistlustabelid
        
        allikas = allikas_var.get()
        vanuseklass=vanuse_var.get()
        kuupäev=kuupäev_var.get()
        võistluse_tüüp=tüüp_var.get()
        algus1=algus1_var.get()
        algus2=algus2_var.get()
        koduvõistkond=kodu_var.get()
        tsooni_nr = int(tsoon_spin.get())
        
        # loe võistkonnad tsoonifailist
        if allikas == "tsoon":
            linn, võistkonnad = loe_tsoon(tsoonifail, tsooni_nr)

        # loe võistkonnad tekstikastist
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
         
        if not koduvõistkond or koduvõistkond not in võistkonnad:
            return messagebox.showinfo("!", "Koduvõistkonda ei leitud!")
            
 
        berger_str = f'{len(võistkonnad)}_{võistluse_tüübid[võistluse_tüüp]}' 
        võistkonnad = liiguta_koduvõistkond(võistkonnad, koduvõistkond, 5)
        print(berger_str)


        # võistluspaaride moodustamine
        try:
            võistluspaarid = loo_võistluspaarid(berger[berger_str], võistkonnad)
        except Exception as e:
            raise ValueError(f"Tsooni → turniiri teisendus ebaõnnestus: {e}")

        # kahe väljaku võistluse puhul jagatakse võistluspaarid kahele väljakule
        # kahe päeva korral antakse kaks algusaega
        if võistluse_tüübid[võistluse_tüüp] == '1p1v' :
            algusajad = [algus1]
            võistluspaarid = jaga_väljakutele(võistluspaarid, 1)
        elif võistluse_tüübid[võistluse_tüüp] == '1p2v' :
            algusajad = [algus1]
            võistluspaarid = jaga_väljakutele(võistluspaarid, 2)
        elif võistluse_tüübid[võistluse_tüüp] == '2p1v':
            algusajad = [algus1, algus2]
            võistluspaarid = jaga_väljakutele(võistluspaarid, 1)
        elif võistluse_tüübid[võistluse_tüüp] == '2p2v':
            algusajad = [algus1, algus2]
            võistluspaarid = jaga_väljakutele(võistluspaarid, 2)
    
        # võistlustabelite loomine
        võistlustabelid = loo_võistlustabelid_järjend(võistluspaarid, algusajad, mängu_kestused[vanuseklass])
        loo_pdf('võistlustabelid.pdf', võistlustabelid)
    
    def kopeeri_lõikelauale():
        nonlocal võistlustabelid
        
        output = io.StringIO()
        writer = csv.writer(output, delimiter='\t', lineterminator='\n', quoting=csv.QUOTE_MINIMAL)

        for tabel in võistlustabelid:
            for rida in tabel:
                writer.writerow(rida)
        csv_string = output.getvalue()
        output.close()
        
        root.clipboard_clear()
        root.clipboard_append(csv_string)
        root.update()  # now it’s in clipboard
        
    
    ttk.Button(root, text="Genereeri ajakava PDF", command=nupp_genereeri).grid(
        row=10, column=0, pady=10, sticky="WE")
    ttk.Button(root, text="Kopeeri lõikelauale", command=kopeeri_lõikelauale).grid(
        row=10, column=1, pady=10, sticky="WE")

    root.mainloop()

def loo_pdf(failinimi, võistlustabelid):
    # Create a PDF
    pdf = SimpleDocTemplate(failinimi, pagesize=A4)

    pdftabelid = []
    for i, vtabel in enumerate(võistlustabelid):
        pdftabel = Table(vtabel, colWidths=[30, 275, 200, 50], rowHeights=[60] * len(vtabel))
        pdftabel.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
            ("FONT", (0, 0), (-1, -1), "Helvetica"),
        ]))
        pdftabelid.append(pdftabel)
        if i != len(võistlustabelid) - 1:
            pdftabelid.append(PageBreak())

    for t in pdftabelid:
        pdf.build(pdftabelid)


# --------------------------------
# PROGRAMMI KÄIVITAMINE
# --------------------------------

if __name__ == "__main__":
    
    # fumktsioonide jaoks vajalikud parameetrid
    tsoonifail = 'voistkonnad.txt'
    tsooni_nr = 1
    koduvõistkonna_nr = 5  # mitmendaks nihutatakse koduvõistkond (nt 5. positsioonile)

    võistluse_tüübid  = {
            'ühepäevane ühel väljakul' : '1p1v',
            'ühepäevane kahel väljakul' : '1p2v',
            'kahepäevane ühel väljakul' : '2p1v',
            'kahepäevane kahel väljakul' : '2p2v',
    }
    
    # kui on üks aeg, siis ühepäevane võistlus, kui kaks siis kahepäevane
    algusajad = ['15:00', '10:00'] 
    
    mängu_kestused = {
            'U16' : timedelta(hours=1, minutes=15),
            'U18' : timedelta(hours=2),
            'U20' : timedelta(hours=2),            
    }
    
    """
    # funktsioonide testid
    linn, võistkonnad = loe_tsoon(tsoonifail, tsooni_nr)
    print('Loen', tsoonifail, f'tsooni_nr: {tsooni_nr}')
    print(linn)
    pprint(võistkonnad)
    
    print()
    print(f'Liigutan koduvõistkonna positsioonile {koduvõistkonna_nr}')
    liiguta_koduvõistkond(võistkonnad, 'Narva SK Energia/SK Galla I', koduvõistkonna_nr)
    pprint(võistkonnad)
    
    print()
    print('Loon võistluspaarid')
    #võistluspaarid = loo_võistluspaarid(berger['6_2p1v'], võistkonnad)
    võistluspaarid = loo_võistluspaarid(berger['6_2p2v'], võistkonnad)
    pprint(võistluspaarid)
    print(f'len: {len(võistluspaarid)}')
    
    print()
    print(f'Jagan võistluspaarid kahele väljakule')
    #pprint(võistluspaarid[:len(võistluspaarid) // 2])
    #pprint(võistluspaarid[len(võistluspaarid) // 2 :])
    
    võistluspaarid = jaga_väljakutele(võistluspaarid, 2)
    pprint(võistluspaarid)
    print(f'Mängude arv {len(võistluspaarid)}')
    
    print()
    print('Loon võistlustabelid ja kirjutan pdf faili')
    võistlustabelid = loo_võistlustabelid_järjend(võistluspaarid, algusajad)
    loo_pdf('võistlustabelid.pdf', võistlustabelid)
    """
    
    loo_gui(võistluse_tüübid, mängu_kestused)
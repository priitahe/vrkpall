# -*- coding: utf-8 -*-
"""
Võrkpalli ajakava generaator — Berger-järjekord säilitatud, backtracking paigutaja
(Toetab 5 või 6 võistkonda; 1/2 väljakut; 1/2 päeva)
"""
from pprint import pprint
from datetime import datetime, timedelta
import tkinter as tk
from tkinter import ttk, messagebox
import random
import os
from collections import defaultdict
import math

# ------------- Põhiseaded -------------
tsoonifail = 'voistkonnad.txt'
kodu_võistkonna_nr = 5  # 1-põhine sihtpositsioon kodule

# globaalsed (eksport)
viimane_ajakava = None
viimased_võistkonnad = None
viimane_meta = None

# ------------- Bergeri tabelid (indexid 1-based) -------------
berger_5_2p1v = [
    (2, 5), (3, 4), (1, 2), (5, 3),
    (1, 4), (2, 3), (4, 5), (3, 1),
    (4, 2), (5, 1)
]

berger_6_2p1v = [
    (2, 5), (3, 4), (1, 6), (5, 3),
    (1, 2), (6, 4), (3, 1), (4, 5),
    (2, 6), (1, 4), (2, 3), (6, 5),
    (4, 2), (3, 6), (5, 1)
]

# ------------- Failist lugemine -------------
def loe_tsoon(tsoonifail, tsooni_nr):
    with open(tsoonifail, encoding='utf8') as f:
        on_valitud = False
        võistkonnad = []
        tsooni_linn = ''
        for rida in f:
            rida = rida.strip()
            if not rida:
                continue
            if rida.startswith('#'):
                osa = rida.removeprefix('#').split(',')
                if len(osa) == 2:
                    try:
                        nr = int(osa[0])
                    except Exception:
                        on_valitud = False
                        continue
                    linn = osa[1].strip()
                else:
                    on_valitud = False
                    continue
                if nr == tsooni_nr:
                    on_valitud = True
                    tsooni_linn = linn
                else:
                    on_valitud = False
            elif on_valitud:
                puh = rida.lstrip("0123456789. )").strip()
                if puh:
                    võistkonnad.append(puh)
        if not võistkonnad:
            raise ValueError(f"Tsooni {tsooni_nr} ei leitud või seal pole võistkondi.")
        return tsooni_linn, võistkonnad

# ------------- Tsoon → turniir -------------
def teisenda_tsoonist_turniiriks(võistkonnad):
    n = len(võistkonnad)
    if n == 6:
        kaardistus = {1:5, 2:1, 3:2, 4:3, 5:4, 6:6}
    elif n == 5:
        kaardistus = {1:5, 2:1, 3:2, 4:3, 5:4}
    else:
        raise ValueError("Toetatud ainult 5 või 6 võistkonda teisendamiseks.")
    uus = [None] * n
    for tsoon_pos in range(1, n+1):
        siht = kaardistus[tsoon_pos]
        uus[siht - 1] = võistkonnad[tsoon_pos - 1]
    if any(x is None for x in uus):
        raise RuntimeError("Teisenduse viga — mõni koht jäi täitmata.")
    return uus

# ------------- Nihuta kodu -------------
def nihuta_koduvõistkond(võistkonnad, kodu_nimi, siht_pos):
    try:
        i = võistkonnad.index(kodu_nimi)
    except ValueError:
        raise ValueError(f'Koduvõistkond "{kodu_nimi}" ei leitud nimekirjast.')
    siht_idx = siht_pos - 1
    võistkonnad[i], võistkonnad[siht_idx] = võistkonnad[siht_idx], võistkonnad[i]
    return võistkonnad

# ------------- Bergeri indeksid → nimed -------------
def loo_võistluspaarid(berger, võistkonnad):
    n = len(võistkonnad)
    kokku_mänge = n * (n - 1) // 2
    if kokku_mänge != len(berger):
        print(f'Võistkondade arv ei klapi Bergeri süsteemiga! berger {len(berger)}, vajalik {kokku_mänge}')
        return -1
    tabel = []
    for (a, b) in berger:
        try:
            paar = (võistkonnad[a - 1], võistkonnad[b - 1])
        except IndexError:
            raise ValueError(f'Vigased indeksid Bergeri tabelis: {a}, {b}')
        tabel.append(paar)
    return tabel

# ------------- Kuvamine -------------
def kuva_võistlustabel(võistluspaarid, algusaeg1, kakspäeva=True, algusaeg2=None, mängu_kestus=timedelta(hours=1, minutes=15)):
    def aegstr(dt):
        return f'{dt.hour:02d}:{dt.minute:02d}'
    if algusaeg2 is None:
        algusaeg2 = algusaeg1
    print('1. päev')
    t = algusaeg1
    for i, slot in enumerate(võistluspaarid):
        if kakspäeva and i == len(võistluspaarid) // 2:
            print('2. päev')
            t = algusaeg2
        print(f'Mäng nr {i + 1}')
        if isinstance(slot, tuple) and len(slot) == 2:
            a, b = slot
            print(f'{aegstr(t)}, {i + 1}. {a} - {b}')
        elif isinstance(slot, list) and len(slot) == 2:
            (a, b), (c, d) = slot
            print('1. väljak')
            print(f'{aegstr(t)}, {i + 1}. {a} - {b}')
            print('2. väljak')
            print(f'{aegstr(t)}, {i + 1}. {c} - {d}')
        else:
            raise ValueError(f'Vigane slot struktuur: {slot}')
        t = t + mängu_kestus

# ------------- Kontroll järjestikuste mängude kohta -------------
def kontrolli_järjestikuseid(võistluspaarid, kahepäevane):
    tiimi_mängud = defaultdict(list)
    for i, slot in enumerate(võistluspaarid, start=1):
        if isinstance(slot, tuple):
            a, b = slot
            tiimi_mängud[a].append(i)
            tiimi_mängud[b].append(i)
        elif isinstance(slot, list):
            for (x, y) in slot:
                tiimi_mängud[x].append(i)
                tiimi_mängud[y].append(i)
    rikk = {}
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
                        rikk[t] = f"rohkem kui 2 järjest ({nimi})"
                        break
                else:
                    järjest = 1
    return rikk

# ------------- Lihtne jagaja -------------
def jaga_kaheks_väljakuks_lihtne(võistluspaarid):
    tulemus = []
    töötav = []
    for paar in võistluspaarid:
        töötav.append(paar)
        if len(töötav) == 2:
            tulemus.append(töötav)
            töötav = []
    if töötav:
        töötav.append(('', ''))
        tulemus.append(töötav)
    return tulemus

# ------------- Koduvõistkond 1. väljakul -------------
def sea_kodumeeskond_esimeseks(tabel, kodu_nimi):
    uus = []
    for slot in tabel:
        if isinstance(slot, tuple):
            uus.append(slot)
        elif isinstance(slot, list) and len(slot) == 2:
            m1, m2 = slot
            if (kodu_nimi in m2) and (kodu_nimi not in m1):
                uus.append([m2, m1])
            else:
                uus.append(slot)
        else:
            uus.append(slot)
    return uus

# ------------- Backtracking paigutaja (BERGER järjekord säilib) -------------
def jaga_kaheks_väljakuks_piiranguga(võistluspaarid, max_järjest=2, kahepäevane=False, max_katsed=200000):
    """
    Paigutab matšid slotidesse, hoides matšide algjärjekorda (järjestikku Bergeri listi).
    Tagab max_järjest päevas ja üksikud slotid ainult päeva lõpus (kaheväljakul+kahepäevane).
    """
    M = len(võistluspaarid)
    total_slots = math.ceil(M / 2)
    if kahepäevane:
        day1_slots = total_slots // 2
        day2_slots = total_slots - day1_slots
    else:
        day1_slots = total_slots
        day2_slots = 0

    # Matšid täpselt samas järjekorras kui võistluspaarid
    matches = list(võistluspaarid)

    slots = [[] for _ in range(total_slots)]
    team_slots = defaultdict(list)
    N = len(matches)
    used = [False] * N
    attempts = 0

    # abifunktsioonid
    def max_run_in_range(team, slots_local, start, end):
        run = 0
        maxrun = 0
        for idx in range(start, end):
            if any(team in m for m in slots_local[idx]):
                run += 1
                if run > maxrun:
                    maxrun = run
            else:
                run = 0
        return maxrun

    def check_team_ok(team, slots_local):
        if kahepäevane:
            return max_run_in_range(team, slots_local, 0, day1_slots) <= max_järjest and max_run_in_range(team, slots_local, day1_slots, total_slots) <= max_järjest
        else:
            return max_run_in_range(team, slots_local, 0, total_slots) <= max_järjest

    def singles_only_at_day_end(slots_local):
        def day_ok(start, end):
            seen_one = False
            for s in range(start, end):
                if len(slots_local[s]) == 2:
                    if seen_one:
                        return False
                elif len(slots_local[s]) == 1:
                    seen_one = True
                elif len(slots_local[s]) == 0:
                    seen_one = True
            return True
        if kahepäevane:
            return day_ok(0, day1_slots) and day_ok(day1_slots, total_slots)
        else:
            return day_ok(0, total_slots)

    # backtracking
    def place(next_match_idx):
        nonlocal attempts
        attempts += 1
        # kui kõik paigutatud
        if next_match_idx == N:
            if all(check_team_ok(team, slots) for team_pair in matches for team in team_pair) and singles_only_at_day_end(slots):
                # teisenda välja (tuple või list)
                out = []
                for s in slots:
                    if len(s) == 1:
                        out.append(s[0])
                    elif len(s) == 2:
                        out.append(list(s))
                    else:
                        # tühjad slotid (pole tavaks) ignoreeri
                        pass
                return out
            return None

        a, b = matches[next_match_idx]

        # katsetame slot'id järjekorras — kuid mitte edasi hüpates (enne peab olema täidetud)
        for s_idx in range(total_slots):
            # enne s_idx peab kõik varasemad slotid olema vähemalt mitte-olevalt tühi? Me lubame täita järjestikku:
            # ära pane matši slot'i, kui vasemal on täiesti tühi slot (see jätab skip'i)
            if any(len(slots[x]) == 0 for x in range(0, s_idx)):
                continue

            if len(slots[s_idx]) >= 2:
                continue
            if any(a in m or b in m for m in slots[s_idx]):
                continue

            # pane prooviselt
            slots[s_idx].append((a, b))
            team_slots[a].append(s_idx)
            team_slots[b].append(s_idx)

            # prune: kontrolleeri ainult a ja b (kiire), mitte kõiki tiime
            if not (check_team_ok(a, slots) and check_team_ok(b, slots)):
                # undo
                team_slots[a].pop(); team_slots[b].pop()
                slots[s_idx].pop()
                continue

            res = place(next_match_idx + 1)
            if res is not None:
                return res

            # undo
            team_slots[a].pop(); team_slots[b].pop()
            slots[s_idx].pop()

        # ei leidnud kohta -> backtrack
        return None

    solution = place(0)
    if solution is None:
        # kui ei leia, tagasta lihtne jagaja (GUI kuvab hoiatused)
        return jaga_kaheks_väljakuks_lihtne(võistluspaarid)
    return solution

# ------------- Kui eelviimane on üksik ja viimane topelt -------------
def tõsta_üksik_viimaseks(tabel):
    if not isinstance(tabel, list) or len(tabel) < 2:
        return tabel
    eel = tabel[-2]; viimane = tabel[-1]
    if isinstance(eel, tuple) and isinstance(viimane, list):
        tabel[-2], tabel[-1] = tabel[-1], tabel[-2]
    return tabel

# ------------- Valikud -------------
def vali_berger_ja_seaded(võistkondade_arv, tüüp):
    if võistkondade_arv == 5:
        berger = berger_5_2p1v
    elif võistkondade_arv == 6:
        berger = berger_6_2p1v
    else:
        raise ValueError("Toetatud vaid 5 või 6 võistkonda.")
    kahel_väljakul = "kahel väljakul" in tüüp
    kahepäevane = "kahepäevane" in tüüp
    väljakuid = 2 if kahel_väljakul else 1
    return berger, väljakuid, kahepäevane

# ------------- Tabel -> listiks (eksport) -------------
def tee_ajakava_listiks(tabel, algus1_dt, kahepäevane=True, algus2_dt=None, mängu_kestus=timedelta(hours=1, minutes=15)):
    if algus2_dt is None:
        algus2_dt = algus1_dt
    kokku = len(tabel)
    tulem = []
    for i, slot in enumerate(tabel):
        if kahepäevane:
            pool = kokku // 2
            if i < pool:
                päev = 1
                idx_päevas = i
                t = algus1_dt + idx_päevas * mängu_kestus
            else:
                päev = 2
                idx_päevas = i - pool
                t = algus2_dt + idx_päevas * mängu_kestus
        else:
            päev = 1
            idx_päevas = i
            t = algus1_dt + idx_päevas * mängu_kestus
        def aegstr(dt):
            return f'{dt.hour:02d}:{dt.minute:02d}'
        if isinstance(slot, tuple):
            a, b = slot
            tulem.append({'päev': päev, 'aeg': aegstr(t), 'mäng_nr': i+1, 'väljak': 1, 'kodumeeskond': a, 'võõrameeskond': b})
        elif isinstance(slot, list) and len(slot) == 2:
            (a, b), (c, d) = slot
            tulem.append({'päev': päev, 'aeg': aegstr(t), 'mäng_nr': i+1, 'väljak': 1, 'kodumeeskond': a, 'võõrameeskond': b})
            tulem.append({'päev': päev, 'aeg': aegstr(t), 'mäng_nr': i+1, 'väljak': 2, 'kodumeeskond': c, 'võõrameeskond': d})
        else:
            raise ValueError(f'Vigane slot struktuur: {slot}')
    return tulem

# ------------- Eksport -------------
def eksporti_excelisse(path="ajakava_tksheet.xlsx"):
    global viimane_ajakava, viimased_võistkonnad, viimane_meta
    if viimane_ajakava is None or viimased_võistkonnad is None or viimane_meta is None:
        raise RuntimeError("Puudu: genereeri esmalt ajakava (vajuta 'Genereeri ajakava').")
    try:
        import pandas as pd
    except Exception:
        teams_csv = "voistkonnad.csv"
        schedule_csv = "ajakava.csv"
        with open(teams_csv, "w", encoding="utf8") as f:
            f.write("positsioon;võistkond\n")
            for i, t in enumerate(viimased_võistkonnad, start=1):
                f.write(f"{i};{t}\n")
        with open(schedule_csv, "w", encoding="utf8") as f:
            f.write("päev;aeg;mäng_nr;väljak;kodumeeskond;võõrameeskond\n")
            for r in viimane_ajakava:
                f.write(f"{r['päev']};{r['aeg']};{r['mäng_nr']};{r['väljak']};{r['kodumeeskond']};{r['võõrameeskond']}\n")
        return os.path.abspath(teams_csv), os.path.abspath(schedule_csv)
    df_voist = pd.DataFrame({'Positsioon': list(range(1, len(viimased_võistkonnad) + 1)), 'Võistkond': viimased_võistkonnad})
    df_ajak = pd.DataFrame(viimane_ajakava)
    df_ajak['Päev'] = df_ajak['päev'].map({1: 'I päev', 2: 'II päev'})
    df_ajak = df_ajak[['Päev', 'aeg', 'mäng_nr', 'väljak', 'kodumeeskond', 'võõrameeskond']]
    df_ajak.columns = ['Päev', 'Aeg', 'Mäng nr', 'Väljak', 'Kodu', 'Võõras']
    meta_rows = [("Kuupäev", viimane_meta.get('kuupäev', '')), ("Vanuseklass", viimane_meta.get('vanuseklass', '')), ("Võistluse tüüp", viimane_meta.get('tüüp', '')), ("Asukoht", viimane_meta.get('asukoht', ''))]
    try:
        writer = pd.ExcelWriter(path, engine='openpyxl')
        df_voist.to_excel(writer, sheet_name='Võistkonnad', index=False)
        df_ajak.to_excel(writer, sheet_name='Ajakava', index=False)
        df_meta = pd.DataFrame(meta_rows, columns=['Väli', 'Väärtus'])
        df_meta.to_excel(writer, sheet_name='Meta', index=False)
        writer.save()
        return os.path.abspath(path)
    except Exception as e:
        raise RuntimeError(f"Excelisse kirjutamine ebaõnnestus: {e}")

# ------------- Peamine genereerimine -------------
def genereeri_ajakava_gui(vanuseklass, kuupäev, võistluse_tüüp, algus1, algus2, võistkonnad, kodu_võistkond_nimi, asukoht="", värvid=None):
    if len(võistkonnad) not in (5, 6):
        raise ValueError("Toetatud vaid 5 või 6 võistkonda.")
    try:
        algus1_dt = datetime.strptime(f"{kuupäev} {algus1}", "%Y-%m-%d %H:%M")
    except Exception:
        raise ValueError("I päeva algusaja või kuupäeva formaat on vale (YYYY-MM-DD ja HH:MM).")
    try:
        algus2_dt = datetime.strptime(f"{kuupäev} {algus2}", "%Y-%m-%d %H:%M")
    except Exception:
        algus2_dt = None
    mängu_kestus = timedelta(hours=1, minutes=15) if vanuseklass == "U16" else timedelta(hours=2)
    töö_võistkonnad = võistkonnad[:]
    if kodu_võistkond_nimi.strip():
        if kodu_võistkond_nimi.strip() not in töö_võistkonnad:
            raise ValueError("Koduvõistkond peab olema võistkondade nimekirjas.")
        nihuta_koduvõistkond(töö_võistkonnad, kodu_võistkond_nimi.strip(), kodu_võistkonna_nr)
    berger, väljakuid, kahepäevane = vali_berger_ja_seaded(len(töö_võistkonnad), võistluse_tüüp)
    võistluspaarid = loo_võistluspaarid(berger, töö_võistkonnad)
    if võistluspaarid == -1:
        raise ValueError("Bergeri tabel ei sobinud võistkondade arvuga.")
    if väljakuid == 2:
        tabel = jaga_kaheks_väljakuks_piiranguga(võistluspaarid, max_järjest=2, kahepäevane=kahepäevane)
    else:
        tabel = võistluspaarid
    tabel = tõsta_üksik_viimaseks(tabel)
    if väljakuid == 2 and kodu_võistkond_nimi.strip():
        tabel = sea_kodumeeskond_esimeseks(tabel, kodu_võistkond_nimi.strip())
    print()
    print("==========================================")
    if asukoht:
        print(f"Asukoht: {asukoht}")
    print(f"Kuupäev: {kuupäev}, vanuseklass: {vanuseklass}")
    print(f"Võistluse tüüp: {võistluse_tüüp}")
    print("Osalevad võistkonnad:")
    for v in töö_võistkonnad:
        print(" -", v)
    print("==========================================")
    if kahepäevane and algus2_dt is not None:
        kuva_võistlustabel(tabel, algus1_dt, kakspäeva=True, algusaeg2=algus2_dt, mängu_kestus=mängu_kestus)
    else:
        kuva_võistlustabel(tabel, algus1_dt, kakspäeva=False, algusaeg2=None, mängu_kestus=mängu_kestus)
    rikk = kontrolli_järjestikuseid(tabel, kahepäevane)
    if rikk:
        print("\n⚠️  Järjestikuste mängude piirangu rikkumised:")
        for t, p in rikk.items():
            print(f" - {t}: {p}")
    else:
        print("\n✅ Kõik võistkonnad vastavad järjestikuse mängu piirangule!")
    return tabel, mängu_kestus, kahepäevane, algus1_dt, (algus2_dt if algus2_dt is not None else algus1_dt)

# ------------- GUI -------------
def loo_gui():
    global viimane_ajakava, viimased_võistkonnad, viimane_meta
    root = tk.Tk()
    root.title("Võrkpalli ajakava generaator")

    allikas_var = tk.StringVar(value="tsoon")
    ttk.Label(root, text="Võistkondade allikas:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
    ttk.Radiobutton(root, text="Loe tsoonifailist", variable=allikas_var, value="tsoon").grid(row=0, column=1, sticky="w")
    ttk.Radiobutton(root, text="Sisesta käsitsi", variable=allikas_var, value="käsitsi").grid(row=0, column=2, sticky="w")

    ttk.Label(root, text="Tsooni number (1–10):").grid(row=1, column=0, sticky="w", padx=5, pady=5)
    tsoon_spin = tk.Spinbox(root, from_=1, to=10, width=6)
    tsoon_spin.grid(row=1, column=1, sticky="w")

    ttk.Label(root, text="Võistkonnad (üks rida = üks võistkond):").grid(row=2, column=0, columnspan=3, sticky="w", padx=5, pady=5)
    sisestus_box = tk.Text(root, height=8, width=50)
    sisestus_box.grid(row=3, column=0, columnspan=3, padx=5, pady=5)

    vanuse_var = tk.StringVar(value="U16")
    kuupäev_var = tk.StringVar(value="2025-12-15")
    tüüp_var = tk.StringVar(value="kahepäevane kahel väljakul")
    algus1_var = tk.StringVar(value="10:00")
    algus2_var = tk.StringVar(value="10:00")
    kodu_var = tk.StringVar(value="")

    ttk.Label(root, text="Vanuseklass:").grid(row=4, column=0, sticky="w", padx=5, pady=5)
    ttk.Radiobutton(root, text="U16", variable=vanuse_var, value="U16").grid(row=4, column=1, sticky="w")
    ttk.Radiobutton(root, text="U18", variable=vanuse_var, value="U18").grid(row=4, column=2, sticky="w")
    ttk.Radiobutton(root, text="U20", variable=vanuse_var, value="U20").grid(row=4, column=3, sticky="w")

    ttk.Label(root, text="Võistluse kuupäev (YYYY-MM-DD):").grid(row=5, column=0, sticky="w", padx=5, pady=5)
    ttk.Entry(root, textvariable=kuupäev_var, width=15).grid(row=5, column=1, sticky="w")

    ttk.Label(root, text="Võistluse tüüp:").grid(row=6, column=0, sticky="w", padx=5, pady=5)
    tüüp_combo = ttk.Combobox(root, textvariable=tüüp_var, values=["ühepäevane ühel väljakul","ühepäevane kahel väljakul","kahepäevane ühel väljakul","kahepäevane kahel väljakul"], state="readonly", width=28)
    tüüp_combo.grid(row=6, column=1, sticky="w")

    ttk.Label(root, text="Algusaeg I päeval (HH:MM):").grid(row=7, column=0, sticky="w", padx=5, pady=5)
    ttk.Entry(root, textvariable=algus1_var, width=10).grid(row=7, column=1, sticky="w")
    ttk.Label(root, text="Algusaeg II päeval (HH:MM):").grid(row=8, column=0, sticky="w", padx=5, pady=5)
    ttk.Entry(root, textvariable=algus2_var, width=10).grid(row=8, column=1, sticky="w")

    ttk.Label(root, text="Koduvõistkonna nimi (või tühi):").grid(row=9, column=0, sticky="w", padx=5, pady=5)
    ttk.Entry(root, textvariable=kodu_var, width=30).grid(row=9, column=1, columnspan=2, sticky="w")

    def nupp_genereeri():
        global viimane_ajakava, viimased_võistkonnad, viimane_meta
        try:
            allikas = allikas_var.get()
            asukoht = ""
            if allikas == "tsoon":
                try:
                    tsooni_nr = int(tsoon_spin.get())
                except Exception:
                    raise ValueError("Tsooni number peab olema täisarv 1–10.")
                linn, võistkonnad = loe_tsoon(tsoonifail, tsooni_nr)
                asukoht = f"Tsoon {tsooni_nr}, {linn}"
                try:
                    võistkonnad = teisenda_tsoonist_turniiriks(võistkonnad)
                except Exception as e:
                    raise ValueError(f"Tsooni → turniiri teisendus ebaõnnestus: {e}")
            else:
                tekst = sisestus_box.get("1.0", tk.END).strip()
                read = tekst.splitlines()
                võistkonnad = []
                for r in read:
                    r2 = r.strip()
                    if not r2:
                        continue
                    r2 = r2.lstrip("0123456789. )").strip()
                    if r2:
                        võistkonnad.append(r2)
                k = kodu_var.get().strip()
                if k:
                    asukoht = k
                else:
                    asukoht = "Käsitsi sisestatud"
            if len(võistkonnad) == 0:
                raise ValueError("Võistkondi ei leitud. Kontrolli sisendit.")
            if len(võistkonnad) not in (5, 6):
                raise ValueError(f"Toetatud vaid 5 või 6 võistkonda. Leiti: {len(võistkonnad)}")
            värvid = {}
            for v in võistkonnad:
                r = random.randint(150, 255); g = random.randint(150, 255); b = random.randint(150, 255)
                värvid[v] = f'#{r:02x}{g:02x}{b:02x}'
            tulemus = genereeri_ajakava_gui(vanuseklass=vanuse_var.get(), kuupäev=kuupäev_var.get(), võistluse_tüüp=tüüp_var.get(), algus1=algus1_var.get(), algus2=algus2_var.get(), võistkonnad=võistkonnad, kodu_võistkond_nimi=kodu_var.get(), asukoht=asukoht, värvid=värvid)
            if tulemus is None:
                raise RuntimeError("genereeri_ajakava_gui ei tagastanud tulemusi - vaata terminali.")
            if not (isinstance(tulemus, tuple) and len(tulemus) == 5):
                raise RuntimeError("genereeri_ajakava_gui tagastas ootamatut struktuuri.")
            tabel, mängu_kestus, kahepäevane, algus1_dt, algus2_dt = tulemus
            ajakava_listiks = tee_ajakava_listiks(tabel, algus1_dt, kahepäevane, algus2_dt, mängu_kestus)
            viimane_ajakava = ajakava_listiks
            viimased_võistkonnad = võistkonnad[:]
            viimane_meta = {'kuupäev': kuupäev_var.get(), 'vanuseklass': vanuse_var.get(), 'tüüp': tüüp_var.get(), 'asukoht': asukoht}
            messagebox.showinfo("Valmis", "Ajakava genereeritud — vaata terminali väljundit.")
        except Exception as e:
            import traceback
            traceback.print_exc()
            messagebox.showerror("Viga", str(e))

    def nupp_eksport():
        try:
            tulemus = eksporti_excelisse("ajakava_tksheet.xlsx")
            if isinstance(tulemus, tuple):
                messagebox.showinfo("Eksport valmis", f"Failid salvestatud:\n{tulemus[0]}\n{tulemus[1]}")
            else:
                messagebox.showinfo("Eksport valmis", f"Excel-fail salvestatud: {tulemus}")
        except Exception as e:
            messagebox.showerror("Eksport ebaõnnestus", str(e))

    ttk.Button(root, text="Genereeri ajakava", command=nupp_genereeri).grid(row=10, column=0, columnspan=3, pady=10)
    ttk.Button(root, text="Eksport Exceli (.xlsx)", command=nupp_eksport).grid(row=11, column=0, columnspan=3, pady=5)

    root.mainloop()

if __name__ == "__main__":
    loo_gui()


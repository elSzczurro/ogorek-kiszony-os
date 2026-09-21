import tkinter as tk
from tkinter import messagebox, colorchooser
import time, datetime, random, json, os

czy_admin = False
PLIK_PAMIECI = "system_data.json"
KASA_START = 83457894574875634975394875983475

domyslne_dane = {
    "notatka": "",
    "zadania": [],
    "kolor_pulpitu": "#1e271f",
    "usuniete_pliki": [],
    "stan_konta": KASA_START,
    "historia_banku": []
}

def wczytaj_dane():
    if os.path.exists(PLIK_PAMIECI):
        try:
            with open(PLIK_PAMIECI, "r", encoding="utf-8") as f:
                d = json.load(f)
                if "stan_konta" not in d: d["stan_konta"] = KASA_START
                if "historia_banku" not in d: d["historia_banku"] = []
                if "usuniete_pliki" not in d: d["usuniete_pliki"] = []
                return d
        except:
            return domyslne_dane
    return domyslne_dane

def zapisz_dane():
    try:
        with open(PLIK_PAMIECI, "w", encoding="utf-8") as f:
            json.dump(dane_systemu, f, ensure_ascii=False, indent=4)
    except:
        pass

dane_systemu = wczytaj_dane()

def otworz_notatnik():
    okno = tk.Toplevel(pulpit); okno.title("Notatnik - OgórekKiszonyOS"); okno.geometry("400x300"); okno.configure(bg="#f4f9f4")
    pole_tekstowe = tk.Text(okno, font=("Consolas", 11), bg="#ffffff", fg="#1e272c")
    pole_tekstowe.pack(expand=True, fill="both", padx=5, pady=5)
    pole_tekstowe.insert("1.0", dane_systemu.get("notatka", ""))
    def zapisz_notatke():
        dane_systemu["notatka"] = pole_tekstowe.get("1.0", tk.END).strip()
        zapisz_dane()
    okno.bind("<Destroy>", lambda e: zapisz_notatke())
def otworz_kalkulator():
    okno = tk.Toplevel(pulpit); okno.title("Kalkulator"); okno.geometry("240x320"); okno.resizable(False, False); okno.configure(bg="#2e3d30")
    ekran = tk.Entry(okno, font=("Arial", 18), justify="right", bg="#1e271f", fg="#a2d4ab", bd=5); ekran.pack(pady=15, padx=10, fill="x")
    def klik(p):
        if p == "C": ekran.delete(0, tk.END)
        elif p == "=":
            try:
                w = ekran.get()
                if "+" in w: a, b = w.split("+"); r = float(a) + float(b)
                elif "-" in w: a, b = w.split("-"); r = float(a) - float(b)
                elif "*" in w: a, b = w.split("*"); r = float(a) * float(b)
                elif "/" in w: a, b = w.split("/"); r = float(a) / float(b) if float(b) != 0 else "Błąd"
                else: r = w
                ekran.delete(0, tk.END); ekran.insert(tk.END, str(r))
            except: ekran.delete(0, tk.END); ekran.insert(tk.END, "Błąd")
        else: ekran.insert(tk.END, p)
    ramka = tk.Frame(okno, bg="#2e3d30"); ramka.pack(expand=True, fill="both", padx=10, pady=5)
    uklad = [['7', '8', '9', '/'], ['4', '5', '6', '*'], ['1', '2', '3', '-'], ['C', '0', '=', '+']]
    for r, rzad in enumerate(uklad):
        for c, z in enumerate(rzad):
            btn = tk.Button(ramka, text=z, font=("Arial", 12, "bold"), bg="#4a5f4d", fg="white", command=lambda x=z: klik(x))
            btn.grid(row=r, column=c, sticky="nsew", padx=3, pady=3); ramka.grid_rowconfigure(r, weight=1); ramka.grid_columnconfigure(c, weight=1)

def otworz_ustawienia():
    okno = tk.Toplevel(pulpit); okno.title("Ustawienia"); okno.geometry("350x250"); okno.configure(bg="#2e3d30"); okno.resizable(False, False)
    tk.Label(okno, text="Ustawienia OgórekKiszonyOS", font=("Arial", 14, "bold"), bg="#2e3d30", fg="white").pack(pady=15)
    def zmien_kolor(k):
        pulpit.configure(bg=k); dane_systemu["kolor_pulpitu"] = k; zapisz_dane()
    tk.Button(okno, text="Motyw: Kiszony (Ciemny)", bg="#4a5f4d", fg="white", width=25, command=lambda: zmien_kolor("#1e271f")).pack(pady=5)
    tk.Button(okno, text="Motyw: Świeży (Jasny)", bg="#2ecc71", fg="white", width=25, command=lambda: zmien_kolor("#27ae60")).pack(pady=5)
    tk.Button(okno, text="Wybierz własny kolor...", bg="#34495e", fg="white", width=25, command=lambda: zmien_kolor(colorchooser.askcolor(title="Kolor"))).pack(pady=5)

def otworz_bank():
    okno_bank = tk.Toplevel(pulpit); okno_bank.title("Ogórkowy Bank"); okno_bank.geometry("450x450"); okno_bank.configure(bg="#2c3e50")
    lbl_tytul = tk.Label(okno_bank, text="💰 Ogórkowy Bank Krajowy 💰", font=("Arial", 14, "bold"), bg="#2c3e50", fg="#f1c40f"); lbl_tytul.pack(pady=10)
    lbl_saldo = tk.Label(okno_bank, text=f"Stan konta:\n{dane_systemu['stan_konta']:,} zł", font=("Arial", 11, "bold"), bg="#2c3e50", fg="white", justify="center", wraplength=400); lbl_saldo.pack(pady=10)
    frame_zakupy = tk.LabelFrame(okno_bank, text=" Kup coś ze sklepu ", font=("Arial", 10, "bold"), bg="#2c3e50", fg="#1abc9c", padx=10, pady=10); frame_zakupy.pack(pady=10, fill="x", padx=15)
    sklep = [("Fabryka Ogórków", 500000000000), ("Prywatna Wyspa Kiszona", 99999999999999), ("Złoty Słoik Świata", 88888888888888888), ("Superkomputer HubertX", 7345789457487563)]
    def kup(nazwa, cena):
        if dane_systemu["stan_konta"] >= cena:
            dane_systemu["stan_konta"] -= cena; data_zakupu = datetime.datetime.now().strftime("%H:%M:%S")
            dane_systemu["historia_banku"].insert(0, f"[{data_zakupu}] Kupiono: {nazwa} (-{cena:,} zł)"); zapisz_dane()
            lbl_saldo.config(text=f"Stan konta:\n{dane_systemu['stan_konta']:,} zł")
            box_historia.insert(0, dane_systemu["historia_banku"]); messagebox.showinfo("Sukces", f"Zakupiono: {nazwa}!")
        else: messagebox.showerror("Błąd", "Brak środków!")
    for nazwa, cena in sklep:
        tk.Button(frame_zakupy, text=f"{nazwa} ({cena:,} zł)", font=("Arial", 9), bg="#34495e", fg="white", anchor="w", command=lambda n=nazwa, c=cena: kup(n, c)).pack(fill="x", pady=2)
    tk.Label(okno_bank, text="Historia transakcji:", font=("Arial", 10, "bold"), bg="#2c3e50", fg="white").pack(pady=5)
    box_historia = tk.Listbox(okno_bank, font=("Consolas", 9), bg="#34495e", fg="#ecf0f1", height=6); box_historia.pack(fill="both", expand=True, padx=15, pady=5)
    for h in dane_systemu.get("historia_banku", []): box_historia.insert(tk.END, h)
def otworz_panel_beta():
    okno_beta = tk.Toplevel(pulpit); okno_beta.title("Panel Admina"); okno_beta.geometry("400x350"); okno_beta.configure(bg="#7f8c8d"); okno_beta.resizable(False, False)
    tk.Label(okno_beta, text="🛠️ PANEL ADMINA (BETA)", font=("Arial", 14, "bold"), bg="#7f8c8d", fg="#c0392b").pack(pady=15)
    def pokaz_ram(): messagebox.showinfo("RAM", f"Alokacja: {random.randint(120, 250)} MB")
    def crash(): pulpit.destroy()
    def wywolywacz_zaglady():
        if messagebox.askyesno("⚠️ ALERT ZAGŁADY", "Czy na pewno chcesz wywołać 1000 błędów na raz?"):
            for i in range(1000):
                okno_err = tk.Toplevel(pulpit); okno_err.title(f"Błąd {i+1}/1000"); okno_err.geometry(f"250x100+{random.randint(0, 800)}+{random.randint(0, 500)}"); okno_err.configure(bg="#c0392b")
                tk.Label(okno_err, text="System eksplodował!", fg="white", bg="#c0392b", font=("Arial", 10, "bold")).pack(pady=20)
                pulpit.update()
    tk.Button(okno_beta, text="Sprawdź zużycie systemu", font=("Arial", 10, "bold"), bg="#2c3e50", fg="white", width=30, command=pokaz_ram).pack(pady=5)
    tk.Button(okno_beta, text="💥 WYWOŁAJ 1000 BŁĘDÓW 💥", font=("Arial", 10, "bold"), bg="#e74c3c", fg="white", width=30, command=wywolywacz_zaglady).pack(pady=5)
    tk.Button(okno_beta, text="Zasymuluj Crash", font=("Arial", 10, "bold"), bg="#c0392b", fg="white", width=30, command=crash).pack(pady=5)

def otworz_gre():
    okno = tk.Toplevel(pulpit); okno.title("Gra"); okno.geometry("300x250"); okno.configure(bg="#2c3e50"); okno.resizable(False, False)
    wylosowana = random.randint(1, 100); stan = {"proby": 0}
    tk.Label(okno, text="Zgadnij liczbę od 1 do 100!", font=("Arial", 12, "bold"), bg="#2c3e50", fg="white").pack(pady=15)
    strzal = tk.Entry(okno, font=("Arial", 14), justify="center", width=10); strzal.pack(pady=5)
    wynik_lbl = tk.Label(okno, text="Wpisz liczbę!", font=("Arial", 10), bg="#2c3e50", fg="#ebd494"); wynik_lbl.pack(pady=10)
    def sprawdz():
        try:
            u = int(strzal.get()); stan["proby"] += 1
            if u < wylosowana: wynik_lbl.config(text="Za mało!")
            elif u > wylosowana: wynik_lbl.config(text="Za dużo!")
            else: wynik_lbl.config(text=f"Brawo! W {stan['proby']} próbach!"); messagebox.showinfo("Wygrana!", f"Liczba to {wylosowana}.")
        except: wynik_lbl.config(text="Wpisz liczbę!")
    tk.Button(okno, text="Sprawdź", font=("Arial", 11, "bold"), bg="#27ae60", fg="white", command=sprawdz).pack(pady=10)

def otworz_todo():
    okno = tk.Toplevel(pulpit); okno.title("Zadania"); okno.geometry("350x400"); okno.configure(bg="#34495e")
    gora = tk.Frame(okno, bg="#34495e"); gora.pack(pady=10)
    entry = tk.Entry(gora, font=("Arial", 12), width=18); entry.pack(side="left", padx=5)
    box = tk.Listbox(okno, font=("Arial", 12), width=30, height=15, bg="#ecf0f1", fg="#2c3e50"); box.pack(pady=10, expand=True, fill="both")
    for z in dane_systemu.get("zadania", []): box.insert(tk.END, z)
    def dodaj():
        t = entry.get().strip()
        if t: box.insert(tk.END, t); entry.delete(0, tk.END); dane_systemu["zadania"] = list(box.get(0, tk.END)); zapisz_dane()
    def usun():
        if box.curselection(): box.delete(box.curselection()); dane_systemu["zadania"] = list(box.get(0, tk.END)); zapisz_dane()
        else: messagebox.showwarning("Błąd", "Wybierz zadanie!")
    tk.Button(gora, text="Dodaj", bg="#2ecc71", fg="white", command=dodaj).pack(side="left")
    tk.Button(okno, text="Usuń", bg="#e74c3c", fg="white", command=usun).pack(pady=10)

def otworz_paint():
    okno_paint = tk.Toplevel(pulpit); okno_paint.title("Paint"); okno_paint.geometry("500x450"); okno_paint.configure(bg="#34495e")
    canvas = tk.Canvas(okno_paint, bg="white", cursor="pencil"); canvas.pack(expand=True, fill="both", padx=10, pady=10)
    def rysuj(event):
        x1, y1 = (event.x - 2), (event.y - 2); x2, y2 = (event.x + 2), (event.y + 2)
        canvas.create_oval(x1, y1, x2, y2, fill="black", outline="black")
    canvas.bind("<B1-Motion>", rysuj)
    tk.Button(okno_paint, text="Wyczyść", font=("Arial", 10, "bold"), bg="#e74c3c", fg="white", command=lambda: canvas.delete("all")).pack(pady=5)

def otworz_eksplorator():
    okno_exp = tk.Toplevel(pulpit); okno_exp.title("Eksplorator plików"); okno_exp.geometry("380x380"); okno_exp.configure(bg="#1a252f")
    tk.Label(okno_exp, text="Dysk systemowy (C:)", font=("Arial", 12, "bold"), bg="#1a252f", fg="white").pack(pady=10)
    lista_plikow = tk.Listbox(okno_exp, font=("Consolas", 11), bg="#2c3e50", fg="#ecf0f1", width=35, height=10); lista_plikow.pack(pady=10, padx=15, fill="both", expand=True)
    wszystkie_pliki = ["kernel_ogorek.dll", "jajco.sys", "config_kiszony.cfg", "system_pulpit.exe"]
    def odswiez_liste():
        lista_plikow.delete(0, tk.END)
        for p in wszystkie_pliki:
            if p not in dane_systemu.get("usuniete_pliki", []): lista_plikow.insert(tk.END, f"📄 {p}")
    odswiez_liste()
    def usun_plik():
        try:
            wybrany_tekst = lista_plikow.get(lista_plikow.curselection()); nazwa_pliku = wybrany_tekst.replace("📄 ", "")
            dane_systemu["usuniete_pliki"].append(nazwa_pliku); zapisz_dane(); odswiez_liste()
            if "jajco.sys" in nazwa_pliku:
                messagebox.showwarning("OSTRZEŻENIE", "Usunąłeś jajco.sys! System wariuje!")
                def dyskoteka(pr=0):
                    if pr < 10:
                        pulpit.configure(bg=random.choice(["#ff00ff", "#00ffff", "#ffff00", "#ff0000", dane_systemu["kolor_pulpitu"]]))
                        pulpit.after(200, lambda: dyskoteka(pr + 1))
                dyskoteka()
            elif "kernel_ogorek.dll" in nazwa_pliku:
                for _ in range(3): messagebox.showerror("BŁĄD", "Ogórek uciekł ze słoika!")
            else: messagebox.showinfo("Sukces", "Plik usunięty.")
        except: messagebox.showwarning("Błąd", "Wybierz plik!")
    def przywroc_pliki():
        if dane_systemu.get("usuniete_pliki", []):
            dane_systemu["usuniete_pliki"] = []; zapisz_dane(); odswiez_liste()
            messagebox.showinfo("Koszyk", "Wszystkie pliki systemowe zostały przywrócone!")
        else: messagebox.showinfo("Koszyk", "Brak plików do przywrócenia.")
    ramka_przyciski = tk.Frame(okno_exp, bg="#1a252f")
    ramka_przyciski.pack(pady=10)
    tk.Button(ramka_przyciski, text="Usuń plik", font=("Arial", 10, "bold"), bg="#c0392b", fg="white", command=usun_plik).pack(side="left", padx=5)
    tk.Button(ramka_przyciski, text="♻️ Przywróć pliki", font=("Arial", 10, "bold"), bg="#27ae60", fg="white", command=przywroc_pliki).pack(side="left", padx=5)

def zaladuj_pulpit():
    for w in pulpit.winfo_children():
        if isinstance(w, tk.Button) and w != btn_start: w.destroy()
    ikony = [("📝\nNotatnik", otworz_notatnik, "#a2d4ab"), ("🧮\nKalkulator", otworz_kalkulator, "#a2d4ab")]
    if czy_admin: ikony.append(("🛠️\nPanel Beta", otworz_panel_beta, "#c0392b"))
    ikony.extend([("🏦\nBank", otworz_bank, "#f1c40f"), ("📁\nPliki", otworz_eksplorator, "#f39c12"), ("🎨\nPaint", otworz_paint, "#1abc9c"), ("⚙️\nUstawienia", otworz_ustawienia, "#e67e22"), ("🎮\nGra", otworz_gre, "#3498db"), ("📋\nZadania", otworz_todo, "#f1c40f")])
    for i, (nazwa, funkcja, kolor) in enumerate(ikony):
        col = i // 6; row = i % 6
        btn = tk.Button(pulpit, text=nazwa, font=("Arial", 11, "bold"), bg="#2e3d30", fg=kolor, bd=0, command=funkcja)
        btn.place(x=40 + (col * 120), y=40 + (row * 105), width=90, height=80)

def sprawdz_logowanie():
    global czy_admin
    haslo = wpisane_haslo.get()
    if haslo == "admin123": czy_admin = True; okno_logowania.destroy(); pulpit.deiconify(); zaladuj_pulpit()
    elif haslo == "ogorek": czy_admin = False; okno_logowania.destroy(); pulpit.deiconify(); zaladuj_pulpit()
    else: messagebox.showerror("Błąd", "Złe hasło!")

pulpit = tk.Tk(); pulpit.title("OgórekKiszonyOS v2.1"); pulpit.attributes("-fullscreen", True)
pulpit.bind("<Escape>", lambda e: pulpit.attributes("-fullscreen", False)); pulpit.configure(bg=dane_systemu["kolor_pulpitu"]); pulpit.withdraw()
okno_logowania = tk.Tk(); okno_logowania.title("Logowanie"); okno_logowania.geometry("350x220"); okno_logowania.configure(bg="#141a14")
okno_logowania.eval('tk::PlaceWindow . center')
tk.Label(okno_logowania, text="🔒 Wprowadź hasło:", font=("Arial", 12, "bold"), bg="#141a14", fg="#a2d4ab").pack(pady=15)
wpisane_haslo = tk.Entry(okno_logowania, font=("Arial", 14), show="*", justify="center")
wpisane_haslo.pack(pady=5); wpisane_haslo.focus_set(); wpisane_haslo.bind("<Return>", lambda e: sprawdz_logowanie())
tk.Label(okno_logowania, text="Użyj 'ogorek' lub 'admin123'", font=("Arial", 9, "italic"), bg="#141a14", fg="#7f8c8d").pack(pady=2)
tk.Button(okno_logowania, text="Zaloguj", font=("Arial", 11, "bold"), bg="#27ae60", fg="white", command=sprawdz_logowanie).pack(pady=15)
pasek = tk.Frame(pulpit, bg="#141a14", height=45); pasek.pack(side="bottom", fill="x")
btn_start = tk.Button(pasek, text="🥒 START", font=("Arial", 11, "bold"), bg="#27ae60", fg="white", bd=0, command=lambda: messagebox.showinfo("OS", "OgórekKiszonyOS v2.1"))
btn_start.pack(side="left", padx=5, pady=5, ipady=3, ipadx=10)
tk.Button(pasek, text="❌ Wyłącz", font=("Arial", 10, "bold"), bg="#c0392b", fg="white", bd=0, command=lambda: pulpit.destroy() if messagebox.askyesno("Koniec", "Wyłączyć?") else None).pack(side="right", padx=5, pady=5, ipady=3, ipadx=5)
zegar = tk.Label(pasek, font=("Arial", 12, "bold"), bg="#141a14", fg="#a2d4ab"); zegar.pack(side="right", padx=15)
data_lbl = tk.Label(pasek, text=datetime.datetime.now().strftime("%d.%m.%Y"), font=("Arial", 11), bg="#141a14", fg="#7f8c8d"); data_lbl.pack(side="right", padx=5)
def odswiez_zegar(): zegar.config(text=time.strftime("%H:%M:%S")); pulpit.after(1000, odswiez_zegar)
odswiez_zegar(); okno_logowania.mainloop()
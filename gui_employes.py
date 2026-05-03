import tkinter as tk
from tkinter import messagebox, ttk
import csv
import os
import datetime

FICHIER = "employes.csv"
USERS_FILE = "users.csv"
AUDIT_FILE = "audit.log"
HIGH_SAL_FILE = "high_salary.csv"
REPORT_FILE = "report.txt"
COLONNES_REQUISES = ["id", "nom", "prenom", "poste", "salaire", "departement"]
DEPARTEMENTS_VALIDES = ["Informatique", "Finance", "RH", "Support", "Communication", "Marketing", "Direction"]

def charger_employes():
    if not os.path.exists(FICHIER):
        return []
    employes = []
    with open(FICHIER, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=';')
        for row in reader:
            employes.append(dict(row))
    return employes

def sauvegarder_employes(employes):
    with open(FICHIER, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=COLONNES_REQUISES, delimiter=';')
        writer.writeheader()
        for e in employes:
            writer.writerow(e)

def charger_users():
    users = {}
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'w', newline='', encoding='utf-8') as f:
            w = csv.writer(f, delimiter=';')
            w.writerow(["username", "password"])
            w.writerow(["admin", "admin123"])
            w.writerow(["user1", "pass1"])
    with open(USERS_FILE, newline='', encoding='utf-8') as f:
        for row in csv.DictReader(f, delimiter=';'):
            users[row['username']] = row['password']
    return users

def log_audit(msg):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(AUDIT_FILE, 'a', encoding='utf-8') as f:
        f.write("[" + now + "] " + msg + "\n")

class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Connexion")
        self.root.resizable(False, False)
        self.tentatives = 0
        self.users = charger_users()

        tk.Label(root, text="Gestion Employes", font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=2, pady=10)
        tk.Label(root, text="Username :").grid(row=1, column=0, padx=10, sticky="e")
        tk.Label(root, text="Password :").grid(row=2, column=0, padx=10, sticky="e")

        self.entry_user = tk.Entry(root, width=20)
        self.entry_pass = tk.Entry(root, width=20, show="*")
        self.entry_user.grid(row=1, column=1, padx=10, pady=5)
        self.entry_pass.grid(row=2, column=1, padx=10, pady=5)

        self.lbl_msg = tk.Label(root, text="", fg="red")
        self.lbl_msg.grid(row=3, column=0, columnspan=2)

        tk.Button(root, text="Connexion", width=15, command=self.login).grid(row=4, column=0, columnspan=2, pady=10)
        self.entry_pass.bind("<Return>", lambda e: self.login())

    def login(self):
        u = self.entry_user.get().strip()
        p = self.entry_pass.get().strip()
        if u in self.users and self.users[u] == p:
            log_audit("Connexion OK : " + u)
            self.root.destroy()
            main_app()
        else:
            self.tentatives += 1
            log_audit("Echec connexion : " + u)
            restant = 3 - self.tentatives
            if self.tentatives >= 3:
                log_audit("Compte bloque apres 3 tentatives.")
                messagebox.showerror("Bloque", "Trop de tentatives. Fermeture.")
                self.root.destroy()
            else:
                self.lbl_msg.config(text="Identifiants incorrects. Restantes : " + str(restant))
                self.entry_pass.delete(0, tk.END)

class AppEmployes:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestion des Employes")
        self.root.geometry("900x550")
        self.employes = charger_employes()
        self.build_ui()

    def build_ui(self):
        # ── top frame: buttons ──
        top = tk.Frame(self.root, bg="#2c3e50", pady=6)
        top.pack(fill="x")

        btn_style = {"bg": "#3498db", "fg": "white", "width": 14, "relief": "flat", "padx": 4}
        tk.Button(top, text="Stats",           **btn_style, command=self.show_stats).pack(side="left", padx=4)
        tk.Button(top, text="Ajouter",         **btn_style, command=self.open_ajouter).pack(side="left", padx=4)
        tk.Button(top, text="Modifier",        **btn_style, command=self.open_modifier).pack(side="left", padx=4)
        tk.Button(top, text="Supprimer",       **btn_style, command=self.supprimer).pack(side="left", padx=4)
        tk.Button(top, text="Filtrer Dept",    **btn_style, command=self.filtrer_dept).pack(side="left", padx=4)
        tk.Button(top, text="Filtrer Salaire", **btn_style, command=self.filtrer_salaire).pack(side="left", padx=4)
        tk.Button(top, text="Trier",           **btn_style, command=self.trier).pack(side="left", padx=4)
        tk.Button(top, text="Exporter >4000",  **btn_style, command=self.exporter).pack(side="left", padx=4)
        tk.Button(top, text="Rapport",         **btn_style, command=self.rapport).pack(side="left", padx=4)
        tk.Button(top, text="Doublons",        **btn_style, command=self.doublons).pack(side="left", padx=4)

        # ── search bar ──
        mid = tk.Frame(self.root, pady=4)
        mid.pack(fill="x", padx=8)
        tk.Label(mid, text="Recherche ID :").pack(side="left")
        self.entry_search = tk.Entry(mid, width=10)
        self.entry_search.pack(side="left", padx=4)
        tk.Button(mid, text="Chercher", command=self.chercher_id).pack(side="left")
        tk.Button(mid, text="Afficher tout", command=self.refresh_table).pack(side="left", padx=6)
        self.lbl_info = tk.Label(mid, text="", fg="green")
        self.lbl_info.pack(side="left", padx=10)

        # ── table ──
        cols = ("ID", "Nom", "Prenom", "Poste", "Salaire", "Departement")
        self.tree = ttk.Treeview(self.root, columns=cols, show="headings", height=20)
        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=130 if c != "Poste" else 160)
        scroll = ttk.Scrollbar(self.root, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll.set)
        self.tree.pack(side="left", fill="both", expand=True, padx=8, pady=6)
        scroll.pack(side="left", fill="y", pady=6)

        self.refresh_table()

    def refresh_table(self, data=None):
        self.employes = charger_employes()
        if data is None:
            data = self.employes
        for row in self.tree.get_children():
            self.tree.delete(row)
        for e in data:
            self.tree.insert("", "end", values=(
                e['id'], e['nom'], e['prenom'], e['poste'], e['salaire'], e['departement']
            ))
        self.lbl_info.config(text=str(len(data)) + " employe(s) affiches")

    def get_selected_id(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Attention", "Selectionnez un employe dans la liste.")
            return None
        return self.tree.item(sel[0])['values'][0]

    def show_stats(self):
        if not self.employes:
            messagebox.showinfo("Stats", "Aucun employe.")
            return
        salaires = []
        for e in self.employes:
            try:
                salaires.append(float(e['salaire']))
            except ValueError:
                pass
        moy = sum(salaires) / len(salaires) if salaires else 0
        msg = (
            "Total employes : " + str(len(self.employes)) + "\n"
            "Salaire moyen  : " + str(round(moy, 2)) + " DT\n"
            "Salaire min    : " + str(min(salaires)) + " DT\n"
            "Salaire max    : " + str(max(salaires)) + " DT"
        )
        messagebox.showinfo("Statistiques", msg)

    def chercher_id(self):
        eid = self.entry_search.get().strip()
        res = [e for e in self.employes if e['id'] == eid]
        if not res:
            messagebox.showinfo("Recherche", "Aucun employe avec ID " + eid)
        else:
            self.refresh_table(res)

    def open_ajouter(self):
        win = tk.Toplevel(self.root)
        win.title("Ajouter un employe")
        win.resizable(False, False)
        fields = ["ID", "Nom", "Prenom", "Poste", "Salaire"]
        entries = {}
        for i, f in enumerate(fields):
            tk.Label(win, text=f + " :").grid(row=i, column=0, padx=10, pady=4, sticky="e")
            e = tk.Entry(win, width=22)
            e.grid(row=i, column=1, padx=10, pady=4)
            entries[f] = e
        tk.Label(win, text="Departement :").grid(row=len(fields), column=0, padx=10, sticky="e")
        dept_var = tk.StringVar(value=DEPARTEMENTS_VALIDES[0])
        tk.OptionMenu(win, dept_var, *DEPARTEMENTS_VALIDES).grid(row=len(fields), column=1, padx=10, pady=4, sticky="w")

        def valider():
            new_id = entries["ID"].get().strip()
            nom = entries["Nom"].get().strip()
            prenom = entries["Prenom"].get().strip()
            poste = entries["Poste"].get().strip()
            sal_str = entries["Salaire"].get().strip()
            dept = dept_var.get()
            if not new_id.isdigit():
                messagebox.showerror("Erreur", "ID invalide.", parent=win)
                return
            if any(e['id'] == new_id for e in self.employes):
                messagebox.showerror("Erreur", "ID existe deja.", parent=win)
                return
            if not nom or not prenom or not poste:
                messagebox.showerror("Erreur", "Champs manquants.", parent=win)
                return
            try:
                sal = float(sal_str)
                if sal <= 0:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Erreur", "Salaire invalide.", parent=win)
                return
            self.employes.append({
                "id": new_id, "nom": nom, "prenom": prenom,
                "poste": poste, "salaire": str(sal), "departement": dept
            })
            sauvegarder_employes(self.employes)
            self.refresh_table()
            messagebox.showinfo("OK", "Employe ajoute.", parent=win)
            win.destroy()

        tk.Button(win, text="Ajouter", command=valider, bg="#27ae60", fg="white", width=12).grid(
            row=len(fields)+1, column=0, columnspan=2, pady=10)

    def open_modifier(self):
        eid = self.get_selected_id()
        if eid is None:
            return
        emp = next((e for e in self.employes if e['id'] == str(eid)), None)
        if emp is None:
            return
        win = tk.Toplevel(self.root)
        win.title("Modifier employe " + str(eid))
        win.resizable(False, False)
        fields = [("Nom", emp['nom']), ("Prenom", emp['prenom']),
                  ("Poste", emp['poste']), ("Salaire", emp['salaire'])]
        entries = {}
        for i, (label, val) in enumerate(fields):
            tk.Label(win, text=label + " :").grid(row=i, column=0, padx=10, pady=4, sticky="e")
            e = tk.Entry(win, width=22)
            e.insert(0, val)
            e.grid(row=i, column=1, padx=10, pady=4)
            entries[label] = e
        tk.Label(win, text="Departement :").grid(row=len(fields), column=0, padx=10, sticky="e")
        dept_var = tk.StringVar(value=emp['departement'])
        tk.OptionMenu(win, dept_var, *DEPARTEMENTS_VALIDES).grid(row=len(fields), column=1, padx=10, pady=4, sticky="w")

        def valider():
            nom = entries["Nom"].get().strip()
            prenom = entries["Prenom"].get().strip()
            poste = entries["Poste"].get().strip()
            sal_str = entries["Salaire"].get().strip()
            dept = dept_var.get()
            if not nom or not prenom or not poste:
                messagebox.showerror("Erreur", "Champs vides.", parent=win)
                return
            try:
                sal = float(sal_str)
                if sal <= 0:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Erreur", "Salaire invalide.", parent=win)
                return
            emp['nom'] = nom
            emp['prenom'] = prenom
            emp['poste'] = poste
            emp['salaire'] = str(sal)
            emp['departement'] = dept
            sauvegarder_employes(self.employes)
            self.refresh_table()
            messagebox.showinfo("OK", "Modifie.", parent=win)
            win.destroy()

        tk.Button(win, text="Enregistrer", command=valider, bg="#e67e22", fg="white", width=12).grid(
            row=len(fields)+1, column=0, columnspan=2, pady=10)

    def supprimer(self):
        eid = self.get_selected_id()
        if eid is None:
            return
        if messagebox.askyesno("Confirmer", "Supprimer employe ID " + str(eid) + " ?"):
            self.employes = [e for e in self.employes if e['id'] != str(eid)]
            sauvegarder_employes(self.employes)
            self.refresh_table()

    def filtrer_dept(self):
        win = tk.Toplevel(self.root)
        win.title("Filtrer par departement")
        win.resizable(False, False)
        tk.Label(win, text="Departement :").grid(row=0, column=0, padx=10, pady=10)
        dept_var = tk.StringVar(value=DEPARTEMENTS_VALIDES[0])
        tk.OptionMenu(win, dept_var, *DEPARTEMENTS_VALIDES).grid(row=0, column=1, padx=10)

        def appliquer():
            d = dept_var.get()
            res = [e for e in self.employes if e['departement'] == d]
            self.refresh_table(res)
            win.destroy()

        tk.Button(win, text="Filtrer", command=appliquer, bg="#3498db", fg="white").grid(
            row=1, column=0, columnspan=2, pady=10)

    def filtrer_salaire(self):
        win = tk.Toplevel(self.root)
        win.title("Filtrer par salaire")
        win.resizable(False, False)
        tk.Label(win, text="Min (DT) :").grid(row=0, column=0, padx=10, pady=6, sticky="e")
        tk.Label(win, text="Max (DT) :").grid(row=1, column=0, padx=10, pady=6, sticky="e")
        entry_min = tk.Entry(win, width=12)
        entry_max = tk.Entry(win, width=12)
        entry_min.grid(row=0, column=1, padx=10)
        entry_max.grid(row=1, column=1, padx=10)

        def appliquer():
            try:
                smin = float(entry_min.get().strip())
                smax = float(entry_max.get().strip())
            except ValueError:
                messagebox.showerror("Erreur", "Entrez des nombres.", parent=win)
                return
            res = []
            for e in self.employes:
                try:
                    if smin <= float(e['salaire']) <= smax:
                        res.append(e)
                except ValueError:
                    pass
            self.refresh_table(res)
            win.destroy()

        tk.Button(win, text="Filtrer", command=appliquer, bg="#3498db", fg="white").grid(
            row=2, column=0, columnspan=2, pady=10)

    def trier(self):
        win = tk.Toplevel(self.root)
        win.title("Trier")
        win.resizable(False, False)
        choix = tk.StringVar(value="1")
        tk.Radiobutton(win, text="Salaire croissant",   variable=choix, value="1").pack(anchor="w", padx=20, pady=4)
        tk.Radiobutton(win, text="Salaire decroissant", variable=choix, value="2").pack(anchor="w", padx=20, pady=4)
        tk.Radiobutton(win, text="Departement A-Z",     variable=choix, value="3").pack(anchor="w", padx=20, pady=4)

        def appliquer():
            def get_sal(e):
                try:
                    return float(e['salaire'])
                except ValueError:
                    return 0.0
            match choix.get():
                case "1":
                    tri = sorted(self.employes, key=get_sal)
                case "2":
                    tri = sorted(self.employes, key=get_sal, reverse=True)
                case "3":
                    tri = sorted(self.employes, key=lambda x: x['departement'])
                case _:
                    tri = self.employes
            self.refresh_table(tri)
            win.destroy()

        tk.Button(win, text="Trier", command=appliquer, bg="#3498db", fg="white", width=10).pack(pady=10)

    def exporter(self):
        res = []
        for e in self.employes:
            try:
                if float(e['salaire']) > 4000:
                    res.append(e)
            except ValueError:
                pass
        with open(HIGH_SAL_FILE, 'w', newline='', encoding='utf-8') as f:
            w = csv.DictWriter(f, fieldnames=COLONNES_REQUISES, delimiter=';')
            w.writeheader()
            for e in res:
                w.writerow(e)
        messagebox.showinfo("Export", str(len(res)) + " employe(s) exportes dans " + HIGH_SAL_FILE)

    def rapport(self):
        stats = {}
        for e in self.employes:
            dept = e.get('departement', 'Autre')
            try:
                sal = float(e['salaire'])
            except ValueError:
                sal = 0
            if dept not in stats:
                stats[dept] = {'c': 0, 't': 0}
            stats[dept]['c'] += 1
            stats[dept]['t'] += sal

        lignes = ["=== RAPPORT PAR DEPARTEMENT ===", ""]
        for d in stats:
            c = stats[d]['c']
            m = stats[d]['t'] / c if c else 0
            lignes.append(d + " : " + str(c) + " emp, moy=" + str(round(m, 2)) + " DT")
            lignes.append("#" * c)
            lignes.append("")

        with open(REPORT_FILE, 'w', encoding='utf-8') as f:
            for l in lignes:
                f.write(l + "\n")

        win = tk.Toplevel(self.root)
        win.title("Rapport")
        txt = tk.Text(win, width=55, height=20, font=("Courier", 10))
        txt.pack(padx=10, pady=10)
        for l in lignes:
            txt.insert("end", l + "\n")
        txt.config(state="disabled")

    def doublons(self):
        vus = set()
        unique = []
        for e in self.employes:
            if e['id'] not in vus:
                vus.add(e['id'])
                unique.append(e)
        nb = len(self.employes) - len(unique)
        sauvegarder_employes(unique)
        self.employes = unique
        self.refresh_table()
        messagebox.showinfo("Doublons", str(nb) + " doublon(s) supprime(s).")

def main_app():
    root = tk.Tk()
    AppEmployes(root)
    root.mainloop()

root = tk.Tk()
LoginWindow(root)
root.mainloop()

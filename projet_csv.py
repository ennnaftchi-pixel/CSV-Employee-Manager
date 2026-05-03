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
        print("Erreur : fichier introuvable -> " + FICHIER)
        return None
    employes = []
    with open(FICHIER, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=';')
        colonnes = reader.fieldnames
        if colonnes is None:
            print("Erreur : fichier vide.")
            return None
        for col in COLONNES_REQUISES:
            if col not in colonnes:
                print("Erreur : colonne manquante -> " + col)
                return None
        for row in reader:
            employes.append(dict(row))
    return employes

def sauvegarder_employes(employes):
    with open(FICHIER, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=COLONNES_REQUISES, delimiter=';')
        writer.writeheader()
        for e in employes:
            writer.writerow(e)

def afficher_employe(e):
    print("  ID:", e['id'], "|", e['prenom'], e['nom'], "|", e['poste'], "|", e['salaire'], "DT |", e['departement'])

def afficher_statistiques(employes):
    if not employes:
        print("Aucun employe.")
        return
    print("Total employes :", len(employes))
    salaires = []
    for e in employes:
        try:
            salaires.append(float(e['salaire']))
        except ValueError:
            print("Salaire non lisible pour ID:", e['id'])
    if salaires:
        moy = sum(salaires) / len(salaires)
        print("Moyenne :", round(moy, 2), "DT")
        print("Min     :", min(salaires), "DT")
        print("Max     :", max(salaires), "DT")


def rechercher_par_id(employes, eid):
    for e in employes:
        if e['id'] == str(eid):
            return e
    return None

def ajouter_employe(employes):
    print("\n-- Ajouter --")
    new_id = input("ID : ").strip()
    if not new_id.isdigit():
        print("ID invalide.")
        return employes
    if rechercher_par_id(employes, new_id):
        print("ID existe deja.")
        return employes
    nom = input("Nom : ").strip()
    prenom = input("Prenom : ").strip()
    poste = input("Poste : ").strip()
    salaire_str = input("Salaire : ").strip()
    try:
        salaire = float(salaire_str)
        if salaire <= 0:
            print("Salaire doit etre positif.")
            return employes
    except ValueError:
        print("Salaire invalide, entrez un nombre.")
        return employes
    print("Departements :", ", ".join(DEPARTEMENTS_VALIDES))
    dept = input("Departement : ").strip()
    if dept not in DEPARTEMENTS_VALIDES:
        print("Departement invalide.")
        return employes
    if not nom or not prenom or not poste:
        print("Champs manquants.")
        return employes
    employes.append({
        "id": new_id,
        "nom": nom,
        "prenom": prenom,
        "poste": poste,
        "salaire": str(salaire),
        "departement": dept
    })
    sauvegarder_employes(employes)
    print("Employe ajoute.")
    return employes

def lire_employe(employes):
    eid = input("ID : ").strip()
    e = rechercher_par_id(employes, eid)
    if e:
        afficher_employe(e)
    else:
        print("Non trouve.")

def modifier_employe(employes):
    print("\n-- Modifier --")
    eid = input("ID : ").strip()
    e = rechercher_par_id(employes, eid)
    if not e:
        print("Non trouve.")
        return employes
    afficher_employe(e)
    nom = input("Nom [" + e['nom'] + "] : ").strip()
    prenom = input("Prenom [" + e['prenom'] + "] : ").strip()
    poste = input("Poste [" + e['poste'] + "] : ").strip()
    salaire_str = input("Salaire [" + e['salaire'] + "] : ").strip()
    print("Departements :", ", ".join(DEPARTEMENTS_VALIDES))
    dept = input("Departement [" + e['departement'] + "] : ").strip()
    if nom:
        e['nom'] = nom
    if prenom:
        e['prenom'] = prenom
    if poste:
        e['poste'] = poste
    if salaire_str:
        try:
            sal = float(salaire_str)
            if sal > 0:
                e['salaire'] = str(sal)
            else:
                print("Salaire invalide, ignore.")
        except ValueError:
            print("Salaire invalide, ignore.")
    if dept:
        if dept in DEPARTEMENTS_VALIDES:
            e['departement'] = dept
        else:
            print("Departement invalide, ignore.")
    sauvegarder_employes(employes)
    print("Modifie.")
    return employes

def supprimer_employe(employes):
    eid = input("ID : ").strip()
    e = rechercher_par_id(employes, eid)
    if not e:
        print("Non trouve.")
        return employes
    afficher_employe(e)
    if input("Confirmer (oui/non) : ").strip().lower() == "oui":
        employes.remove(e)
        sauvegarder_employes(employes)
        print("Supprime.")
    else:
        print("Annule.")
    return employes

def filtrer_par_departement(employes):
    print("Departements :", ", ".join(DEPARTEMENTS_VALIDES))
    dept = input("Departement : ").strip()
    res = [e for e in employes if e['departement'].lower() == dept.lower()]
    if not res:
        print("Aucun resultat.")
    else:
        for e in res:
            afficher_employe(e)

def filtrer_par_salaire(employes):
    try:
        smin = float(input("Min : ").strip())
        smax = float(input("Max : ").strip())
    except ValueError:
        print("Entrez des nombres valides.")
        return
    res = []
    for e in employes:
        try:
            if smin <= float(e['salaire']) <= smax:
                res.append(e)
        except ValueError:
            pass
    if not res:
        print("Aucun resultat.")
    else:
        for e in res:
            afficher_employe(e)

def get_salaire_float(e):
    try:
        return float(e['salaire'])
    except ValueError:
        return 0.0

def trier_employes(employes):
    print("1 Salaire croissant")
    print("2 Salaire decroissant")
    print("3 Departement A-Z")
    c = input("Choix : ").strip()
    match c:
        case "1":
            tri = sorted(employes, key=get_salaire_float)
        case "2":
            tri = sorted(employes, key=get_salaire_float, reverse=True)
        case "3":
            tri = sorted(employes, key=lambda x: x['departement'])
        case _:
            print("Choix invalide.")
            return
    for e in tri:
        afficher_employe(e)

def exporter_high_salary(employes):
    res = []
    for e in employes:
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
    print("Export fini :", len(res), "employes")

def generer_rapport(employes):
    stats = {}
    for e in employes:
        dept = e.get('departement', 'Autre')
        try:
            sal = float(e['salaire'])
        except ValueError:
            sal = 0
        if dept not in stats:
            stats[dept] = {'c': 0, 't': 0}
        stats[dept]['c'] += 1
        stats[dept]['t'] += sal

    lignes = ["RAPPORT PAR DEPARTEMENT", ""]
    for d in stats:
        c = stats[d]['c']
        m = stats[d]['t'] / c if c else 0
        lignes.append(d + " : " + str(c) + " emp, moy=" + str(round(m, 2)) + " DT")
        lignes.append("#" * c)
        lignes.append("")

    with open(REPORT_FILE, 'w', encoding='utf-8') as f:
        for l in lignes:
            f.write(l + "\n")

    print("Rapport cree -> " + REPORT_FILE)
    for l in lignes:
        print(l)

def supprimer_doublons(employes):
    vus = set()
    unique = []
    for e in employes:
        if e['id'] not in vus:
            vus.add(e['id'])
            unique.append(e)
    nb = len(employes) - len(unique)
    sauvegarder_employes(unique)
    print("Doublons supprimes :", nb)
    return unique

def init_users():
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'w', newline='', encoding='utf-8') as f:
            w = csv.writer(f, delimiter=';')
            w.writerow(["username", "password"])
            w.writerow(["admin", "admin123"])
            w.writerow(["user1", "pass1"])

def charger_users():
    users = {}
    if not os.path.exists(USERS_FILE):
        return users
    with open(USERS_FILE, newline='', encoding='utf-8') as f:
        for row in csv.DictReader(f, delimiter=';'):
            users[row['username']] = row['password']
    return users

def log_audit(msg):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(AUDIT_FILE, 'a', encoding='utf-8') as f:
        f.write("[" + now + "] " + msg + "\n")

def authentification():
    init_users()
    users = charger_users()
    for i in range(3):
        u = input("User : ").strip()
        p = input("Pass : ").strip()
        if u in users and users[u] == p:
            print("Bienvenue, " + u + " !")
            log_audit("Connexion OK : " + u)
            return True
        print("Identifiants incorrects. Tentatives restantes :", 2 - i)
        log_audit("Echec connexion : " + u)
    print("Compte bloque.")
    log_audit("Compte bloque apres 3 tentatives.")
    return False

def menu_crud(emp):
    while True:
        print("\n1 Ajouter")
        print("2 Rechercher")
        print("3 Modifier")
        print("4 Supprimer")
        print("0 Retour")
        c = input("> ").strip()
        match c:
            case "1":
                emp = ajouter_employe(emp)
            case "2":
                lire_employe(emp)
            case "3":
                emp = modifier_employe(emp)
            case "4":
                emp = supprimer_employe(emp)
            case "0":
                return emp
            case _:
                print("Choix invalide.")

def menu_filtrage_tri(emp):
    while True:
        print("\n1 Filtrer par departement")
        print("2 Filtrer par salaire")
        print("3 Trier")
        print("0 Retour")
        c = input("> ").strip()
        match c:
            case "1":
                filtrer_par_departement(emp)
            case "2":
                filtrer_par_salaire(emp)
            case "3":
                trier_employes(emp)
            case "0":
                break
            case _:
                print("Choix invalide.")

def menu_principal():
    if not authentification():
        return

    emp = charger_employes()
    if emp is None:
        return

    while True:
        print("GESTION DES EMPLOYES")
        print("1 Stats")
        print("2 CRUD")
        print("3 Filtrer / Trier")
        print("4 Exporter salaires > 4000")
        print("5 Rapport")
        print("6 Supprimer doublons")
        print("0 Quitter")
        c = input("> ").strip()
        match c:
            case "1":
                afficher_statistiques(emp)
            case "2":
                emp = menu_crud(emp)
            case "3":
                menu_filtrage_tri(emp)
            case "4":
                exporter_high_salary(emp)
            case "5":
                generer_rapport(emp)
            case "6":
                emp = supprimer_doublons(emp)
            case "0":
                print("Au revoir !")
                break
            case _:
                print("Choix invalide.")

menu_principal()

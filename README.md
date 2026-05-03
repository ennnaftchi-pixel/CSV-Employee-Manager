====================================================
  MINI PROJET - GESTION EMPLOYES CSV
  Niveau L1CS | ISI | Annee 2025-2026
====================================================

FICHIERS DU PROJET :
  projet_csv.py     -> application en ligne de commande (CLI)
  gui_employes.py   -> application avec interface graphique (Tkinter)
  employes.csv      -> fichier de donnees des employes
  users.csv         -> comptes de connexion (cree automatiquement)
  audit.log         -> journal des connexions
  high_salary.csv   -> genere par l'application (salaires > 4000 DT)
  report.txt        -> rapport statistique par departement

COMMENT LANCER :
  Version CLI :
    python projet_csv.py

  Version GUI :
    python gui_employes.py

IDENTIFIANTS PAR DEFAUT :
  admin / admin123
  user1 / pass1

FORMAT DU FICHIER employes.csv :
  id;nom;prenom;poste;salaire;departement
  Separateur : point-virgule (;)
  Encodage   : UTF-8

DEPARTEMENTS VALIDES :
  Informatique, Finance, RH, Support,
  Communication, Marketing, Direction

FONCTIONNALITES :

  1. AUTHENTIFICATION
     - Connexion via users.csv
     - Maximum 3 tentatives avant blocage
     - Toutes les connexions loggees dans audit.log

  2. STATISTIQUES
     - Nombre total d'employes
     - Salaire moyen, minimum, maximum

  3. CRUD
     - Ajouter un employe (validation ID unique + salaire positif + departement valide)
     - Rechercher par ID
     - Modifier les informations (departement valide oblige)
     - Supprimer avec confirmation

  4. FILTRAGE ET TRI
     - Filtrer par departement
     - Filtrer par plage de salaires
     - Trier par salaire (croissant ou decroissant)
     - Trier par departement (A-Z)

  5. EXPORT
     - Exporte les employes avec salaire > 4000 DT dans high_salary.csv

  6. RAPPORT
     - Statistiques par departement : nombre d'employes + salaire moyen
     - Histogramme textuel (#) par departement
     - Sauvegarde dans report.txt

  7. DOUBLONS
     - Detection et suppression automatique des IDs en double

CONTRAINTES TECHNIQUES :
  - Bibliotheques standard uniquement (csv, os, datetime, tkinter)
  - Pas de pandas
  - Encodage UTF-8 partout
  - Gestion des erreurs avec except ValueError (specifique)
  - Menus avec match/case (Python 3.10+)

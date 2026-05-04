# ============================================================
#  PROJET  : Smart Santé 2035
#  FICHIER : app.py
#  RÔLE    : Point d'entrée du back-end Flask.
#            Initialise l'application, configure les routes
#            et démarre le serveur REST.
#
#  POUR LANCER :
#    pip install flask
#    python app.py
#
#  API disponible sur : http://localhost:5000
#
#  NIVEAU  : Licence 2 Informatique – GPI
# ============================================================

from flask import Flask, request, jsonify
import sys, os

# Ajouter le dossier courant au path Python
sys.path.insert(0, os.path.dirname(__file__))

from model.patient           import Patient
from model.constantes_vitales import ConstantesVitales
from algorithme.file_priorite import FilePrioriteTriageQ
from algorithme.graphe_hospitalier import (
    GrapheHospitalier, EtablissementSante,
    GOUDRON, PISTE, IMPRATICABLE
)
from algorithme.table_hachage import TableDeHachage

# ── Initialisation de l'application Flask ────────────────────
app = Flask(__name__)

# ── Initialisation des modules algorithmiques ────────────────

# Module MTI : file de triage (tas binaire)
file_triage = FilePrioriteTriageQ(capacite_max=500)

# Module MGD : table de hachage pour les dossiers patients
dossiers_patients = TableDeHachage()

# Module MOH : graphe hospitalier pour Dijkstra
graphe = GrapheHospitalier()

# ── Chargement des données initiales du graphe ───────────────

def initialiser_graphe():
    """
    Charge les établissements de santé et les routes dans le graphe.
    En production : ces données viendraient de la base PostgreSQL.
    """
    # Ajouter les établissements (noeuds du graphe)
    etabs = [
        EtablissementSante("CSB-01",   "CSB Manakambahiny",
                           EtablissementSante.CSB_II,
                           -18.91, 47.53, 20, 15),
        EtablissementSante("HOP-DIS",  "Hôpital District Antananarivo",
                           EtablissementSante.HOPITAL_DIS,
                           -18.92, 47.51, 80, 12),
        EtablissementSante("HOP-REF",  "Hôpital de Référence Analakely",
                           EtablissementSante.HOP_REF_REG,
                           -18.90, 47.52, 200, 35),
        EtablissementSante("CHUR-ANT", "CHUR Antananarivo",
                           EtablissementSante.CHUR,
                           -18.89, 47.50, 500, 60),
        EtablissementSante("HOP-SAT",  "Hôpital Saturé (exemple)",
                           EtablissementSante.HOPITAL_DIS,
                           -18.91, 47.55, 60, 0),  # 0 lits !
    ]
    for e in etabs:
        graphe.ajouter_noeud(e)

    # Ajouter les routes (arcs du graphe)
    # (id_source, id_dest, distance_km, temps_min, etat_route, ambulance)
    graphe.ajouter_arc("CSB-01",  "HOP-DIS",   8.5,  25, GOUDRON, True)
    graphe.ajouter_arc("CSB-01",  "HOP-SAT",   3.0,  10, GOUDRON, False)
    graphe.ajouter_arc("CSB-01",  "HOP-REF",  15.0,  40, PISTE,   False)
    graphe.ajouter_arc("HOP-DIS", "HOP-REF",   7.0,  20, GOUDRON, True)
    graphe.ajouter_arc("HOP-DIS", "CHUR-ANT", 12.0,  30, GOUDRON, True)
    graphe.ajouter_arc("HOP-REF", "CHUR-ANT",  5.0,  15, GOUDRON, True)
    graphe.ajouter_arc("HOP-SAT", "HOP-DIS",   6.0,  18, GOUDRON, False)

    print("✅ Graphe hospitalier initialisé avec succès.")

# Initialiser le graphe au démarrage
initialiser_graphe()


# ════════════════════════════════════════════════════════════
#  ROUTES API REST
# ════════════════════════════════════════════════════════════

# ── ROUTE 1 : Accueil ────────────────────────────────────────

@app.route("/", methods=["GET"])
def accueil():
    """
    GET /
    Page d'accueil de l'API.
    """
    return jsonify({
        "projet"    : "Smart Santé 2035",
        "version"   : "1.0",
        "statut"    : "opérationnel",
        "endpoints" : {
            "POST /patients/admission"       : "Admettre un patient",
            "GET  /patients/<id>"            : "Obtenir un dossier",
            "GET  /triage/prochain"          : "Voir le patient suivant O(1)",
            "POST /triage/traiter"           : "Traiter le prochain O(log n)",
            "GET  /orientation/<id>/<source>": "Calculer orientation Dijkstra",
            "PUT  /etablissements/<id>/lits" : "Mettre à jour disponibilité",
            "GET  /demo"                     : "Démonstration complète",
        }
    })


# ── ROUTE 2 : Admettre un patient ────────────────────────────

@app.route("/patients/admission", methods=["POST"])
def admettre_patient():
    """
    POST /patients/admission

    Corps JSON attendu :
    {
      "nom"              : "Rakoto",
      "prenom"           : "Jean",
      "age"              : 45,
      "fc"               : 110,
      "spo2"             : 88.0,
      "temperature"      : 39.5,
      "fr"               : 24,
      "tension"          : "140/90",
      "score_symptomes"  : 60,
      "score_antecedents": 30
    }
    """
    donnees = request.get_json()

    if not donnees:
        return jsonify({"erreur": "Corps JSON manquant"}), 400

    # Vérification des champs obligatoires
    champs_requis = ["nom", "prenom", "age", "fc", "spo2",
                     "temperature", "fr", "tension"]
    for champ in champs_requis:
        if champ not in donnees:
            return jsonify({"erreur": f"Champ manquant : {champ}"}), 400

    # Créer les constantes vitales et calculer le score vital
    constantes = ConstantesVitales(
        patient_id             = "temp",
        frequence_cardiaque    = donnees["fc"],
        saturation_o2          = donnees["spo2"],
        temperature            = donnees["temperature"],
        frequence_respiratoire = donnees["fr"],
        tension_arterielle     = donnees["tension"]
    )
    score_vital = constantes.calculer_score_vital()

    # Créer le patient avec son score de triage
    patient = Patient(
        nom              = donnees["nom"],
        prenom           = donnees["prenom"],
        age              = donnees["age"],
        score_vital      = score_vital,
        score_symptomes  = donnees.get("score_symptomes", 50),
        score_antecedents= donnees.get("score_antecedents", 30)
    )

    # Insérer dans la file de triage (tas binaire) → O(log n)
    file_triage.inserer(patient)

    # Sauvegarder dans la table de hachage → O(1)
    dossiers_patients.inserer(patient.id_patient, patient)

    reponse = patient.to_dict()
    reponse["constantes"] = constantes.to_dict()
    reponse["patients_en_attente"] = file_triage.taille()
    reponse["message"] = "Patient admis et inséré dans la file de triage."

    code_http = 201
    return jsonify(reponse), code_http


# ── ROUTE 3 : Obtenir un dossier patient ─────────────────────

@app.route("/patients/<id_patient>", methods=["GET"])
def obtenir_patient(id_patient):
    """
    GET /patients/<id_patient>
    Recherche en O(1) via la table de hachage.
    """
    patient = dossiers_patients.rechercher(id_patient)

    if patient is None:
        return jsonify({"erreur": f"Patient non trouvé : {id_patient}"}), 404

    return jsonify(patient.to_dict()), 200


# ── ROUTE 4 : Consulter le prochain patient ──────────────────

@app.route("/triage/prochain", methods=["GET"])
def consulter_prochain():
    """
    GET /triage/prochain
    Retourne le patient le plus prioritaire SANS l'extraire.
    Complexité : O(1) — accès direct à la racine du tas
    """
    patient = file_triage.consulter_max()

    if patient is None:
        return jsonify({
            "statut"  : "vide",
            "message" : "Aucun patient en attente."
        }), 200

    reponse = patient.to_dict()
    reponse["patients_en_attente"] = file_triage.taille()
    reponse["complexite"] = "O(1) – racine du tas binaire"
    return jsonify(reponse), 200


# ── ROUTE 5 : Traiter le prochain patient ────────────────────

@app.route("/triage/traiter", methods=["POST"])
def traiter_prochain():
    """
    POST /triage/traiter
    Extrait le patient le plus prioritaire de la file.
    Complexité : O(log n) — sift-down après extraction
    """
    patient = file_triage.extraire_max()

    if patient is None:
        return jsonify({
            "statut"  : "vide",
            "message" : "File de triage vide."
        }), 200

    reponse = patient.to_dict()
    reponse["patients_restants"] = file_triage.taille()
    reponse["complexite"]        = "O(log n) – extraction tas binaire"
    reponse["message"]           = "Patient extrait de la file de triage."
    return jsonify(reponse), 200


# ── ROUTE 6 : Calculer l'orientation Dijkstra ────────────────

@app.route("/orientation/<id_patient>/<id_source>", methods=["GET"])
def calculer_orientation(id_patient, id_source):
    """
    GET /orientation/<id_patient>/<id_source>

    Exemple : GET /orientation/PAT-001/CSB-01

    Exécute l'algorithme de Dijkstra pour trouver le meilleur
    établissement de santé pour ce patient.
    """
    import time

    # Récupérer le patient
    patient = dossiers_patients.rechercher(id_patient)
    if patient is None:
        return jsonify({"erreur": f"Patient non trouvé : {id_patient}"}), 404

    # Vérifier que l'établissement source existe
    if id_source not in graphe.noeuds:
        return jsonify({"erreur": f"Établissement non trouvé : {id_source}"}), 404

    # Exécuter Dijkstra et mesurer le temps
    debut = time.time()
    resultat = graphe.dijkstra(id_source, patient)
    duree_ms = round((time.time() - debut) * 1000, 2)

    if resultat is None:
        return jsonify({
            "statut"  : "info",
            "message" : "Pas de transfert nécessaire ou aucun établissement compatible.",
        }), 200

    resultat["patient"]       = patient.to_dict()
    resultat["duree_calcul_ms"] = duree_ms
    resultat["complexite"]    = "O((V+E) × log V)"
    resultat["info_madagascar"] = "V≈3000 étab, E≈15000 routes → ≈207000 opérations"

    return jsonify(resultat), 200


# ── ROUTE 7 : Mettre à jour disponibilité établissement ──────

@app.route("/etablissements/<id_etab>/lits", methods=["PUT"])
def mettre_a_jour_lits(id_etab):
    """
    PUT /etablissements/<id_etab>/lits

    Corps JSON :
    { "lits_disponibles": 25 }
    """
    donnees = request.get_json()

    if not donnees or "lits_disponibles" not in donnees:
        return jsonify({"erreur": "Champ 'lits_disponibles' manquant"}), 400

    nouveaux_lits = donnees["lits_disponibles"]

    if nouveaux_lits < 0:
        return jsonify({"erreur": "Le nombre de lits ne peut pas être négatif"}), 400

    if id_etab not in graphe.noeuds:
        return jsonify({"erreur": f"Établissement non trouvé : {id_etab}"}), 404

    graphe.mettre_a_jour_lits(id_etab, nouveaux_lits)

    return jsonify({
        "statut"          : "succes",
        "id_etab"         : id_etab,
        "lits_disponibles": nouveaux_lits,
        "message"         : "Disponibilité mise à jour. Graphe recalculé."
    }), 200


# ── ROUTE 8 : Démonstration complète ─────────────────────────

@app.route("/demo", methods=["GET"])
def demonstration():
    """
    GET /demo
    Lance une démonstration complète des 3 algorithmes
    et retourne les résultats en JSON.
    """
    resultats = []

    # ── Démo 1 : Tas binaire ──────────────────────────────────
    demo_file = FilePrioriteTriageQ(capacite_max=10)

    patients_demo = [
        Patient("Rakoto", "Jean",  45, 20, 15, 10),  # Blessure légère
        Patient("Rabe",   "Marie", 72, 90, 88, 75),  # Crise cardiaque
        Patient("Rasoa",  "Paul",  30, 55, 60, 40),  # Fracture
        Patient("Rajao",  "Emma",   3, 70, 65, 20),  # Enfant fièvre
        Patient("Randria","Thomas",55, 35, 30, 25),  # Douleur modérée
    ]

    for p in patients_demo:
        demo_file.inserer(p)

    ordre_traitement = []
    while not demo_file.est_vide():
        p = demo_file.extraire_max()
        ordre_traitement.append({
            "id"     : p.id_patient,
            "nom"    : f"{p.prenom} {p.nom}",
            "score"  : p.score_triage,
            "couleur": p.couleur_priorite,
        })

    resultats.append({
        "algorithme"        : "Tas binaire (Binary Max-Heap)",
        "complexite_insert" : "O(log n)",
        "complexite_extract": "O(log n)",
        "avantage"          : "Le plus grave est TOUJOURS traité en premier",
        "ordre_traitement"  : ordre_traitement,
    })

    # ── Démo 2 : Dijkstra ────────────────────────────────────
    patient_urgent = Patient("Urgence", "Solo", 55, 92, 88, 70)
    resultat_dijkstra = graphe.dijkstra("CSB-01", patient_urgent)

    resultats.append({
        "algorithme"  : "Dijkstra (Plus court chemin)",
        "complexite"  : "O((V+E) × log V)",
        "pour_madagascar": "≈207 000 opérations → quelques millisecondes",
        "resultat"    : resultat_dijkstra,
    })

    # ── Démo 3 : Table de hachage ────────────────────────────
    table_demo = TableDeHachage()
    for p in patients_demo:
        table_demo.inserer(p.id_patient, p.nom)

    resultats.append({
        "algorithme"   : "Table de hachage",
        "complexite"   : "O(1) moyenne pour get/put/delete",
        "nb_elements"  : table_demo.nb_elements(),
        "facteur_charge": round(table_demo.facteur_charge(), 2),
        "avantage"     : "Accès instantané à n'importe quel dossier par son ID",
    })

    return jsonify({
        "projet"     : "Smart Santé 2035 – Démonstration algorithmique",
        "resultats"  : resultats,
    }), 200


# ── Lancement du serveur ──────────────────────────────────────

if __name__ == "__main__":
    print("\n╔══════════════════════════════════════════════╗")
    print("║    SMART SANTÉ 2035 – Serveur Flask          ║")
    print("║    API disponible sur http://localhost:5000   ║")
    print("╚══════════════════════════════════════════════╝\n")
    app.run(debug=True, port=5000)

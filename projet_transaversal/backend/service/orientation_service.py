# ============================================================
#  PROJET  : Smart Santé 2035
#  FICHIER : service/orientation_service.py
#  RÔLE    : Logique métier du Module d'Orientation (MOH).
#            Orchestre l'algorithme de Dijkstra.
#
#  FLUX :
#    app.py → OrientationService → GrapheHospitalier (Dijkstra)
#                                → EtablissementRepository
#  NIVEAU  : Licence 2 Informatique – GPI
# ============================================================

import time
from algorithme.graphe_hospitalier       import GrapheHospitalier, EtablissementSante, GOUDRON, PISTE
from repository.etablissement_repository import EtablissementRepository


class OrientationService:
    """Service métier pour l'orientation hospitalière (Module MOH)."""

    def __init__(self):
        self._graphe     = GrapheHospitalier()
        self._repository = EtablissementRepository()
        self._initialiser_graphe()

    # ── Calculer l'orientation optimale ──────────────────────

    def calculer_orientation(self, id_source, patient):
        """
        Exécute Dijkstra pour trouver le meilleur établissement.

        Étapes :
          1. Vérifier si l'établissement source peut traiter le patient
          2. Lancer Dijkstra sur le graphe → O((V+E) log V)
          3. Réserver un lit dans l'établissement cible
          4. Notifier l'établissement cible

        Retourne le résultat de Dijkstra ou None si pas de transfert.
        """
        # Étape 1 : L'établissement source peut-il traiter ce patient ?
        source = self._graphe.noeuds.get(id_source)
        if source and source.peut_accepter_patient(patient.niveau_priorite):
            return None  # Pas de transfert nécessaire

        # Étape 2 : Lancer Dijkstra
        debut   = time.time()
        resultat = self._graphe.dijkstra(id_source, patient)
        duree_ms = round((time.time() - debut) * 1000, 2)

        if resultat is None:
            return None

        # Étape 3 : Réserver un lit dans l'établissement cible
        id_cible = resultat["etablissement_cible"]["id_etab"]
        self._repository.mettre_a_jour_lits(
            id_cible,
            resultat["etablissement_cible"]["lits_disponibles"] - 1
        )
        self._graphe.mettre_a_jour_lits(
            id_cible,
            resultat["etablissement_cible"]["lits_disponibles"] - 1
        )

        # Ajouter les métadonnées de performance
        resultat["duree_calcul_ms"] = duree_ms
        resultat["complexite"]      = "O((V+E) × log V)"

        # Étape 4 : Notifier
        self._notifier_etablissement(resultat)

        return resultat

    # ── Mettre à jour disponibilité ───────────────────────────

    def mettre_a_jour_disponibilite(self, id_etab, nouveaux_lits):
        """
        Met à jour les lits d'un établissement dans le repo ET le graphe.
        Les prochains appels à Dijkstra utiliseront les nouvelles données.
        """
        ok_repo  = self._repository.mettre_a_jour_lits(id_etab, nouveaux_lits)
        if ok_repo:
            self._graphe.mettre_a_jour_lits(id_etab, nouveaux_lits)
        return ok_repo

    def obtenir_etablissement(self, id_etab):
        return self._repository.trouver_par_id(id_etab)

    def lister_etablissements(self):
        return self._repository.trouver_tous()

    def nb_etablissements(self):
        return self._repository.compter()

    # ── Initialisation du graphe ──────────────────────────────

    def _initialiser_graphe(self):
        """Charge les établissements et routes dans le graphe."""
        etabs = [
            EtablissementSante("CSB-01",   "CSB Manakambahiny",          EtablissementSante.CSB_II,       -18.91, 47.53, 20,  15),
            EtablissementSante("HOP-DIS",  "Hôpital District Anta.",      EtablissementSante.HOPITAL_DIS,  -18.92, 47.51, 80,  12),
            EtablissementSante("HOP-REF",  "Hôpital Référence Analakely", EtablissementSante.HOP_REF_REG,  -18.90, 47.52, 200, 35),
            EtablissementSante("CHUR-ANT", "CHUR Antananarivo",           EtablissementSante.CHUR,         -18.89, 47.50, 500, 60),
            EtablissementSante("HOP-SAT",  "Hôpital Saturé",              EtablissementSante.HOPITAL_DIS,  -18.91, 47.55, 60,   0),
        ]
        for e in etabs:
            self._graphe.ajouter_noeud(e)
            self._repository.sauvegarder(e)

        self._graphe.ajouter_arc("CSB-01",  "HOP-DIS",   8.5,  25, GOUDRON, True)
        self._graphe.ajouter_arc("CSB-01",  "HOP-SAT",   3.0,  10, GOUDRON, False)
        self._graphe.ajouter_arc("CSB-01",  "HOP-REF",  15.0,  40, PISTE,   False)
        self._graphe.ajouter_arc("HOP-DIS", "HOP-REF",   7.0,  20, GOUDRON, True)
        self._graphe.ajouter_arc("HOP-DIS", "CHUR-ANT", 12.0,  30, GOUDRON, True)
        self._graphe.ajouter_arc("HOP-REF", "CHUR-ANT",  5.0,  15, GOUDRON, True)
        self._graphe.ajouter_arc("HOP-SAT", "HOP-DIS",   6.0,  18, GOUDRON, False)

    def _notifier_etablissement(self, resultat):
        print(f"\n📡 Notification → {resultat['etablissement_cible']['nom']}")
        print(f"   Arrivée dans : {resultat['temps_minutes']} min")

# ============================================================
#  PROJET  : Smart Santé 2035
#  FICHIER : repository/patient_repository.py
#  RÔLE    : Couche d'accès aux données pour les patients.
#            Fait le lien entre les services et la base de données.
#
#  PATTERN : Repository Pattern
#    Les services ne savent pas comment les données sont stockées.
#    Ils appellent le repository qui gère la persistance.
#
#  NIVEAU  : Licence 2 Informatique – GPI
# ============================================================


class PatientRepository:
    """
    Gère la persistance des données patients.
    Simulation en mémoire (en production : PostgreSQL via psycopg2).
    """

    def __init__(self):
        # Stockage en mémoire : dict { id_patient → Patient }
        # En production : remplacé par des requêtes SQL
        self._stockage  = {}
        self._compteur  = 1

    # ── CREATE ────────────────────────────────────────────────

    def sauvegarder(self, patient):
        """
        Sauvegarde un patient (INSERT ou UPDATE).
        Équivalent SQL :
          INSERT INTO patients ... ON CONFLICT(id) DO UPDATE SET ...

        Complexité : O(1) — accès direct au dictionnaire
        """
        self._stockage[patient.id_patient] = patient
        print(f"💾 [PatientRepository] Sauvegardé : {patient.id_patient}")
        return patient

    # ── READ ──────────────────────────────────────────────────

    def trouver_par_id(self, id_patient):
        """
        Recherche un patient par son identifiant.
        Équivalent SQL : SELECT * FROM patients WHERE id = %s

        Complexité : O(1)
        """
        return self._stockage.get(id_patient, None)

    def trouver_tous(self):
        """
        Retourne tous les patients.
        Équivalent SQL : SELECT * FROM patients
        """
        return list(self._stockage.values())

    def trouver_par_niveau(self, niveau):
        """
        Retourne les patients d'un niveau de priorité donné.
        Équivalent SQL :
          SELECT * FROM patients WHERE niveau_priorite = %s
          ORDER BY timestamp_admission ASC
        """
        resultat = [
            p for p in self._stockage.values()
            if p.niveau_priorite == niveau
        ]
        # Trier par heure d'arrivée
        resultat.sort(key=lambda p: p.timestamp_admission)
        return resultat

    def trouver_critiques(self):
        """
        Retourne les patients de niveau 1 ou 2 (Rouge/Orange).
        Équivalent SQL :
          SELECT * FROM patients WHERE niveau_priorite <= 2
        """
        return [
            p for p in self._stockage.values()
            if p.niveau_priorite <= 2
        ]

    def existe(self, id_patient):
        """
        Vérifie si un patient existe.
        Équivalent SQL : SELECT EXISTS(SELECT 1 FROM patients WHERE id = %s)
        """
        return id_patient in self._stockage

    def compter(self):
        """
        Compte le nombre total de patients.
        Équivalent SQL : SELECT COUNT(*) FROM patients
        """
        return len(self._stockage)

    # ── DELETE ────────────────────────────────────────────────

    def supprimer(self, id_patient):
        """
        Supprime un patient (quand il quitte l'hôpital).
        Équivalent SQL : DELETE FROM patients WHERE id = %s
        """
        if id_patient in self._stockage:
            del self._stockage[id_patient]
            print(f"🗑 [PatientRepository] Supprimé : {id_patient}")
            return True
        return False

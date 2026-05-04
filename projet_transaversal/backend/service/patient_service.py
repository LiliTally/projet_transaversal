# ============================================================
#  PROJET  : Smart Santé 2035
#  FICHIER : service/patient_service.py
#  RÔLE    : Logique métier pour la gestion des dossiers patients.
#  NIVEAU  : Licence 2 Informatique – GPI
# ============================================================

from repository.patient_repository import PatientRepository


class PatientService:
    """Service métier pour la gestion des dossiers patients."""

    def __init__(self):
        self._repository = PatientRepository()

    def enregistrer(self, patient):
        """Enregistre un patient après validation."""
        if not patient.nom or not patient.prenom:
            raise ValueError("Nom et prénom obligatoires.")
        return self._repository.sauvegarder(patient)

    def obtenir(self, id_patient):
        """Obtient un patient par son ID."""
        p = self._repository.trouver_par_id(id_patient)
        if not p:
            raise ValueError(f"Patient non trouvé : {id_patient}")
        return p

    def lister_tous(self):
        """Liste tous les patients enregistrés."""
        return self._repository.trouver_tous()

    def lister_par_priorite(self, niveau):
        """Liste les patients d'un niveau de priorité donné (1 à 5)."""
        if niveau not in range(1, 6):
            raise ValueError("Niveau doit être entre 1 et 5.")
        return self._repository.trouver_par_niveau(niveau)

    def lister_critiques(self):
        """Liste les patients de niveau 1 ou 2 (Rouge/Orange)."""
        return self._repository.trouver_critiques()

    def marquer_pris_en_charge(self, id_patient):
        """Marque un patient comme pris en charge (le retire du système)."""
        return self._repository.supprimer(id_patient)

    def statistiques(self):
        """Retourne les statistiques globales des patients."""
        total     = self._repository.compter()
        critiques = len(self._repository.trouver_critiques())
        return {
            "total"         : total,
            "critiques_rouge": len(self._repository.trouver_par_niveau(1)),
            "urgents_orange" : len(self._repository.trouver_par_niveau(2)),
            "semi_urgents"   : len(self._repository.trouver_par_niveau(3)),
            "non_urgents"    : total - critiques,
        }

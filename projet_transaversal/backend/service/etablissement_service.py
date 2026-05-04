# ============================================================
#  PROJET  : Smart Santé 2035
#  FICHIER : service/etablissement_service.py
#  RÔLE    : Logique métier pour la gestion des établissements.
#  NIVEAU  : Licence 2 Informatique – GPI
# ============================================================

from repository.etablissement_repository import EtablissementRepository


class EtablissementService:
    """Service métier pour la gestion des établissements de santé."""

    def __init__(self):
        self._repository = EtablissementRepository()

    def sauvegarder(self, etab):
        """Sauvegarde ou met à jour un établissement."""
        return self._repository.sauvegarder(etab)

    def obtenir(self, id_etab):
        """Obtient un établissement par son ID."""
        e = self._repository.trouver_par_id(id_etab)
        if not e:
            raise ValueError(f"Établissement non trouvé : {id_etab}")
        return e

    def lister_tous(self):
        """Liste tous les établissements."""
        return self._repository.trouver_tous()

    def lister_disponibles(self):
        """Liste les établissements avec des lits disponibles."""
        return self._repository.trouver_avec_lits_dispo()

    def mettre_a_jour_lits(self, id_etab, nouveaux_lits):
        """Met à jour le nombre de lits disponibles."""
        if nouveaux_lits < 0:
            raise ValueError("Le nombre de lits ne peut pas être négatif.")
        return self._repository.mettre_a_jour_lits(id_etab, nouveaux_lits)

    def statistiques(self):
        """Retourne les statistiques globales du réseau hospitalier."""
        tous        = self._repository.trouver_tous()
        disponibles = self._repository.trouver_avec_lits_dispo()
        return {
            "total_etablissements"     : len(tous),
            "etablissements_disponibles": len(disponibles),
            "total_lits_dispo"         : sum(e.lits_disponibles for e in tous),
            "total_lits"               : sum(e.capacite_totale  for e in tous),
        }

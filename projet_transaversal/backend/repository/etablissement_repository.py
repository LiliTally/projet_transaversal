# ============================================================
#  PROJET  : Smart Santé 2035
#  FICHIER : repository/etablissement_repository.py
#  RÔLE    : Couche d'accès aux données pour les établissements.
#  NIVEAU  : Licence 2 Informatique – GPI
# ============================================================


class EtablissementRepository:
    """
    Gère la persistance des données des établissements de santé.
    Simulation en mémoire (en production : PostgreSQL).
    """

    def __init__(self):
        self._stockage = {}  # { id_etab → EtablissementSante }

    # ── CREATE / UPDATE ───────────────────────────────────────

    def sauvegarder(self, etab):
        """
        Sauvegarde ou met à jour un établissement.
        Équivalent SQL : INSERT INTO etablissements ... ON CONFLICT DO UPDATE
        """
        self._stockage[etab.id_etab] = etab
        print(f"💾 [EtablissementRepository] Sauvegardé : {etab.nom}")
        return etab

    # ── READ ──────────────────────────────────────────────────

    def trouver_par_id(self, id_etab):
        """
        Recherche un établissement par son ID.
        Équivalent SQL : SELECT * FROM etablissements WHERE id = %s
        Complexité : O(1)
        """
        return self._stockage.get(id_etab, None)

    def trouver_tous(self):
        """Retourne tous les établissements."""
        return list(self._stockage.values())

    def trouver_operationnels(self):
        """
        Retourne uniquement les établissements opérationnels.
        Équivalent SQL :
          SELECT * FROM etablissements WHERE est_operationnel = TRUE
        """
        return [e for e in self._stockage.values() if e.est_operationnel]

    def trouver_avec_lits_dispo(self):
        """
        Retourne les établissements avec des lits disponibles.
        Équivalent SQL :
          SELECT * FROM etablissements
          WHERE lits_disponibles > 0 AND est_operationnel = TRUE
        """
        return [
            e for e in self._stockage.values()
            if e.lits_disponibles > 0 and e.est_operationnel
        ]

    def trouver_par_niveau_min(self, niveau_min):
        """
        Retourne les établissements de niveau >= niveau_min.
        Utilisé par Dijkstra pour filtrer les destinations.
        Équivalent SQL :
          SELECT * FROM etablissements WHERE niveau_soins >= %s
        """
        return [
            e for e in self._stockage.values()
            if e.niveau_soins >= niveau_min and e.est_operationnel
        ]

    def existe(self, id_etab):
        """Vérifie si un établissement existe."""
        return id_etab in self._stockage

    def compter(self):
        """Compte le nombre d'établissements."""
        return len(self._stockage)

    # ── UPDATE ────────────────────────────────────────────────

    def mettre_a_jour_lits(self, id_etab, nouveaux_lits):
        """
        Met à jour le nombre de lits disponibles.
        Équivalent SQL :
          UPDATE etablissements SET lits_disponibles = %s WHERE id = %s
        """
        etab = self._stockage.get(id_etab)
        if etab:
            etab.lits_disponibles = nouveaux_lits
            print(f"🔄 [EtablissementRepository] "
                  f"{etab.nom} → {nouveaux_lits} lits")
            return True
        return False

# ============================================================
#  PROJET  : Smart Santé 2035
#  FICHIER : model/enums/niveau_priorite.py
#  RÔLE    : Les 5 niveaux de priorité médicale du triage.
#            Inspiré du Manchester Triage System (MTS).
#  NIVEAU  : Licence 2 Informatique – GPI
# ============================================================

from enum import Enum

class NiveauPriorite(Enum):
    """
    Les 5 niveaux de priorité médicale.
    Valeur = (numéro, couleur, description, délai_max_minutes)
    """
    ROUGE  = (1, "ROUGE",  "Critique – immédiat",       0)
    ORANGE = (2, "ORANGE", "Très urgent – 15 min",      15)
    JAUNE  = (3, "JAUNE",  "Urgent – 30 min",           30)
    VERT   = (4, "VERT",   "Non urgent – 1 heure",      60)
    BLEU   = (5, "BLEU",   "Peut attendre – 2 heures", 120)

    def __init__(self, numero, couleur, description, delai_max):
        self.numero      = numero
        self.couleur     = couleur
        self.description = description
        self.delai_max   = delai_max

    @staticmethod
    def depuis_score(score):
        """
        Retourne le niveau correspondant à un score de triage.
        Complexité : O(1)
        """
        if score >= 80: return NiveauPriorite.ROUGE
        if score >= 60: return NiveauPriorite.ORANGE
        if score >= 40: return NiveauPriorite.JAUNE
        if score >= 20: return NiveauPriorite.VERT
        return NiveauPriorite.BLEU

    @property
    def necessite_alerte(self):
        """Retourne True si ce niveau déclenche une alerte immédiate."""
        return self in (NiveauPriorite.ROUGE, NiveauPriorite.ORANGE)

    def to_dict(self):
        return {
            "numero"     : self.numero,
            "couleur"    : self.couleur,
            "description": self.description,
            "delai_max"  : self.delai_max,
        }

    def __str__(self):
        return f"Niveau {self.numero} – {self.couleur} ({self.description})"

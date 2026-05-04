# ============================================================
#  PROJET  : Smart Santé 2035
#  FICHIER : model/enums/etat_route.py
#  RÔLE    : État des routes utilisé dans le graphe hospitalier.
#  NIVEAU  : Licence 2 Informatique – GPI
# ============================================================

from enum import Enum

class EtatRoute(Enum):
    """État d'une route entre deux établissements de santé."""
    GOUDRON      = ("goudron",      1.0,          "Route asphaltée, praticable toute l'année")
    PISTE        = ("piste",        1.8,          "Piste en latérite, difficile en saison des pluies")
    IMPRATICABLE = ("impraticable", float('inf'), "Route fermée – impraticable")

    def __init__(self, code, facteur, description):
        self.code        = code
        self.facteur     = facteur   # Facteur multiplicateur sur le temps de trajet
        self.description = description

    @property
    def est_praticable(self):
        return self != EtatRoute.IMPRATICABLE

    def __str__(self):
        return f"{self.code} (facteur×{self.facteur})"

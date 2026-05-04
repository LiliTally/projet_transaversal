# ============================================================
#  PROJET  : Smart Santé 2035
#  FICHIER : model/enums/niveau_soins.py
#  RÔLE    : Niveaux de la pyramide sanitaire malgache.
#  NIVEAU  : Licence 2 Informatique – GPI
# ============================================================

from enum import Enum

class NiveauSoins(Enum):
    """
    Les 5 niveaux de la pyramide sanitaire malgache.
    Du plus bas (CSB I) au plus élevé (CHUR).
    """
    CSB_I       = (1, "CSB I",       "Centre de Santé de Base niveau 1")
    CSB_II      = (2, "CSB II",      "Centre de Santé de Base niveau 2")
    HOPITAL_DIS = (3, "Hôpital Dist","Hôpital de District")
    HOP_REF_REG = (4, "Hôp. Réf.",  "Hôpital de Référence Régionale")
    CHUR        = (5, "CHUR",        "Centre Hospitalier Universitaire Régional")

    def __init__(self, numero, sigle, description):
        self.numero      = numero
        self.sigle       = sigle
        self.description = description

    def peut_traiter_niveau(self, niveau_priorite):
        """
        Vérifie si cet établissement peut traiter un patient
        du niveau de priorité donné.
        """
        if niveau_priorite == 1 and self.numero < 3: return False
        if niveau_priorite == 2 and self.numero < 2: return False
        return True

    def __str__(self):
        return f"{self.sigle} – {self.description}"

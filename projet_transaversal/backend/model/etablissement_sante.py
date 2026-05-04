# ============================================================
#  PROJET  : Smart Santé 2035
#  FICHIER : model/etablissement_sante.py
#  RÔLE    : Modèle d'un établissement de santé.
#            Représente un nœud dans le graphe hospitalier.
#  NIVEAU  : Licence 2 Informatique – GPI
# ============================================================

class EtablissementSante:
    """
    Un établissement de santé dans le réseau hospitalier malgache.
    Chaque établissement est un nœud du graphe utilisé par Dijkstra.
    """

    # Niveaux de soins (pyramide sanitaire malgache)
    CSB_I       = 1
    CSB_II      = 2
    HOPITAL_DIS = 3
    HOP_REF_REG = 4
    CHUR        = 5

    def __init__(self, id_etab, nom, niveau_soins,
                 latitude, longitude,
                 capacite_totale, lits_disponibles,
                 specialites=None):
        """
        Paramètres :
            id_etab          : identifiant unique (ex: "CHUR-ANT")
            nom              : nom complet de l'établissement
            niveau_soins     : 1 à 5 (CSB I → CHUR)
            latitude         : coordonnée GPS latitude
            longitude        : coordonnée GPS longitude
            capacite_totale  : nombre total de lits
            lits_disponibles : nombre de lits libres en ce moment
            specialites      : liste des spécialités disponibles
        """
        self.id_etab          = id_etab
        self.nom              = nom
        self.niveau_soins     = niveau_soins
        self.latitude         = latitude
        self.longitude        = longitude
        self.capacite_totale  = capacite_totale
        self.lits_disponibles = lits_disponibles
        self.specialites      = specialites or []
        self.est_operationnel = True

    # ── Méthodes ──────────────────────────────────────────────

    def taux_occupation(self):
        """
        Calcule le taux d'occupation entre 0.0 (vide) et 1.0 (plein).
        Utilisé par Dijkstra pour pondérer les arcs.
        """
        if self.capacite_totale == 0:
            return 1.0
        return 1.0 - (self.lits_disponibles / self.capacite_totale)

    def peut_accepter_patient(self, niveau_priorite):
        """
        Vérifie si l'établissement peut accueillir ce patient.

        Règles :
          - Doit être opérationnel
          - Doit avoir des lits disponibles
          - Niveau de soins compatible avec la gravité du patient
        """
        if not self.est_operationnel:      return False
        if self.lits_disponibles <= 0:     return False
        if niveau_priorite == 1 and self.niveau_soins < 3: return False
        if niveau_priorite == 2 and self.niveau_soins < 2: return False
        return True

    def reserver_lit(self):
        """Réserve un lit pour un patient entrant."""
        if self.lits_disponibles > 0:
            self.lits_disponibles -= 1
            return True
        return False

    def liberer_lit(self):
        """Libère un lit quand un patient sort."""
        if self.lits_disponibles < self.capacite_totale:
            self.lits_disponibles += 1

    def to_dict(self):
        """Convertit en dictionnaire pour la réponse JSON."""
        return {
            "id_etab"          : self.id_etab,
            "nom"              : self.nom,
            "niveau_soins"     : self.niveau_soins,
            "latitude"         : self.latitude,
            "longitude"        : self.longitude,
            "capacite_totale"  : self.capacite_totale,
            "lits_disponibles" : self.lits_disponibles,
            "taux_occupation"  : f"{self.taux_occupation()*100:.0f}%",
            "specialites"      : self.specialites,
            "est_operationnel" : self.est_operationnel,
        }

    def __str__(self):
        return (f"[{self.id_etab}] {self.nom} | "
                f"Niveau:{self.niveau_soins} | "
                f"Lits:{self.lits_disponibles}/{self.capacite_totale} | "
                f"{self.taux_occupation()*100:.0f}% occupé")

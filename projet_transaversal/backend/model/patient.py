# ============================================================
#  PROJET  : Smart Santé 2035
#  FICHIER : model/patient.py
#  RÔLE    : Représente un patient admis dans le système.
#            Calcule automatiquement le score de triage
#            à partir des constantes vitales.
#  NIVEAU  : Licence 2 Informatique – GPI
# ============================================================

import time
import uuid


class Patient:
    """
    Un patient admis dans le système de triage.

    Le score de triage est calculé selon la formule :
      S = 0.45 × vital + 0.30 × symptômes + 0.15 × antécédents + 0.10 × âge

    Plus le score est élevé → plus le patient est grave → priorité haute.
    """

    # Niveaux de priorité (inspiré du Manchester Triage System)
    NIVEAUX = {
        1: ("ROUGE",  "Critique – immédiat",      0),
        2: ("ORANGE", "Très urgent – 15 min",     15),
        3: ("JAUNE",  "Urgent – 30 min",          30),
        4: ("VERT",   "Non urgent – 1h",          60),
        5: ("BLEU",   "Peut attendre – 2h",      120),
    }

    def __init__(self, nom, prenom, age,
                 score_vital, score_symptomes, score_antecedents,
                 id_patient=None):
        """
        Crée un nouveau patient et calcule son score de triage.

        Paramètres :
            nom               : nom de famille
            prenom            : prénom
            age               : âge en années
            score_vital       : score des constantes vitales (0-100)
            score_symptomes   : score des symptômes déclarés (0-100)
            score_antecedents : score des antécédents médicaux (0-100)
            id_patient        : ID unique (généré automatiquement si None)
        """
        # Identifiant unique
        self.id_patient = id_patient or f"PAT-{str(uuid.uuid4())[:8].upper()}"

        # Données démographiques
        self.nom    = nom
        self.prenom = prenom
        self.age    = age

        # Heure d'arrivée (pour départager les égalités de score)
        self.timestamp_admission = time.time()

        # Calcul du score composite pondéré
        self.score_triage = self._calculer_score_composite(
            score_vital, score_symptomes, score_antecedents, age
        )

        # Niveau de priorité déduit du score
        self.niveau_priorite = self._determiner_niveau(self.score_triage)

    # ── Méthodes de calcul ────────────────────────────────────

    def _calculer_score_composite(self, vital, symptomes, antecedents, age):
        """
        Formule pondérée :
          S = 0.45×vital + 0.30×symptômes + 0.15×antécédents + 0.10×scoreAge

        Complexité : O(1)
        """
        # Score lié à l'âge (enfants < 5 ans et adultes > 70 = plus vulnérables)
        if age < 5 or age > 70:
            score_age = 80.0   # Vulnérabilité élevée
        elif age < 15 or age > 60:
            score_age = 50.0   # Vulnérabilité modérée
        else:
            score_age = 20.0   # Adulte en âge normal

        score = (0.45 * vital
               + 0.30 * symptomes
               + 0.15 * antecedents
               + 0.10 * score_age)

        # On s'assure que le score reste entre 0 et 100
        return min(100.0, max(0.0, score))

    def _determiner_niveau(self, score):
        """
        Détermine le niveau de priorité (1 à 5) selon le score.
        Complexité : O(1)
        """
        if score >= 80: return 1   # ROUGE
        if score >= 60: return 2   # ORANGE
        if score >= 40: return 3   # JAUNE
        if score >= 20: return 4   # VERT
        return 5                   # BLEU

    def est_prioritaire_sur(self, autre_patient):
        """
        Vérifie si ce patient est plus prioritaire qu'un autre.
        Utilisé par le tas binaire pour comparer deux patients.

        En cas d'égalité de score → le premier arrivé est prioritaire.

        Retourne True si ce patient doit être traité AVANT l'autre.
        """
        if self.score_triage != autre_patient.score_triage:
            return self.score_triage > autre_patient.score_triage
        # Égalité → le plus ancien dans la file est prioritaire (FIFO de secours)
        return self.timestamp_admission < autre_patient.timestamp_admission

    # ── Propriétés utiles ─────────────────────────────────────

    @property
    def couleur_priorite(self):
        """Retourne la couleur et description du niveau de priorité."""
        couleur, description, _ = self.NIVEAUX[self.niveau_priorite]
        return f"{couleur} – {description}"

    @property
    def est_critique(self):
        """Retourne True si le patient est de niveau 1 ou 2."""
        return self.niveau_priorite <= 2

    def to_dict(self):
        """Convertit le patient en dictionnaire pour la réponse JSON."""
        couleur, description, delai = self.NIVEAUX[self.niveau_priorite]
        return {
            "id_patient"       : self.id_patient,
            "nom"              : self.nom,
            "prenom"           : self.prenom,
            "age"              : self.age,
            "score_triage"     : round(self.score_triage, 2),
            "niveau_priorite"  : self.niveau_priorite,
            "couleur"          : couleur,
            "description"      : description,
            "delai_max_minutes": delai,
            "alerte_requise"   : self.est_critique,
        }

    def __str__(self):
        return (f"[{self.id_patient}] {self.prenom} {self.nom} "
                f"| Score: {self.score_triage:.1f} "
                f"| Priorité: {self.couleur_priorite}")

    def __repr__(self):
        return self.__str__()

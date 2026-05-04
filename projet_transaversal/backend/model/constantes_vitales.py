# ============================================================
#  PROJET  : Smart Santé 2035
#  FICHIER : model/constantes_vitales.py
#  RÔLE    : Stocke les mesures médicales d'un patient et
#            calcule automatiquement le score vital.
#  NIVEAU  : Licence 2 Informatique – GPI
# ============================================================

import time
import uuid


class ConstantesVitales:
    """
    Mesures médicales d'un patient prises à l'admission.

    Ces mesures sont utilisées par le MTI pour calculer
    le score de triage composite.
    """

    def __init__(self, patient_id,
                 frequence_cardiaque,   # battements/min  (normal: 60-100)
                 saturation_o2,         # pourcentage     (normal: 95-100)
                 temperature,           # degrés Celsius  (normal: 36.5-37.5)
                 frequence_respiratoire,# respirations/min(normal: 12-20)
                 tension_arterielle):   # ex: "120/80"
        """
        Paramètres :
            patient_id             : ID du patient associé
            frequence_cardiaque    : fréquence cardiaque en bpm
            saturation_o2          : saturation en oxygène en %
            temperature            : température corporelle en °C
            frequence_respiratoire : fréquence respiratoire par minute
            tension_arterielle     : tension artérielle (ex: "120/80")
        """
        self.id_constantes          = str(uuid.uuid4())[:8].upper()
        self.patient_id             = patient_id
        self.frequence_cardiaque    = frequence_cardiaque
        self.saturation_o2          = saturation_o2
        self.temperature            = temperature
        self.frequence_respiratoire = frequence_respiratoire
        self.tension_arterielle     = tension_arterielle
        self.timestamp_mesure       = time.time()

    # ── Méthodes de calcul ────────────────────────────────────

    def calculer_score_vital(self):
        """
        Calcule un score vital entre 0 et 100.
        Chaque constante hors des valeurs normales augmente le score.
        Plus le score est élevé → état plus grave.

        Complexité : O(1)
        """
        score = 0.0

        # ── Fréquence cardiaque ────────────────────────────────
        fc = self.frequence_cardiaque
        if fc < 40 or fc > 150:   score += 30   # Très anormal
        elif fc < 50 or fc > 120: score += 15   # Anormal
        elif fc < 60 or fc > 100: score +=  5   # Légèrement hors normes

        # ── Saturation en oxygène ──────────────────────────────
        spo2 = self.saturation_o2
        if spo2 < 85:   score += 35   # Hypoxie sévère → très grave
        elif spo2 < 90: score += 25   # Hypoxie modérée
        elif spo2 < 95: score += 10   # Légèrement bas

        # ── Température ───────────────────────────────────────
        temp = self.temperature
        if temp > 40.0 or temp < 35.0:   score += 20
        elif temp > 39.0 or temp < 36.0: score += 10

        # ── Fréquence respiratoire ─────────────────────────────
        fr = self.frequence_respiratoire
        if fr < 8 or fr > 30:    score += 15
        elif fr < 12 or fr > 20: score +=  5

        return min(100.0, score)

    def est_critique(self):
        """
        Retourne True si au moins une constante est en zone dangereuse.
        Déclenche une alerte immédiate si True.
        """
        return (
            self.saturation_o2 < 90
            or self.frequence_cardiaque < 40
            or self.frequence_cardiaque > 150
            or self.temperature > 40.5
            or self.temperature < 34.5
            or self.frequence_respiratoire < 8
            or self.frequence_respiratoire > 35
        )

    def to_dict(self):
        """Convertit les constantes en dictionnaire pour JSON."""
        return {
            "id_constantes"          : self.id_constantes,
            "patient_id"             : self.patient_id,
            "frequence_cardiaque"    : self.frequence_cardiaque,
            "saturation_o2"          : self.saturation_o2,
            "temperature"            : self.temperature,
            "frequence_respiratoire" : self.frequence_respiratoire,
            "tension_arterielle"     : self.tension_arterielle,
            "score_vital_calcule"    : round(self.calculer_score_vital(), 2),
            "etat_critique"          : self.est_critique(),
        }

    def __str__(self):
        return (f"FC:{self.frequence_cardiaque}bpm | "
                f"SpO2:{self.saturation_o2}% | "
                f"Temp:{self.temperature}°C | "
                f"FR:{self.frequence_respiratoire}/min | "
                f"Score vital:{self.calculer_score_vital():.1f} | "
                f"Critique:{'OUI ⚠' if self.est_critique() else 'non'}")

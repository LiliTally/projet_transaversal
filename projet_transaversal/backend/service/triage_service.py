# ============================================================
#  PROJET  : Smart Santé 2035
#  FICHIER : service/triage_service.py
#  RÔLE    : Logique métier du Module de Triage Intelligent (MTI).
#            Coordonne le tas binaire et le repository patients.
#
#  FLUX :
#    app.py → TriageService → FilePrioriteTriageQ
#                           → PatientRepository
#  NIVEAU  : Licence 2 Informatique – GPI
# ============================================================

from algorithme.file_priorite    import FilePrioriteTriageQ
from repository.patient_repository import PatientRepository
from model.patient               import Patient


class TriageService:
    """Service métier pour le triage médical (Module MTI)."""

    def __init__(self, capacite_max=500):
        # Tas binaire : algorithme central du triage
        self._file      = FilePrioriteTriageQ(capacite_max)
        self._repository = PatientRepository()

    # ── Admettre un patient ───────────────────────────────────

    def admettre_patient(self, nom, prenom, age,
                          score_vital, score_symptomes, score_antecedents):
        """
        Admet un patient dans le système de triage.

        Étapes :
          1. Créer l'objet Patient avec son score de triage
          2. Insérer dans le tas binaire → O(log n)
          3. Sauvegarder en base de données → O(1)
          4. Envoyer une alerte si cas critique (niveau 1 ou 2)

        Retourne le patient créé avec son niveau de priorité.
        """
        # Étape 1 : Créer le patient
        patient = Patient(nom, prenom, age,
                          score_vital, score_symptomes, score_antecedents)

        # Étape 2 : Insérer dans le tas binaire → O(log n)
        self._file.inserer(patient)

        # Étape 3 : Sauvegarder en base → O(1)
        self._repository.sauvegarder(patient)

        # Étape 4 : Alerte si critique
        if patient.est_critique:
            self._envoyer_alerte(patient)

        return patient

    # ── Traiter le prochain patient ───────────────────────────

    def traiter_prochain(self):
        """
        Extrait le patient le plus prioritaire de la file.
        Opération extraire_max() du tas binaire → O(log n)
        """
        return self._file.extraire_max()

    # ── Consulter sans extraire ───────────────────────────────

    def consulter_prochain(self):
        """
        Retourne le patient le plus prioritaire SANS l'extraire.
        Complexité : O(1) — accès direct à la racine du tas
        """
        return self._file.consulter_max()

    # ── Réévaluer un patient ──────────────────────────────────

    def reevaluer_patient(self, id_patient,
                           nouveau_vital, nouveau_symptomes, nouveau_antecedents):
        """
        Réévalue un patient dont l'état a changé.
        Recalcule son score et le réinsère dans la file.
        """
        ancien = self._repository.trouver_par_id(id_patient)
        if not ancien:
            return None

        # Créer un nouveau patient avec les nouveaux scores
        nouveau = Patient(
            ancien.nom, ancien.prenom, ancien.age,
            nouveau_vital, nouveau_symptomes, nouveau_antecedents,
            id_patient=id_patient
        )

        # Réinsérer dans la file
        self._file.inserer(nouveau)
        self._repository.sauvegarder(nouveau)

        # Alerte si aggravation
        if nouveau.est_critique and not ancien.est_critique:
            print(f"⚠ AGGRAVATION : {nouveau.prenom} {nouveau.nom}")
            self._envoyer_alerte(nouveau)

        return nouveau

    # ── Statistiques ──────────────────────────────────────────

    def nb_patients_en_attente(self):
        return self._file.taille()

    def patients_critiques(self):
        return self._repository.trouver_critiques()

    def afficher_file(self):
        self._file.afficher_file()

    # ── Privé ─────────────────────────────────────────────────

    def _envoyer_alerte(self, patient):
        """
        Envoie une alerte pour un patient critique.
        En production : notification push, SMS, alarme sonore.
        """
        print(f"\n🚨 ALERTE {patient.couleur_priorite}")
        print(f"   Patient : {patient.prenom} {patient.nom}")
        print(f"   Score   : {patient.score_triage:.1f}\n")

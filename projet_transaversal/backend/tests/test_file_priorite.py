# ============================================================
#  PROJET  : Smart Santé 2035
#  FICHIER : tests/test_file_priorite.py
#  RÔLE    : Tests unitaires du tas binaire (FilePrioriteTriageQ).
#  USAGE   : python -m pytest tests/ -v
#  NIVEAU  : Licence 2 Informatique – GPI
# ============================================================

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from algorithme.file_priorite import FilePrioriteTriageQ
from model.patient             import Patient


def creer_patient(nom, vital, symptomes=50, antecedents=30, age=35):
    return Patient(nom, "Test", age, vital, symptomes, antecedents)


class TestFilePriorite:

    def setup_method(self):
        """Crée une nouvelle file avant chaque test."""
        self.file = FilePrioriteTriageQ(capacite_max=10)

    # ── Tests d'insertion ─────────────────────────────────────

    def test_inserer_un_patient(self):
        p = creer_patient("Rakoto", 50)
        self.file.inserer(p)
        assert self.file.taille() == 1

    def test_inserer_plusieurs_patients(self):
        for i in range(5):
            self.file.inserer(creer_patient(f"Patient{i}", i * 10))
        assert self.file.taille() == 5

    def test_file_pleine(self):
        file_petite = FilePrioriteTriageQ(capacite_max=2)
        file_petite.inserer(creer_patient("P1", 50))
        file_petite.inserer(creer_patient("P2", 60))
        resultat = file_petite.inserer(creer_patient("P3", 70))
        assert resultat == False   # Ne peut pas insérer

    # ── Tests d'extraction ────────────────────────────────────

    def test_extraire_max_ordre_correct(self):
        """Le patient le plus grave doit toujours sortir en premier."""
        p_leger   = creer_patient("Leger",   20)   # Blessure légère
        p_critique= creer_patient("Critique",90)   # Arrêt cardiaque
        p_moyen   = creer_patient("Moyen",   55)   # Fracture

        self.file.inserer(p_leger)
        self.file.inserer(p_critique)
        self.file.inserer(p_moyen)

        # Le critique doit sortir en premier
        premier = self.file.extraire_max()
        assert premier.nom == "Critique"

        deuxieme = self.file.extraire_max()
        assert deuxieme.nom == "Moyen"

        troisieme = self.file.extraire_max()
        assert troisieme.nom == "Leger"

    def test_extraire_file_vide(self):
        resultat = self.file.extraire_max()
        assert resultat is None

    # ── Tests de consultation ─────────────────────────────────

    def test_consulter_max_ne_modifie_pas_file(self):
        """consulter_max() ne doit pas changer la taille de la file."""
        self.file.inserer(creer_patient("P1", 80))
        self.file.inserer(creer_patient("P2", 40))

        taille_avant = self.file.taille()
        self.file.consulter_max()
        taille_apres = self.file.taille()

        assert taille_avant == taille_apres  # Aucun changement

    def test_consulter_max_retourne_le_plus_prioritaire(self):
        p_grave = creer_patient("Grave", 90)
        p_leger = creer_patient("Leger", 20)
        self.file.inserer(p_grave)
        self.file.inserer(p_leger)

        max_patient = self.file.consulter_max()
        assert max_patient.nom == "Grave"

    # ── Tests de la propriété du tas ──────────────────────────

    def test_propriete_tas_apres_insertions(self):
        """La racine doit toujours être le plus prioritaire."""
        scores = [30, 80, 50, 90, 20, 70]
        patients = [creer_patient(f"P{i}", s) for i, s in enumerate(scores)]

        for p in patients:
            self.file.inserer(p)

        # La racine doit avoir le score maximal
        max_score = max(scores)
        assert self.file.consulter_max().score_triage >= max_score * 0.9

    # ── Tests FIFO vs HEAP ────────────────────────────────────

    def test_superieur_a_fifo(self):
        """
        Démonstration : le heap traite le plus grave en premier,
        contrairement à une file FIFO.
        """
        # Ordre d'arrivée : léger, critique, moyen
        ordre_arrivee = ["Leger", "Critique", "Moyen"]
        scores        = {"Leger": 20, "Critique": 95, "Moyen": 55}

        for nom in ordre_arrivee:
            self.file.inserer(creer_patient(nom, scores[nom]))

        # HEAP : ordre de traitement doit être Critique → Moyen → Leger
        ordre_traitement = []
        while not self.file.est_vide():
            ordre_traitement.append(self.file.extraire_max().nom)

        assert ordre_traitement == ["Critique", "Moyen", "Leger"]
        # FIFO aurait donné : Leger → Critique → Moyen (DANGEREUX !)


# ── Lancer les tests directement ─────────────────────────────
if __name__ == "__main__":
    t = TestFilePriorite()
    tests = [
        t.test_inserer_un_patient,
        t.test_extraire_max_ordre_correct,
        t.test_consulter_max_ne_modifie_pas_file,
        t.test_superieur_a_fifo,
    ]
    print("\n── Tests FilePrioriteTriageQ ──")
    for test in tests:
        t.setup_method()
        try:
            test()
            print(f"  ✅ {test.__name__}")
        except AssertionError as e:
            print(f"  ❌ {test.__name__} : {e}")
    print()

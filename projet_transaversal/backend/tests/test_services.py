# ============================================================
#  PROJET  : Smart Santé 2035
#  FICHIER : tests/test_services.py
#  RÔLE    : Tests unitaires des services métier.
#  NIVEAU  : Licence 2 Informatique – GPI
# ============================================================

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from service.triage_service  import TriageService
from service.patient_service import PatientService


class TestTriageService:

    def setup_method(self):
        self.service = TriageService(capacite_max=50)

    def test_admettre_patient(self):
        p = self.service.admettre_patient("Rakoto","Jean",45, 80,60,30)
        assert p is not None
        assert p.nom == "Rakoto"
        assert p.niveau_priorite in range(1, 6)

    def test_admettre_augmente_file(self):
        avant = self.service.nb_patients_en_attente()
        self.service.admettre_patient("Test","X",30, 50,50,30)
        assert self.service.nb_patients_en_attente() == avant + 1

    def test_traiter_prochain(self):
        self.service.admettre_patient("P1","X",30, 90,80,70)  # Critique
        self.service.admettre_patient("P2","Y",30, 20,15,10)  # Léger
        premier = self.service.traiter_prochain()
        assert premier.nom == "P1"  # Le critique doit passer en premier

    def test_consulter_ne_reduit_pas_file(self):
        self.service.admettre_patient("Test","X",30, 50,50,30)
        avant = self.service.nb_patients_en_attente()
        self.service.consulter_prochain()
        assert self.service.nb_patients_en_attente() == avant

    def test_patient_critique_detecte(self):
        p = self.service.admettre_patient("Critique","X",30, 95,90,80)
        assert p.est_critique == True
        assert p.niveau_priorite <= 2

    def test_patient_non_critique(self):
        p = self.service.admettre_patient("Leger","X",30, 10,10,10)
        assert p.est_critique == False
        assert p.niveau_priorite >= 3


if __name__ == "__main__":
    t = TestTriageService()
    tests = [
        t.test_admettre_patient,
        t.test_admettre_augmente_file,
        t.test_traiter_prochain,
        t.test_consulter_ne_reduit_pas_file,
        t.test_patient_critique_detecte,
        t.test_patient_non_critique,
    ]
    print("\n── Tests TriageService ──")
    for test in tests:
        t.setup_method()
        try:
            test()
            print(f"  ✅ {test.__name__}")
        except AssertionError as e:
            print(f"  ❌ {test.__name__} : {e}")
    print()

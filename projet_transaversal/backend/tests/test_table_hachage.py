# ============================================================
#  PROJET  : Smart Santé 2035
#  FICHIER : tests/test_table_hachage.py
#  RÔLE    : Tests unitaires de la table de hachage.
#  NIVEAU  : Licence 2 Informatique – GPI
# ============================================================

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from algorithme.table_hachage import TableDeHachage


class TestTableHachage:

    def setup_method(self):
        self.table = TableDeHachage()

    def test_inserer_et_rechercher(self):
        self.table.inserer("PAT-001", "Rakoto Jean")
        assert self.table.rechercher("PAT-001") == "Rakoto Jean"

    def test_cle_inexistante(self):
        assert self.table.rechercher("INCONNU") is None

    def test_mise_a_jour(self):
        self.table.inserer("PAT-001", "Rakoto Jean")
        self.table.inserer("PAT-001", "Rakoto Jean (MàJ)")
        assert self.table.rechercher("PAT-001") == "Rakoto Jean (MàJ)"

    def test_supprimer(self):
        self.table.inserer("PAT-001", "Rakoto Jean")
        self.table.supprimer("PAT-001")
        assert self.table.rechercher("PAT-001") is None

    def test_nb_elements(self):
        for i in range(5):
            self.table.inserer(f"PAT-{i:03d}", f"Patient {i}")
        assert self.table.nb_elements() == 5

    def test_facteur_charge(self):
        assert self.table.facteur_charge() == 0.0
        self.table.inserer("K1", "V1")
        assert self.table.facteur_charge() > 0

    def test_redimensionnement(self):
        """Le redimensionnement ne doit pas perdre de données."""
        for i in range(20):
            self.table.inserer(f"KEY-{i}", f"VALUE-{i}")
        for i in range(20):
            assert self.table.rechercher(f"KEY-{i}") == f"VALUE-{i}"


if __name__ == "__main__":
    t = TestTableHachage()
    tests = [
        t.test_inserer_et_rechercher,
        t.test_cle_inexistante,
        t.test_mise_a_jour,
        t.test_supprimer,
        t.test_nb_elements,
        t.test_redimensionnement,
    ]
    print("\n── Tests TableDeHachage ──")
    for test in tests:
        t.setup_method()
        try:
            test()
            print(f"  ✅ {test.__name__}")
        except AssertionError as e:
            print(f"  ❌ {test.__name__} : {e}")
    print()

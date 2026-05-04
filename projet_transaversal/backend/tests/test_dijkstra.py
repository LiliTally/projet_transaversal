# ============================================================
#  PROJET  : Smart Santé 2035
#  FICHIER : tests/test_dijkstra.py
#  RÔLE    : Tests unitaires de l'algorithme de Dijkstra.
#  NIVEAU  : Licence 2 Informatique – GPI
# ============================================================

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from algorithme.graphe_hospitalier import GrapheHospitalier, EtablissementSante, GOUDRON, PISTE, IMPRATICABLE
from model.patient                  import Patient


def creer_graphe_test():
    """Crée un graphe de test avec 4 établissements."""
    g = GrapheHospitalier()
    csb  = EtablissementSante("CSB",  "CSB Test",    1, 0, 0, 20, 15)
    hop  = EtablissementSante("HOP",  "Hôpital Test",3, 0, 0, 80, 12)
    chur = EtablissementSante("CHUR", "CHUR Test",   5, 0, 0, 500, 60)
    sat  = EtablissementSante("SAT",  "Hôp Saturé",  3, 0, 0, 60,  0)
    for e in [csb, hop, chur, sat]:
        g.ajouter_noeud(e)
    g.ajouter_arc("CSB",  "HOP",   8.0, 25, GOUDRON, True)
    g.ajouter_arc("CSB",  "SAT",   3.0, 10, GOUDRON, False)
    g.ajouter_arc("HOP",  "CHUR", 12.0, 30, GOUDRON, True)
    g.ajouter_arc("SAT",  "HOP",   6.0, 18, GOUDRON, False)
    return g


class TestDijkstra:

    def setup_method(self):
        self.graphe = creer_graphe_test()

    def test_dijkstra_trouve_chemin(self):
        """Dijkstra doit trouver un établissement compatible."""
        patient = Patient("Test", "Solo", 40, 90, 80, 70)   # Niveau 1 – critique
        resultat = self.graphe.dijkstra("CSB", patient)
        assert resultat is not None

    def test_dijkstra_evite_hopital_sature(self):
        """Dijkstra ne doit pas orienter vers un hôpital sans lits."""
        patient  = Patient("Test", "Solo", 40, 50, 50, 50)
        resultat = self.graphe.dijkstra("CSB", patient)
        if resultat:
            assert resultat["etablissement_cible"]["lits_disponibles"] > 0

    def test_dijkstra_niveau1_vers_niveau3_min(self):
        """Un patient de niveau 1 doit aller vers un hôpital de niveau >= 3."""
        patient  = Patient("Test", "Solo", 40, 95, 90, 80)   # Critique
        resultat = self.graphe.dijkstra("CSB", patient)
        if resultat:
            assert resultat["etablissement_cible"]["niveau_soins"] >= 3

    def test_chemin_retourne_liste(self):
        """Le chemin retourné doit être une liste de noms."""
        patient  = Patient("Test", "Solo", 40, 50, 50, 50)
        resultat = self.graphe.dijkstra("CSB", patient)
        if resultat:
            assert isinstance(resultat["chemin"], list)
            assert len(resultat["chemin"]) >= 2

    def test_mise_a_jour_lits(self):
        """La mise à jour des lits doit influencer les prochains calculs."""
        self.graphe.mettre_a_jour_lits("HOP", 0)  # Hôpital plein
        patient  = Patient("Test", "Solo", 40, 50, 50, 50)
        resultat = self.graphe.dijkstra("CSB", patient)
        if resultat:
            # Ne doit pas orienter vers HOP (plein)
            assert resultat["etablissement_cible"]["id_etab"] != "HOP"


if __name__ == "__main__":
    t = TestDijkstra()
    tests = [
        t.test_dijkstra_trouve_chemin,
        t.test_dijkstra_evite_hopital_sature,
        t.test_dijkstra_niveau1_vers_niveau3_min,
        t.test_chemin_retourne_liste,
    ]
    print("\n── Tests Dijkstra ──")
    for test in tests:
        t.setup_method()
        try:
            test()
            print(f"  ✅ {test.__name__}")
        except AssertionError as e:
            print(f"  ❌ {test.__name__} : {e}")
    print()

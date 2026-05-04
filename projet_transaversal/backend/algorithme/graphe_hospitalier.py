# ============================================================
#  PROJET  : Smart Santé 2035
#  FICHIER : algorithme/graphe_hospitalier.py
#  RÔLE    : Graphe orienté pondéré du réseau hospitalier.
#            Implémente l'algorithme de Dijkstra pour trouver
#            l'orientation hospitalière optimale.
#
#  STRUCTURE : Liste d'adjacence (dict de listes)
#    noeuds : { id_etab → EtablissementSante }
#    arcs   : { id_source → [ (id_dest, distance, temps, etat, ambulance) ] }
#
#  DIJKSTRA :
#    Trouve le chemin de coût minimal dans un graphe à poids positifs.
#    Complexité : O((V + E) × log V)
#    Madagascar : V≈3000, E≈15000 → ≈207 000 opérations → quelques ms ✅
#
#  NIVEAU  : Licence 2 Informatique – GPI
# ============================================================

import heapq   # Module Python pour les files de priorité min (min-heap)


# ── Constantes pour l'état des routes ────────────────────────
GOUDRON      = "goudron"       # Route asphaltée  → facteur 1.0
PISTE        = "piste"         # Piste sablée     → facteur 1.8
IMPRATICABLE = "impraticable"  # Fermée saison pluies → infini


class EtablissementSante:
    """Représente un nœud dans le graphe hospitalier."""

    # Niveaux de soins
    CSB_I       = 1
    CSB_II      = 2
    HOPITAL_DIS = 3
    HOP_REF_REG = 4
    CHUR        = 5

    def __init__(self, id_etab, nom, niveau_soins,
                 latitude, longitude,
                 capacite_totale, lits_disponibles):
        self.id_etab          = id_etab
        self.nom              = nom
        self.niveau_soins     = niveau_soins
        self.latitude         = latitude
        self.longitude        = longitude
        self.capacite_totale  = capacite_totale
        self.lits_disponibles = lits_disponibles
        self.est_operationnel = True

    def taux_occupation(self):
        """Retourne le taux d'occupation entre 0.0 (vide) et 1.0 (plein)."""
        if self.capacite_totale == 0:
            return 1.0
        return 1.0 - (self.lits_disponibles / self.capacite_totale)

    def peut_accepter_patient(self, niveau_priorite):
        """
        Vérifie si l'établissement peut accueillir un patient
        du niveau de priorité donné.

        Règle : un patient critique (niveau 1) ne va pas dans un CSB.
        """
        if not self.est_operationnel:      return False
        if self.lits_disponibles <= 0:     return False
        if niveau_priorite == 1 and self.niveau_soins < 3: return False
        if niveau_priorite == 2 and self.niveau_soins < 2: return False
        return True

    def to_dict(self):
        return {
            "id_etab"          : self.id_etab,
            "nom"              : self.nom,
            "niveau_soins"     : self.niveau_soins,
            "lits_disponibles" : self.lits_disponibles,
            "capacite_totale"  : self.capacite_totale,
            "taux_occupation"  : f"{self.taux_occupation()*100:.0f}%",
            "est_operationnel" : self.est_operationnel,
        }

    def __str__(self):
        return (f"[{self.id_etab}] {self.nom} "
                f"| Niveau:{self.niveau_soins} "
                f"| Lits:{self.lits_disponibles}/{self.capacite_totale} "
                f"| {self.taux_occupation()*100:.0f}% occupé")


class GrapheHospitalier:
    """
    Graphe orienté pondéré du réseau hospitalier malgache.

    Structure interne :
      noeuds : dict { id_etab → EtablissementSante }
      arcs   : dict { id_source → liste de tuples (id_dest, dist, temps, etat, ambulance) }
    """

    def __init__(self):
        self.noeuds = {}   # { id → EtablissementSante }
        self.arcs   = {}   # { id_source → [(id_dest, dist_km, temps_min, etat, ambulance)] }

    # ── Construction du graphe ───────────────────────────────

    def ajouter_noeud(self, etab):
        """Ajoute un établissement de santé dans le graphe."""
        self.noeuds[etab.id_etab] = etab
        self.arcs[etab.id_etab]   = []
        print(f"✅ Nœud ajouté : {etab.nom}")

    def ajouter_arc(self, id_source, id_dest,
                    distance_km, temps_min, etat_route, ambulance=False):
        """
        Ajoute une route (arc) entre deux établissements.
        Le graphe est ORIENTÉ : arc de source vers dest seulement.
        Pour bidirectionnel → appeler deux fois avec source/dest inversés.
        """
        if id_source not in self.noeuds or id_dest not in self.noeuds:
            print("⚠ Un des établissements n'existe pas dans le graphe.")
            return
        self.arcs[id_source].append(
            (id_dest, distance_km, temps_min, etat_route, ambulance)
        )

    def _calculer_poids(self, temps_min, etat_route, etab_dest):
        """
        Calcule le coût réel d'un arc pour Dijkstra.

        FORMULE :
          coût = temps × facteur_route × facteur_disponibilité

        facteur_route :
          goudron      → 1.0  (normal)
          piste        → 1.8  (plus long, moins sûr)
          impraticable → infini (route fermée)

        facteur_disponibilité :
          hôpital vide → 1.0  (favorable)
          hôpital plein→ 4.0  (très défavorable)
        """
        # Facteur route
        if etat_route == GOUDRON:
            facteur_route = 1.0
        elif etat_route == PISTE:
            facteur_route = 1.8
        else:  # IMPRATICABLE
            return float('inf')

        # Facteur disponibilité (taux d'occupation de l'hôpital)
        taux = etab_dest.taux_occupation()
        facteur_dispo = 1.0 + (taux * 3.0)
        # taux 0%  → facteur 1.0 (parfait)
        # taux 80% → facteur 3.4 (presque plein)
        # taux 100%→ facteur 4.0 (plein, très défavorable)

        return temps_min * facteur_route * facteur_dispo

    # ═════════════════════════════════════════════════════════
    #  ALGORITHME DE DIJKSTRA
    # ═════════════════════════════════════════════════════════

    def dijkstra(self, id_source, patient):
        """
        Calcule le chemin optimal vers le meilleur établissement
        pour le patient donné.

        ÉTAPES :
          1. Initialiser toutes les distances à l'infini, source à 0
          2. Insérer tous les nœuds dans une file de priorité MIN
          3. Tant que la file n'est pas vide :
             a. Extraire le nœud u de distance minimale
             b. Pour chaque voisin v de u :
                → calculer nouvelle_dist = dist[u] + poids(u,v)
                → si nouvelle_dist < dist[v] : mettre à jour
          4. Trouver le meilleur établissement parmi les accessibles
          5. Reconstruire le chemin en remontant les prédécesseurs

        Complexité : O((V + E) × log V)

        Paramètres :
            id_source : ID de l'établissement de départ
            patient   : le patient à orienter

        Retourne un dict avec l'établissement cible et le chemin.
        """
        print(f"\n🔍 Dijkstra depuis '{self.noeuds[id_source].nom}' "
              f"pour patient niveau {patient.niveau_priorite}")

        # ── ÉTAPE 1 : Initialisation ──────────────────────────
        distances    = {id_e: float('inf') for id_e in self.noeuds}
        predecesseurs = {id_e: None        for id_e in self.noeuds}
        distances[id_source] = 0.0

        # ── ÉTAPE 2 : File de priorité MIN ────────────────────
        # Python heapq est un min-heap : (coût, id_etab)
        # On minimise le coût → le moins cher sort en premier
        file_min = [(0.0, id_source)]
        traites  = set()
        comparaisons = 0

        # ── ÉTAPE 3 : Boucle principale ───────────────────────
        while file_min:

            # 3a. Extraire le nœud u de coût minimal → O(log V)
            cout_u, id_u = heapq.heappop(file_min)

            # Si déjà traité → ignorer (entrée obsolète dans la file)
            if id_u in traites:
                continue
            traites.add(id_u)

            # Optimisation : si coût infini, les nœuds restants sont inaccessibles
            if cout_u == float('inf'):
                break

            # 3b. Relaxation de chaque voisin v de u
            for (id_v, dist_km, temps_min, etat, ambulance) in self.arcs[id_u]:

                if id_v in traites:
                    continue

                etab_v = self.noeuds[id_v]

                # Calcul du poids de l'arc u → v
                poids = self._calculer_poids(temps_min, etat, etab_v)
                comparaisons += 1

                nouvelle_dist = cout_u + poids

                # RELAXATION : meilleur chemin trouvé vers v ?
                if nouvelle_dist < distances[id_v]:
                    distances[id_v]     = nouvelle_dist
                    predecesseurs[id_v] = id_u
                    # Insérer dans la file avec le nouveau coût → O(log V)
                    heapq.heappush(file_min, (nouvelle_dist, id_v))

        print(f"   → Terminé en {comparaisons} comparaisons.")

        # ── ÉTAPE 4 : Trouver le meilleur établissement ───────
        return self._trouver_meilleur(
            id_source, patient, distances, predecesseurs
        )

    def _trouver_meilleur(self, id_source, patient, distances, predecesseurs):
        """
        Parmi tous les établissements accessibles,
        retourne celui avec le coût minimal compatible avec le patient.
        """
        meilleure_dest = None
        meilleur_cout  = float('inf')

        for id_e, cout in distances.items():
            if id_e == id_source:  continue   # Ignorer la source
            if cout >= float('inf'): continue  # Inaccessible

            etab = self.noeuds[id_e]
            if not etab.peut_accepter_patient(patient.niveau_priorite):
                continue  # Incompatible avec ce patient

            if cout < meilleur_cout:
                meilleur_cout  = cout
                meilleure_dest = id_e

        if meilleure_dest is None:
            print("⚠ Aucun établissement compatible trouvé !")
            return None

        # ── ÉTAPE 5 : Reconstruire le chemin ──────────────────
        chemin      = self._reconstruire_chemin(id_source, meilleure_dest,
                                                predecesseurs)
        dist_totale = self._calculer_distance_totale(chemin)
        temps_total = self._calculer_temps_total(chemin)

        etab_cible = self.noeuds[meilleure_dest]
        print(f"\n🏥 Meilleur établissement : {etab_cible.nom}")
        print(f"   Chemin : {' → '.join(chemin)}")
        print(f"   Distance : {dist_totale:.1f} km | Temps : {temps_total} min")

        return {
            "etablissement_cible" : etab_cible.to_dict(),
            "chemin"              : chemin,
            "distance_km"         : round(dist_totale, 1),
            "temps_minutes"       : temps_total,
            "cout_dijkstra"       : round(meilleur_cout, 2),
        }

    def _reconstruire_chemin(self, source, destination, predecesseurs):
        """
        Remonte les prédécesseurs de la destination jusqu'à la source.
        Puis inverse pour avoir le chemin dans le bon sens.

        Exemple :
          pred = {B→A, C→B, D→C}
          De A à D : D→C→B→A → inverser → A→B→C→D ✅
        """
        chemin = []
        noeud  = destination

        while noeud is not None:
            chemin.append(self.noeuds[noeud].nom)
            noeud = predecesseurs[noeud]

        chemin.reverse()
        return chemin

    def _calculer_distance_totale(self, chemin_noms):
        """Calcule la distance totale du chemin en km."""
        if len(chemin_noms) < 2:
            return 0.0
        total = 0.0
        # Convertir les noms en IDs
        nom_vers_id = {e.nom: id_e for id_e, e in self.noeuds.items()}
        for i in range(len(chemin_noms) - 1):
            id_src = nom_vers_id.get(chemin_noms[i])
            id_dst = nom_vers_id.get(chemin_noms[i + 1])
            if id_src and id_dst:
                for (id_v, dist, _, _, _) in self.arcs.get(id_src, []):
                    if id_v == id_dst:
                        total += dist
        return total

    def _calculer_temps_total(self, chemin_noms):
        """Calcule le temps de trajet total en minutes."""
        if len(chemin_noms) < 2:
            return 0
        total = 0
        nom_vers_id = {e.nom: id_e for id_e, e in self.noeuds.items()}
        for i in range(len(chemin_noms) - 1):
            id_src = nom_vers_id.get(chemin_noms[i])
            id_dst = nom_vers_id.get(chemin_noms[i + 1])
            if id_src and id_dst:
                for (id_v, _, temps, _, _) in self.arcs.get(id_src, []):
                    if id_v == id_dst:
                        total += temps
        return total

    def mettre_a_jour_lits(self, id_etab, nouveaux_lits):
        """Met à jour la disponibilité d'un établissement dans le graphe."""
        if id_etab in self.noeuds:
            self.noeuds[id_etab].lits_disponibles = nouveaux_lits
            print(f"🔄 Graphe mis à jour : {self.noeuds[id_etab].nom} "
                  f"→ {nouveaux_lits} lits dispo")

    def afficher_graphe(self):
        """Affiche le graphe complet."""
        print(f"\n══ Graphe Hospitalier ({len(self.noeuds)} établissements) ══")
        for id_e, etab in self.noeuds.items():
            print(f"  {etab}")
            for (id_v, dist, temps, etat, amb) in self.arcs[id_e]:
                print(f"    → {self.noeuds[id_v].nom} | "
                      f"{dist}km | {temps}min | {etat}"
                      + (" | 🚑" if amb else ""))
        print("══════════════════════════════════════\n")

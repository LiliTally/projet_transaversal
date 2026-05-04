# ============================================================
#  PROJET  : Smart Santé 2035
#  FICHIER : algorithme/file_priorite.py
#  RÔLE    : File de triage médical basée sur un tas binaire.
#            Garantit que le patient LE PLUS GRAVE est toujours
#            traité en premier.
#
#  STRUCTURE : Tas binaire max (max-heap) dans un tableau.
#
#  PROPRIÉTÉ DU TAS :
#    heap[i] est plus prioritaire que heap[2i+1] et heap[2i+2]
#
#  COMPLEXITÉS :
#    inserer()      → O(log n)  sift-up
#    extraire_max() → O(log n)  sift-down
#    consulter_max()→ O(1)      racine toujours disponible
#    construire()   → O(n)      algorithme de Floyd
#
#  NIVEAU  : Licence 2 Informatique – GPI
# ============================================================


class FilePrioriteTriageQ:
    """
    File de priorité pour le triage médical.
    Implémente un tas binaire max (binary max-heap).

    Représentation dans un tableau :
      - Parent de l'indice i   : (i - 1) // 2
      - Enfant gauche de i     : 2 * i + 1
      - Enfant droit  de i     : 2 * i + 2
    """

    def __init__(self, capacite_max=500):
        """
        Crée une file de triage vide.

        Paramètre :
            capacite_max : nombre maximum de patients simultanés
        """
        self._heap        = []          # Le tableau du tas
        self._capacite_max = capacite_max

    # ── Méthode 1 : INSÉRER ──────────────────────────────────

    def inserer(self, patient):
        """
        Insère un patient dans la file de triage.

        ALGORITHME :
          1. Ajouter le patient à la fin du tableau
          2. Faire remonter le patient à sa bonne place (sift-up)
             tant qu'il est plus prioritaire que son parent

        Complexité : O(log n)

        Exemple : n = 500 patients → au max log2(500) ≈ 9 comparaisons
        """
        if len(self._heap) >= self._capacite_max:
            print("⚠ File pleine ! Augmenter la capacité.")
            return False

        # Étape 1 : Ajouter en fin de tableau
        self._heap.append(patient)
        position = len(self._heap) - 1

        print(f"✅ Inséré en position {position} : {patient}")

        # Étape 2 : Faire remonter (SIFT-UP)
        self._sift_up(position)
        return True

    def _sift_up(self, i):
        """
        SIFT-UP (remonter vers le haut) :
        Remonte un patient dans le tas tant qu'il est
        plus prioritaire que son parent.

        Comme un patient grave qui "passe devant" les moins urgents.
        """
        while i > 0:
            parent = (i - 1) // 2   # Indice du parent

            # Si le patient actuel est plus prioritaire que son parent → échanger
            if self._heap[i].est_prioritaire_sur(self._heap[parent]):
                self._heap[i], self._heap[parent] = \
                    self._heap[parent], self._heap[i]
                i = parent  # Continuer à remonter
            else:
                break       # À sa bonne place → arrêter

    # ── Méthode 2 : EXTRAIRE MAX ────────────────────────────

    def extraire_max(self):
        """
        Extrait et retourne le patient LE PLUS PRIORITAIRE.

        ALGORITHME :
          1. Sauvegarder la racine (le plus grave)
          2. Mettre le dernier élément à la racine
          3. Réduire la taille de 1
          4. Faire descendre la nouvelle racine (sift-down)
          5. Retourner le patient sauvegardé

        Complexité : O(log n)
        """
        if self.est_vide():
            print("⚠ File vide, aucun patient à traiter.")
            return None

        # Étape 1 : Sauvegarder le patient le plus prioritaire (racine)
        patient_max = self._heap[0]
        print(f"🏥 Extraction : {patient_max}")

        # Étape 2 : Déplacer le dernier élément à la racine
        dernier = self._heap.pop()   # Retire le dernier élément

        if self._heap:
            self._heap[0] = dernier  # Le mettre à la racine
            # Étape 3 : Faire descendre (SIFT-DOWN)
            self._sift_down(0)

        return patient_max

    def _sift_down(self, i):
        """
        SIFT-DOWN (descendre vers le bas) :
        Descend un patient dans le tas jusqu'à sa bonne place.
        À chaque étape, on échange avec l'ENFANT LE PLUS PRIORITAIRE.
        """
        n = len(self._heap)

        while True:
            gauche       = 2 * i + 1   # Indice enfant gauche
            droite       = 2 * i + 2   # Indice enfant droit
            plus_grand   = i           # On suppose que le nœud actuel est le max

            # Comparer avec l'enfant gauche
            if (gauche < n and
                    self._heap[gauche].est_prioritaire_sur(self._heap[plus_grand])):
                plus_grand = gauche

            # Comparer avec l'enfant droit
            if (droite < n and
                    self._heap[droite].est_prioritaire_sur(self._heap[plus_grand])):
                plus_grand = droite

            # Si un enfant est plus prioritaire → échanger et continuer
            if plus_grand != i:
                self._heap[i], self._heap[plus_grand] = \
                    self._heap[plus_grand], self._heap[i]
                i = plus_grand
            else:
                break   # À sa bonne place → arrêter

    # ── Méthode 3 : CONSULTER MAX ───────────────────────────

    def consulter_max(self):
        """
        Retourne le patient le plus prioritaire SANS l'extraire.
        Utile pour afficher le prochain patient sur le tableau de bord.

        Complexité : O(1) — la racine est toujours le maximum
        """
        if self.est_vide():
            return None
        return self._heap[0]

    # ── Méthode 4 : CONSTRUIRE TAS (Floyd) ──────────────────

    def construire_tas(self, liste_patients):
        """
        Construit un tas à partir d'une liste de patients non triée.
        Utilise l'algorithme de Floyd : O(n) au lieu de O(n log n).

        ALGORITHME DE FLOYD :
          Appliquer sift-down sur tous les nœuds NON-FEUILLES,
          en partant du bas vers le haut.

        Complexité : O(n) — plus efficace que n insertions successives
        """
        self._heap = list(liste_patients)
        n = len(self._heap)

        # Le premier nœud feuille est à n//2
        # On part du dernier nœud non-feuille et on remonte
        for i in range(n // 2 - 1, -1, -1):
            self._sift_down(i)

        print(f"✅ Tas construit avec {n} patients (algorithme de Floyd O(n))")

    # ── Méthodes utilitaires ─────────────────────────────────

    def est_vide(self):
        """Retourne True si la file est vide."""
        return len(self._heap) == 0

    def taille(self):
        """Retourne le nombre de patients dans la file."""
        return len(self._heap)

    def afficher_file(self):
        """Affiche l'état de la file triée par priorité."""
        print(f"\n──── File de triage ({self.taille()} patients) ────")
        if self.est_vide():
            print("  File vide.")
        else:
            print(f"  [RACINE – LE PLUS URGENT] → {self._heap[0]}")
            for i in range(1, len(self._heap)):
                print(f"  [{i}] {self._heap[i]}")
        print("──────────────────────────────────────────\n")

    # ── Démonstration FIFO vs HEAP ───────────────────────────

    @staticmethod
    def demonstration_vs_fifo():
        """
        Compare la file FIFO et le tas binaire.
        Montre pourquoi le tas binaire est supérieur en médecine.
        """
        from model.patient import Patient

        print("\n══════════════════════════════════════════")
        print("  DÉMONSTRATION : FIFO vs Tas Binaire")
        print("══════════════════════════════════════════")

        # 3 patients arrivent dans cet ordre
        p1 = Patient("Rakoto", "Jean",  45, 20, 15, 10)  # Blessure légère
        p2 = Patient("Rabe",   "Marie", 30, 95, 85, 70)  # Arrêt cardiaque !
        p3 = Patient("Rasoa",  "Paul",  60, 55, 50, 40)  # Fracture

        print("\n📋 Ordre d'arrivée :")
        print(f"  1er : {p1}")
        print(f"  2ème: {p2}")
        print(f"  3ème: {p3}")

        print("\n❌ FILE FIFO (ordre d'arrivée) :")
        print("  1er traité → P1 (blessure légère)")
        print("  2ème traité → P2 (arrêt cardiaque... TROP TARD !")
        print("  Risque de décès évitable.")

        print("\n✅ FILE DE PRIORITÉ (tas binaire) :")
        file = FilePrioriteTriageQ()
        file.inserer(p1)
        file.inserer(p2)
        file.inserer(p3)

        print("\n  Ordre de traitement :")
        rang = 1
        while not file.est_vide():
            traite = file.extraire_max()
            print(f"  {rang}er traité → {traite}")
            rang += 1

        print("\n  → Le cas le plus grave est traité EN PREMIER ✅")
        print("══════════════════════════════════════════\n")

# ============================================================
#  PROJET  : Smart Santé 2035
#  FICHIER : algorithme/table_hachage.py
#  RÔLE    : Table de hachage maison avec chaînage.
#            Permet un accès O(1) aux dossiers patients.
#
#  GESTION DES COLLISIONS : Chaînage (Separate Chaining)
#    Si deux clés donnent le même indice, on les chaîne
#    dans une liste à cet indice.
#
#  REDIMENSIONNEMENT :
#    Quand facteur de charge > 0.75 → on double la capacité.
#
#  COMPLEXITÉ MOYENNE :
#    inserer()   → O(1)
#    rechercher()→ O(1)
#    supprimer() → O(1)
#
#  NIVEAU  : Licence 2 Informatique – GPI
# ============================================================


class TableDeHachage:
    """
    Table de hachage implémentée manuellement avec chaînage.
    Générique : peut stocker n'importe quelle paire (clé, valeur).
    """

    CAPACITE_INITIALE  = 16
    FACTEUR_CHARGE_MAX = 0.75

    def __init__(self):
        """Crée une table de hachage vide."""
        self._capacite  = self.CAPACITE_INITIALE
        self._nb_elements = 0
        # Tableau de seaux : chaque seau est une liste de tuples (clé, valeur)
        self._seaux = [[] for _ in range(self._capacite)]

    # ── Fonction de hachage ──────────────────────────────────

    def _calculer_indice(self, cle):
        """
        Transforme une clé en indice de tableau.

        ALGORITHME :
          1. hash() Python calcule un entier à partir de la clé
          2. abs() garantit un indice positif
          3. % capacité garde l'indice dans les bornes

        Exemple :
          cle = "PAT-001" → hash = 1234567 → abs = 1234567 → % 16 = 7
          L'entrée sera dans le seau n°7.

        Complexité : O(longueur de la clé) ≈ O(1) pour des clés courtes
        """
        return abs(hash(cle)) % self._capacite

    # ── Méthode 1 : INSÉRER / METTRE À JOUR ─────────────────

    def inserer(self, cle, valeur):
        """
        Insère ou met à jour une paire (clé, valeur).

        ALGORITHME :
          1. Calculer l'indice du seau
          2. Chercher si la clé existe dans ce seau
             → Oui : mettre à jour la valeur
             → Non : ajouter une nouvelle entrée
          3. Vérifier si redimensionnement nécessaire

        Complexité moyenne : O(1)
        """
        indice = self._calculer_indice(cle)
        seau   = self._seaux[indice]

        # Chercher si la clé existe déjà dans ce seau
        for i, (k, v) in enumerate(seau):
            if k == cle:
                seau[i] = (cle, valeur)   # Mise à jour
                return

        # Nouvelle entrée
        seau.append((cle, valeur))
        self._nb_elements += 1

        # Vérifier si redimensionnement nécessaire
        if self.facteur_charge() > self.FACTEUR_CHARGE_MAX:
            self._redimensionner()

    # ── Méthode 2 : RECHERCHER ───────────────────────────────

    def rechercher(self, cle):
        """
        Recherche la valeur associée à une clé.

        ALGORITHME :
          1. Calculer l'indice du seau
          2. Parcourir la liste chaînée de ce seau
          3. Retourner la valeur si clé trouvée

        Complexité moyenne : O(1)
        Pire cas : O(n) si toutes les clés dans le même seau
          (évité par une bonne fonction de hachage)
        """
        indice = self._calculer_indice(cle)
        for k, v in self._seaux[indice]:
            if k == cle:
                return v   # Trouvé !
        return None         # Non trouvé

    # ── Méthode 3 : SUPPRIMER ────────────────────────────────

    def supprimer(self, cle):
        """
        Supprime l'entrée correspondant à une clé.

        Complexité moyenne : O(1)
        """
        indice = self._calculer_indice(cle)
        seau   = self._seaux[indice]

        for i, (k, v) in enumerate(seau):
            if k == cle:
                seau.pop(i)
                self._nb_elements -= 1
                return True   # Supprimé

        return False   # Clé non trouvée

    # ── Méthode 4 : REDIMENSIONNER ───────────────────────────

    def _redimensionner(self):
        """
        Double la capacité quand le facteur de charge dépasse 0.75.
        Toutes les entrées sont ré-hachées dans le nouveau tableau.

        Pourquoi redimensionner ?
          Si le tableau est trop plein, les listes chaînées s'allongent
          et les accès passent de O(1) à O(n).

        Complexité : O(n) amorti
        """
        ancienne_capacite = self._capacite
        self._capacite   *= 2
        nouveaux_seaux    = [[] for _ in range(self._capacite)]

        print(f"⚡ Redimensionnement : {ancienne_capacite} → {self._capacite} seaux")

        # Ré-hacher toutes les entrées dans le nouveau tableau
        for seau in self._seaux:
            for cle, valeur in seau:
                nouvel_indice = abs(hash(cle)) % self._capacite
                nouveaux_seaux[nouvel_indice].append((cle, valeur))

        self._seaux = nouveaux_seaux

    # ── Méthodes utilitaires ─────────────────────────────────

    def facteur_charge(self):
        """Retourne le facteur de charge actuel (entre 0 et 1)."""
        return self._nb_elements / self._capacite

    def est_vide(self):
        """Retourne True si la table est vide."""
        return self._nb_elements == 0

    def nb_elements(self):
        """Retourne le nombre d'éléments stockés."""
        return self._nb_elements

    def afficher_etat(self):
        """Affiche l'état interne pour visualiser le chaînage."""
        print(f"\n──── Table de Hachage "
              f"({self._nb_elements} éléments, {self._capacite} seaux) ────")
        print(f"  Facteur de charge : "
              f"{self.facteur_charge():.2f} / {self.FACTEUR_CHARGE_MAX}")
        for i, seau in enumerate(self._seaux):
            if seau:
                entrees = " → ".join([f"({k}:{v})" for k, v in seau])
                print(f"  Seau[{i:2d}] → {entrees} → null")
        print("──────────────────────────────────────────\n")

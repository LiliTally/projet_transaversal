# ============================================================
#  PROJET  : Smart Santé 2035
#  FICHIER : database/db.py
#  RÔLE    : Gestion de la connexion à PostgreSQL.
#            En production, toutes les requêtes passent ici.
#  NIVEAU  : Licence 2 Informatique – GPI
# ============================================================

import os

# En production, installer : pip install psycopg2-binary
# Pour la démonstration, on simule la connexion

class Database:
    """
    Gestionnaire de connexion à la base de données PostgreSQL.
    Utilise le pattern Singleton pour une seule connexion partagée.
    """

    _instance = None  # Instance unique (Singleton)

    def __new__(cls):
        """Garantit qu'une seule instance est créée (Singleton)."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._connecte = False
        return cls._instance

    def connecter(self):
        """
        Établit la connexion à PostgreSQL.
        En production :
            import psycopg2
            self._conn = psycopg2.connect(
                host     = os.environ.get("DB_HOST", "localhost"),
                port     = os.environ.get("DB_PORT", "5432"),
                dbname   = os.environ.get("DB_NAME", "smartsante_db"),
                user     = os.environ.get("DB_USER", "postgres"),
                password = os.environ.get("DB_PASSWORD", "password")
            )
        """
        # Simulation pour la démonstration
        print("🔌 [Database] Connexion à PostgreSQL simulée.")
        self._connecte = True
        return self

    def executer(self, requete_sql, parametres=None):
        """
        Exécute une requête SQL.
        En production : utilise un curseur psycopg2.

        Exemple :
            db.executer(
                "INSERT INTO patients (id, nom, score) VALUES (%s, %s, %s)",
                (patient.id, patient.nom, patient.score_triage)
            )
        """
        if not self._connecte:
            self.connecter()
        print(f"📋 [Database] SQL : {requete_sql[:60]}...")
        return []   # Simulation : retourne une liste vide

    def fermer(self):
        """Ferme la connexion."""
        self._connecte = False
        print("🔌 [Database] Connexion fermée.")


# Instance globale partagée
db = Database()

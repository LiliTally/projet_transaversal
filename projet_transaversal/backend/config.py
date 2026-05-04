# ============================================================
#  PROJET  : Smart Santé 2035
#  FICHIER : config.py
#  RÔLE    : Configuration générale de l'application Flask.
#  NIVEAU  : Licence 2 Informatique – GPI
# ============================================================

import os

class Config:
    SECRET_KEY           = os.environ.get("SECRET_KEY", "smartsante2035-cle-secrete")
    DB_HOST              = os.environ.get("DB_HOST",     "localhost")
    DB_PORT              = os.environ.get("DB_PORT",     "5432")
    DB_NAME              = os.environ.get("DB_NAME",     "smartsante_db")
    DB_USER              = os.environ.get("DB_USER",     "postgres")
    DB_PASSWORD          = os.environ.get("DB_PASSWORD", "password")
    DATABASE_URL         = f"postgresql://{os.environ.get('DB_USER','postgres')}:{os.environ.get('DB_PASSWORD','password')}@{os.environ.get('DB_HOST','localhost')}:{os.environ.get('DB_PORT','5432')}/{os.environ.get('DB_NAME','smartsante_db')}"
    HOST                 = os.environ.get("HOST", "0.0.0.0")
    PORT                 = int(os.environ.get("PORT", 5000))
    DEBUG                = False
    CAPACITE_FILE_TRIAGE = int(os.environ.get("CAPACITE_FILE_TRIAGE", 500))
    FACTEUR_CHARGE_HASH  = 0.75
    JWT_EXPIRATION       = 3600  # 1 heure

class ConfigDeveloppement(Config):
    DEBUG   = True
    DB_NAME = "smartsante_dev"

class ConfigProduction(Config):
    DEBUG = False

class ConfigTest(Config):
    TESTING = True
    DB_NAME = "smartsante_test"

configurations = {
    "developpement": ConfigDeveloppement,
    "production"   : ConfigProduction,
    "test"         : ConfigTest,
    "defaut"       : ConfigDeveloppement,
}

def obtenir_config():
    """Retourne la configuration selon la variable d'environnement ENV."""
    env = os.environ.get("ENV", "defaut")
    return configurations.get(env, ConfigDeveloppement)

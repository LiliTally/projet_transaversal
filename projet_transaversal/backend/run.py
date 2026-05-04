# ============================================================
#  PROJET  : Smart Santé 2035
#  FICHIER : run.py
#  RÔLE    : Point d'entrée pour lancer le serveur Flask.
#  USAGE   : python run.py
#  NIVEAU  : Licence 2 Informatique – GPI
# ============================================================

from app import app
from config import obtenir_config

if __name__ == "__main__":
    config = obtenir_config()
    print("\n╔══════════════════════════════════════════════════╗")
    print("║       SMART SANTÉ 2035 – Serveur Flask           ║")
    print(f"║  Adresse : http://{config.HOST}:{config.PORT}            ║")
    print("║  Endpoints disponibles : GET /                   ║")
    print("╚══════════════════════════════════════════════════╝\n")
    app.run(
        host  = config.HOST,
        port  = config.PORT,
        debug = config.DEBUG
    )

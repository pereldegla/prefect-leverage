import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# Configuration de la connexion
db_host = "postgres"
db_user = "postgres"
db_password = "postgres"

# Se connecter au serveur PostgreSQL
conn = psycopg2.connect(
    host=db_host,
    user=db_user,
    password=db_password,
    dbname="postgres"
)

# Désactiver le mode transactionnel
conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

# Liste des noms de bases de données à créer
db_names = ["catalog_raw", "catalog_table","catalog_view"]

cur = conn.cursor()

# Créer les bases de données si elles n'existent pas
for db_name in db_names:
    cur.execute(sql.SQL("SELECT datname FROM pg_catalog.pg_database WHERE datname = {}").format(sql.Literal(db_name)))
    existing_db = cur.fetchone()
    if existing_db is None:
        cur.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(db_name)))
        print(f"Base de données {db_name} créée avec succès.")
    else:
        print(f"La base de données {db_name} existe déjà.")

cur.close()

# Fermer la connexion
conn.close()

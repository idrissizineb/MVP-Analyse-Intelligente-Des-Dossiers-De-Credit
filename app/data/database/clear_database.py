import sqlite3


DATABASE = "data/database/credit_analysis.db"


connection = sqlite3.connect(DATABASE)

cursor = connection.cursor()


# Supprimer les données
cursor.execute("DELETE FROM dossier_credit")
cursor.execute("DELETE FROM client")


# Réinitialiser les IDs auto-incrémentés
cursor.execute(
    "DELETE FROM sqlite_sequence WHERE name='dossier_credit'"
)

cursor.execute(
    "DELETE FROM sqlite_sequence WHERE name='client'"
)


connection.commit()

connection.close()


print("✅ Base de données nettoyée.")
from data.database.connection import DatabaseConnection
from data.database.database_manager import DatabaseManager


def main():

    database_connection = DatabaseConnection(
        "data/database/credit_analysis.db"
    )

    database_manager = DatabaseManager(
        database_connection
    )

    database_manager.initialize_database()

    database_connection.close()

    print("Database created successfully.")


if __name__ == "__main__":
    main()
from data.database.connection import DatabaseConnection
from data.database.database_manager import DatabaseManager


def main():

    database_connection = DatabaseConnection()

    database_manager = DatabaseManager(
        database_connection=database_connection
    )

    database_manager.initialize_database()

    print("Database schema initialized successfully.")

    database_connection.close()

    print("Database connection closed.")


if __name__ == "__main__":
    main()
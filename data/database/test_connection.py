from data.database.connection import DatabaseConnection  # pyright: ignore[reportMissingImports]


def main():

    database = DatabaseConnection()

    connection = database.connect()  # pyright: ignore[reportUnusedVariable]

    print("Database connection successful.")

    database.close()

    print("Database connection closed.")


if __name__ == "__main__":
    main()
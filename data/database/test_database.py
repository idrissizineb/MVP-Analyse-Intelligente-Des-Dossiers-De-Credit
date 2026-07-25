from data.database.connection import DatabaseConnection
from data.database.database_manager import DatabaseManager


def main():

    database_connection = DatabaseConnection()

    database_manager = DatabaseManager(
        database_connection=database_connection
    )

    database_manager.initialize_database()

    print(
        "Database schema initialized successfully."
    )

    # -------------------------------------------------
    # Create a client
    # -------------------------------------------------

    client_id = database_manager.create_client(
        nom_prenom="TEST CLIENT"
    )

    print(
        f"\nClient created successfully."
    )

    print(
        f"Client ID: {client_id}"
    )

    # -------------------------------------------------
    # Create first credit dossier
    # -------------------------------------------------

    dossier_id_1 = database_manager.create_dossier(
        client_id=client_id,
        numero_compte="2111112345670001",
        nature_credit="Acquisition logement",
        montant_credit=740000.00,
        date_production="2026-05-19",
    )

    print(
        f"\nFirst dossier created."
    )

    print(
        f"Dossier ID: {dossier_id_1}"
    )

    # -------------------------------------------------
    # Create second credit dossier
    # -------------------------------------------------

    dossier_id_2 = database_manager.create_dossier(
        client_id=client_id,
        numero_compte="2111112345670001",
        nature_credit="Crédit automobile",
        montant_credit=250000.00,
        date_production="2026-06-10",
    )

    print(
        f"\nSecond dossier created."
    )

    print(
        f"Dossier ID: {dossier_id_2}"
    )

    # -------------------------------------------------
    # Retrieve all dossiers of the client
    # -------------------------------------------------

    dossiers = database_manager.get_client_dossiers(
        client_id=client_id
    )

    print(
        "\n========== CLIENT DOSSIERS =========="
    )

    for dossier in dossiers:

        print(
            f"\nDossier ID: {dossier[0]}"
        )

        print(
            f"Client ID: {dossier[1]}"
        )

        print(
            f"Account Number: {dossier[2]}"
        )

        print(
            f"Credit Type: {dossier[3]}"
        )

        print(
            f"Amount: {dossier[4]}"
        )

        print(
            f"Production Date: {dossier[5]}"
        )

        print(
            f"Status: {dossier[7]}"
        )

    database_connection.close()

    print(
        "\nDatabase connection closed."
    )


if __name__ == "__main__":
    main()
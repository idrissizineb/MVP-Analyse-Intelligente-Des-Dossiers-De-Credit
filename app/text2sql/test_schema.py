from app.text2sql.schema_manager import SchemaManager


def main():

    manager = SchemaManager(
        "data/database/credit_analysis.db"
    )

    print("\n========== DATABASE SCHEMA ==========\n")

    print(manager.schema_as_text())


if __name__ == "__main__":

    main()
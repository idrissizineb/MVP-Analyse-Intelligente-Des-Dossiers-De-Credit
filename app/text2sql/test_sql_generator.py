from app.text2sql.sql_generator import SQLGenerator


def main():

    generator = SQLGenerator(
        "data/database/credit_analysis.db"
    )

    question = input("Question : ")

    sql = generator.generate_sql(question)

    print("\n========== GENERATED SQL ==========\n")

    print(sql)


if __name__ == "__main__":

    main()
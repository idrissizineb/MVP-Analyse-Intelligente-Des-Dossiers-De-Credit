from app.text2sql.sql_executor import SQLExecutor


def main():

    executor = SQLExecutor("data/database/credit_analysis.db")

    sql = "SELECT * FROM client"

    results = executor.execute(sql)

    print("\n========== RESULTS ==========\n")

    for row in results:

        print(row)


if __name__ == "__main__":

    main()
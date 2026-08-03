from app.text2sql.text2sql_pipeline import Text2SQLPipeline


def main():

    pipeline = Text2SQLPipeline()

    while True:

        print("\n========================================")
        print(" Banque Populaire - Text2SQL Assistant")
        print("========================================")

        question = input("\nQuestion (or 'exit'): ")

        if question.lower() == "exit":
            break

        response = pipeline.ask(question)

        if not response["success"]:

            print("\nSQL Validation Failed")
            print(response["error"])
            continue

        print("\n========== GENERATED SQL ==========\n")
        print(response["generated_sql"])

        print("\n========== SQL RESULTS ==========\n")
        print(response["results"])

        print("\n========== FINAL ANSWER ==========\n")
        print(response["answer"])


if __name__ == "__main__":
    main()
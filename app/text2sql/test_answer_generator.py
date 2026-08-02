from app.text2sql.answer_generator import AnswerGenerator


def main():

    generator = AnswerGenerator()

    question = "Quel est le montant du crédit de TEST CLIENT ?"

    results = [

        {

            "montant_credit": 740000

        }

    ]

    answer = generator.generate(

        question,

        results

    )

    print("\n========== ANSWER ==========\n")

    print(answer)


if __name__ == "__main__":

    main()
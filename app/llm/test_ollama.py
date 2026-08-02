from app.llm.ollama_client import OllamaClient


def main():

    llm = OllamaClient()

    print("\n========== OLLAMA TEST ==========\n")

    response = llm.chat(
        "Introduce yourself in one sentence."
    )

    print(response)


if __name__ == "__main__":

    main()
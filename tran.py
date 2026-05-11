import wikipedia
import nltk
from nltk.tokenize import sent_tokenize

# Download tokenizer
nltk.download('punkt')
nltk.download('punkt_tab')

print("=" * 50)
print("        AI CHATBOT WITH NLP")
print("=" * 50)
print("Type 'exit' to stop.")
print()

while True:

    user = input("You: ")

    if user.lower() == "exit":
        print("Bot: Goodbye!")
        break

    try:

        # Search Wikipedia
        result = wikipedia.summary(
            user,
            sentences=2
        )

        # NLP sentence tokenization
        sentences = sent_tokenize(result)

        # Print response
        print("Bot:", sentences[0])

    except wikipedia.exceptions.DisambiguationError as e:

        print("Bot: Your question is ambiguous. Try being more specific.")

    except wikipedia.exceptions.PageError:

        print("Bot: Sorry, I could not find information.")

    except Exception as e:

        print("Bot: Error occurred:", e)
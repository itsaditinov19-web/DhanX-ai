from modules.rag_engine import search_books

question = input(
    "Ask Trading Question: "
)

result = search_books(
    question
)

print(result)
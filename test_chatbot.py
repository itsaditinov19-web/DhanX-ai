from modules.rag_engine import ask_trading_question

question = input(
    "Ask Trading Question: "
)

answer = ask_trading_question(
    question
)

print("\n")
print(answer)
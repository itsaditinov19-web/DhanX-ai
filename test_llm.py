from modules.llm_engine import generate_answer

answer = generate_answer(

    "What is risk management?",

    "Risk management means limiting losses and protecting capital."
)

print(answer)
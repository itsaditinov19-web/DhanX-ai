from modules.vector_store import semantic_search
from modules.llm_engine import generate_answer
from modules.reranker import (
    rerank_results
)

def search_books(question):

    results = semantic_search(
        question,
        top_k=25
    )

    results = rerank_results(
        question,
        results,
        top_k=5
    )

    print("\n===== RETRIEVED CONTEXT =====")

    MAX_CONTEXT_CHARS = 2500

    final_text = ""

    for item in results:

        if len(final_text) > MAX_CONTEXT_CHARS:
            break

        final_text += item["text"] + "\n\n"

    print("Context Length:", len(final_text))

    return final_text

def ask_trading_question(
    question,
    chat_history=""
):

    context = search_books(
        question
    )
    from modules.market_context import (
    get_market_context
)

    market_context = get_market_context()

    enhanced_context = f"""

    LIVE MARKET CONTEXT

    {market_context}

    BOOK CONTEXT

    {context}

    """
    return generate_answer(
        question=question,
        context=context,
        chat_history=chat_history
    )
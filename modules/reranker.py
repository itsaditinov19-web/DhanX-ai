from sentence_transformers import CrossEncoder

reranker = CrossEncoder(
    "cross-encoder/ms-marco-MiniLM-L-6-v2"
)

def rerank_results(question, results, top_k=5):

    pairs = []

    for item in results:
        pairs.append(
            [question, item["text"]]
        )

    scores = reranker.predict(pairs)

    scored_results = list(
        zip(results, scores)
    )

    scored_results.sort(
        key=lambda x: x[1],
        reverse=True
    )

    return [
        item[0]
        for item in scored_results[:top_k]
    ]
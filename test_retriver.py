from pprint import pprint

from app.ai.retrievers.retriever_service import RetrieverService

retriever = RetrieverService()

results = retriever.retrieve(
    query="What is this document about?",
    top_k=3,
)

pprint(results)
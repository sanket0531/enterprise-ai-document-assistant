from typing import Any


class PromptBuilder:
    """
    Builds prompts for the RAG pipeline.
    """

    SYSTEM_PROMPT = """
You are an Enterprise AI Document Assistant.

Answer ONLY from the provided context.

If the answer is not present, reply:

"I couldn't find this information in the uploaded documents."
"""

    @classmethod
    def build(
        cls,
        question: str,
        retrieval_result: dict[str, Any],
    ) -> str:

        documents = retrieval_result.get("documents", [[]])

        chunks = documents[0] if documents else []

        context = []

        for index, chunk in enumerate(chunks, start=1):
            if not chunk.strip():
                continue

            context.append(
                f"Chunk {index}:\n{chunk}"
            )

        context_text = "\n\n".join(context)

        return f"""
{cls.SYSTEM_PROMPT}

Context:
{context_text}

Question:
{question}

Answer:
"""
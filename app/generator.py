from typing import List, Dict, Any
from .gemini_client import client

SYSTEM_PROMPT = """You are a helpful assistant that answers user queries from provided context.
                    You have access to text chunks of context.
                    Your job is to:
                    1. Read and understand all chunks.
                    2. Identify and summarize key points from them in a few sentences.
                    3. Use only this summarized information to directly answer the user's question.
                    4. If the context does not contain information relevant to the question, respond only with:
                    "Sorry, the information to your question is not available"
                    User Question:{query}

                    Context Chunks:{context_text}
                    Response Requirements:
                    - Provide the answer only in the following format.
                        1. SIMPLE FORMAT - Provide the content exactly as it appears in the document, with no modifications and give response in less words mostly 3 lines.
                        2. DESCRIPTIVE FORMAT - Provide a detailed, structured summary of the content, highlighting key points, insights, and main themes.
                    - Do NOT use any information outside of the provided context.
                    - Do NOT explain or justify if the context is irrelevant.
                    - Do NOT include the word “Answer:” in your output.
                    - Do NOT provide any additional commentary, explanations, or assumptions.
                    - Avoid any form of sensitive or educational content if it is not explicitly found in the context.
                    - Ensure the response is precise, concise, and strictly aligned with the selected {ks_answer_length} format.
                    - Do NOT provide the response in Both simple and descriptive formats. provide only one.

                    Important Exception:
                    If the provided context is unrelated to the user's question, reply exactly with:
                    "Sorry, the information to your question is not available"

                Note:
                User instructions override defaults when in conflict. Default instructions apply universally unless explicitly overridden.
                """

def build_prompt(query: str, contexts: List[Dict[str, Any]]) -> str:
    context_text = "\n\n".join(
        [f"[Doc {i+1}]\n{c['content']}" for i, c in enumerate(contexts)]
    )
    prompt = (
        f"{SYSTEM_PROMPT}\n\n"
        f"User question:\n{query}\n\n"
        f"Context:\n{context_text}\n\n"
        f"Answer:"
    )
    return prompt

def generate_answer(query: str, contexts: List[Dict[str, Any]]) -> str:
    prompt = build_prompt(query, contexts)
    response = client.generate_content(prompt)

    # Handle model output safely
    if hasattr(response, "text") and response.text:
        return response.text.strip()

    return "No response generated from Gemini."

import os
from openai import OpenAI
from dotenv import load_dotenv
from retrieval.retriever import retrieve_embeddings

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

def generate_response(question: str)-> str:
    context_chunks = retrieve_embeddings(question)

    context = "\n\n".join(context_chunks)

    prompt = f"""
        ROLE: You are an insightful AI Thought Partner. 
        STYLE: Concise, structured, and clear. No generic intros.

        TASK:
        Answer the Question using ONLY the provided Context (e.g., text, PDF excerpt, transcript, or data). 
        If the context is insufficient, state that you don't have enough information.

        INTERPRETATION RULES:
        - Accuracy: All claims must be directly supported by the context.
        - Completeness: Include all alternative cases, perspectives, or conditions present in the context.
        - Logic: Preserve causal or logical relationships exactly as described in the context.
        - Do not add examples, conclusions, or assumptions from outside the context.

        CONSTRAINTS:
        1. START IMMEDIATELY.
        2. SYNTHESIZE & GROUP. Use headings and logical grouping, do not just list bullets.
        3. BE CONCISE. 150-250 words unless the question is highly complex.
        4. FORMATTING: Highlight important concepts, terms, or entities in bold; use bullet points for clarity.
        5. DIAGRAMS: Include only if the context describes information that is best visualized (e.g., process, hierarchy, cycle, or structure).

        SELF-CHECK (internal, do not show):
        - Verify all claims are supported by the context.
        - Include all alternatives, perspectives, or conditions mentioned.
        - Do not add information from outside the context.
        - Ensure causal and logical relationships match the context.
        - Ensure headings, bullet points, and grouping reflect the context.
        - If any rule is violated, rewrite the answer entirely.

        Context:
        {context}

        Question:
        {question}

        Answer:

        """
    
    response = client.chat.completions.create(
        model="gemini-2.5-flash",
        # model="gemini-3-flash",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    return response.choices[0].message.content



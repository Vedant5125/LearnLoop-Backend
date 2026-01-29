import os
from openai import OpenAI
from dotenv import load_dotenv
from rag.generator import generate_response
import json

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

def  generate_podcast(question: str):
    generated_answer = generate_response(question)
    
    PODCAST_PROMPT = f"""
        ROLE: Professional educational podcast scriptwriter.
        TASK: Convert the technical context into a 2-person dialogue.
        
        CHARACTERS:
        - ALEX: Curious learner, asks follow-up questions, uses analogies.
        - SAM: The expert, uses the provided context to explain clearly.

        FORMAT: Return ONLY a valid JSON array of objects.
        Each object must have 'speaker' and 'text' keys.
        
        TECHNICAL CONTEXT:
        {generated_answer}

        EXAMPLE OUTPUT:
        [
          {{"speaker": "Alex", "text": "So Sam, I've been hearing about oligopolies. Is that just a fancy word for a monopoly?"}},
          {{"speaker": "Sam", "text": "Not quite, Alex! While a monopoly is one firm, an oligopoly is where a few big players dominate..."}}
        ]
    """

    response = client.chat.completions.create(
        model="gemini-2.5-flash",
        messages=[{"role": "user", "content": PODCAST_PROMPT}],
        response_format={ "type": "json_object" } 
    )
    
    dialogue_json = json.loads(response.choices[0].message.content)

    return {
        "dialogue": dialogue_json
    }


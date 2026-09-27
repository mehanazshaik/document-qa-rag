import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai


PROJECT_ROOT = Path(__file__).resolve().parent.parent
ENV_FILE = PROJECT_ROOT / ".env"

load_dotenv(ENV_FILE)

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file")

client = genai.Client(api_key=API_KEY)

MODEL_NAME = "gemini-3.5-flash-lite"


def generate_answer(question, retrieved_documents):

    context = ""

    for number, document in enumerate(retrieved_documents, start=1):

        context = context + f"""
Source {number}:
Document: {document["source"]}
Page: {document["page"]}

Content:
{document["text"]}

----------------------------------------
"""

    prompt = f"""
You are a document question-answering assistant.

Answer the user's question using ONLY the information provided
in the retrieved context below.

Do not use outside knowledge.

If the answer cannot be found in the retrieved context,
say:

"I could not find the answer in the provided documents."

User Question:
{question}

Retrieved Context:
{context}

Instructions:
1. Give a clear and concise answer.
2. Use only the retrieved context.
3. Do not invent information.
4. Include source citations using the document filename and page number.
"""

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )

    return response.text


if __name__ == "__main__":

    print("Generator module loaded successfully.")
    print("Gemini API key detected.")
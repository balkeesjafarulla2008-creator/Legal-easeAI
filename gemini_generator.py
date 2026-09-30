import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()


class GeminiDocumentGenerator:

    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError("GEMINI_API_KEY is not set in .env file")

        genai.configure(api_key=api_key)

        self.model_name = os.getenv(
            "GEMINI_MODEL",
            "gemini-1.5-pro"
        )

        self.model = genai.GenerativeModel(self.model_name)

    def generate_document(
        self,
        document_type,
        parties,
        terms,
        dates
    ):
        prompt = f"""
You are a legal document assistant.

Generate a professional draft legal document.

Document Type:
{document_type}

Parties:
{parties}

Terms:
{terms}

Dates:
{dates}

Requirements:
- Use clear and professional language.
- Include appropriate headings and sections.
- Keep the document structured and easy to edit.
- Do not invent important facts that were not provided.
- Add a general disclaimer that this is an AI-generated draft
  and should be reviewed by a qualified legal professional.
"""

        response = self.model.generate_content(prompt)

        return response.text
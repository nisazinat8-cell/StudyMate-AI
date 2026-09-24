import os
import time
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY was not found in the .env file.")

client = genai.Client(api_key=api_key)


def generate_study_content(study_text, feature, language):

    prompts = {
        "Easy Explanation": (
            "Explain the following study material in very easy language. "
            "Use headings, bullet points and a simple example."
        ),

        "Summary": (
            "Create a concise, exam-friendly summary of the following "
            "study material. Include the most important points."
        ),

        "Flashcards": (
            "Create 8 useful flashcards from the following material. "
            "Write each one as Question followed by Answer."
        ),

        "Quiz": (
            "Create 5 multiple-choice questions from the following material. "
            "Give four options for every question and provide an answer key "
            "at the end."
        )
    }

    prompt = f"""
You are StudyMate AI, a helpful learning assistant.

Task: {prompts[feature]}
Output language: {language}

Study material:
{study_text}
"""

    # Try up to 3 times if Gemini is temporarily unavailable
    for attempt in range(3):

        try:
            response = client.models.generate_content(
                model="gemini-3.6-flash",
                contents=prompt
            )

            if response.text:
                return response.text

            raise Exception("The AI returned an empty response.")

        except Exception as error:

            error_message = str(error)

            # Retry temporary server/high-demand errors
            if (
                "503" in error_message
                or "UNAVAILABLE" in error_message
                or "high demand" in error_message.lower()
            ):

                if attempt < 2:
                    time.sleep(3)
                    continue

                raise Exception(
                    "The AI service is temporarily busy. "
                    "Please wait a moment and click Generate again."
                )

            # Other errors should not be retried
            raise Exception(
                f"AI request failed: {error_message}"
            )
# To run this code you need to install the following dependencies:
# pip install google-genai

import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

def generate():
    client = genai.Client(
        api_key=os.environ.get("GEMINI_API_KEY"),
    )

    google_search_tool = types.Tool(
        google_search = types.GoogleSearch()
    )

    model = "gemini-2.5-flash-lite-preview-06-17"
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text="""Busque quando foi lançado o Gemini 2.5 flash lite?"""),
            ],
        ),
    ]
    generate_content_config = types.GenerateContentConfig(
        tools=[google_search_tool],
        thinking_config = types.ThinkingConfig(
            thinking_budget=8192,
        ),
        response_mime_type="text/plain",
    )

    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        print(chunk.text, end="")

if __name__ == "__main__":
    generate()

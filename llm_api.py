from google import genai

from .config import API_KEY, MODEL
from .prompt import SYSTEM_PROMPT
import json


client = genai.Client(api_key=API_KEY)


def ask_llm(user_input, lidar_info):

    response = client.models.generate_content(

        model=MODEL,

        contents=[
            lidar_info
            SYSTEM_PROMPT,
            user_input
        ]

    )

    text = response.text.strip()


    if text.startswith("```"):
        text = text.split("\n", 1)[1]
        text = text.rsplit("```", 1)[0].strip()

    return json.loads(text)

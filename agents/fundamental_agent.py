import os
from google.generativeai import GenerativeModel
from dotenv import load_dotenv

load_dotenv()

def analyze_fundamentals(fundamental_data, ticker):
    prompt = f"Analyze the following fundamental data for {ticker} and summarize the strengths and weaknesses for trading:\n{fundamental_data}"
    model = GenerativeModel(os.getenv("GEMINI_API_KEY"))
    response = model.generate_content(prompt)
    return response.text if hasattr(response, 'text') else response

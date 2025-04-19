from google.generativeai import GenerativeModel
import os

def assess_risk(fundamental_data, technical_data, sentiment_data, ticker):
    prompt = (
        f"Given the following data for {ticker}, assess the trading risk:\n"
        f"Fundamental: {fundamental_data}\n"
        f"Technical: {technical_data}\n"
        f"Sentiment: {sentiment_data}\n"
        "Highlight any major risk factors."
    )
    model = GenerativeModel(os.getenv("GEMINI_API_KEY"))
    response = model.generate_content(prompt)
    return response.text if hasattr(response, 'text') else response

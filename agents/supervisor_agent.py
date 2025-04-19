from google.generativeai import GenerativeModel
import os

def make_decision(fundamental, technical, sentiment, risk, ticker):
    prompt = (
        f"Based on the following analyses for {ticker}, recommend buy/hold/sell with reasons and analytics:\n"
        f"Fundamental: {fundamental}\n"
        f"Technical: {technical}\n"
        f"Sentiment: {sentiment}\n"
        f"Risk: {risk}\n"
        "Format output as: parsing, AR forecast (reasoning), buy/hold/sell with reason and analytics."
    )
    model = GenerativeModel(os.getenv("GEMINI_API_KEY"))
    response = model.generate_content(prompt)
    return response.text if hasattr(response, 'text') else response

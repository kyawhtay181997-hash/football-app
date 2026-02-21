import streamlit as st
import requests
from groq import Groq

# API Keys များ
GROQ_API_KEY = "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"
FOOTBALL_KEY = "5da489c665e54c44a227d7826b02134a"

client = Groq(api_key=GROQ_API_KEY)

def get_cleaned_data():
    url = "https://api.football-data.org/v4/matches"
    headers = {'X-Auth-Token': FOOTBALL_KEY}
    response = requests.get(url, headers=headers).json()
    
    cleaned_matches = []
    # Data ထဲက အရေးကြီးတဲ့ အချက်အလက်ပဲ ယူမယ် (Token သက်သာအောင်)
    for match in response.get('matches', []):
        match_info = {
            "homeTeam": match['homeTeam']['name'],
            "awayTeam": match['awayTeam']['name'],
            "competition": match['competition']['name'],
            "date": match['utcDate']
        }
        cleaned_matches.append(match_info)
    return cleaned_matches

def predict_matches():
    # Data ကို အရင်ချုံ့မယ်
    matches = get_cleaned_data()
    
    # ပွဲစဉ်စာရင်းကို စာသားအဖြစ်ပြောင်းမယ်
    matches_text = ""
    for m in matches:
        matches_text += f"{m['homeTeam']} vs {m['awayTeam']} ({m['competition']})\n"

    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "မင်းက ဘောလုံးကျွမ်းကျင်သူပါ။"},
                {"role": "user", "content": f"ဒီနေ့ပွဲတွေထဲက နိုင်ခြေအရှိဆုံး ၅ ပွဲကို ရွေးပေးပါ။ မြန်မာလိုရှင်းပြပါ။\n\nMatches:\n{matches_text}"}
            ]
        )
        print("\n--- ⚽ AI ခန့်မှန်းချက် ရလဒ် ⚽ ---\n")
        print(completion.choices[0].message.content)
    except Exception as e:
        print(f"Error: {e}")

predict_matches()
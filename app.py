import streamlit as st
import requests
from groq import Groq

# ၁။ API KEYS (မင်းရဲ့ Key တွေ ပြန်ထည့်ပါ)
GROQ_API_KEY = "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"
FOOTBALL_KEY = "5da489c665e54c44a227d7826b02134a"

st.set_page_config(page_title="AI Football Expert", page_icon="⚽")
st.title("⚽ AI ဘောလုံးပွဲ ခန့်မှန်းချက်နှင့် အကြံပြုချက်")

client = Groq(api_key=GROQ_API_KEY)

def get_cleaned_data():
    url = "https://api.football-data.org/v4/matches"
    headers = {'X-Auth-Token': FOOTBALL_KEY}
    try:
        response = requests.get(url, headers=headers).json()
        cleaned_matches = []
        if 'matches' in response:
            for match in response['matches']:
                match_info = {
                    "home": match['homeTeam']['name'],
                    "away": match['awayTeam']['name'],
                    "league": match['competition']['name']
                }
                cleaned_matches.append(match_info)
        return cleaned_matches
    except:
        return None

if st.button('ယနေ့အတွက် Tips များ ထုတ်ရန်'):
    with st.spinner('AI က Odds များနှင့် Tips များကို တွက်ချက်နေသည်...'):
        matches = get_cleaned_data()
        if matches:
            matches_text = "\n".join([f"{m['home']} vs {m['away']} ({m['league']})" for m in matches])
            
            # AI ကို အသေးစိတ် ခိုင်းစေခြင်း
            prompt = f"""
            မင်းက ဘောလုံးလောင်းကစားကျွမ်းကျင်သူပါ။ အောက်ပါပွဲစဉ်တွေအတွက်-
            ၁။ နိုင်ခြေအရှိဆုံး ၅ ပွဲကို ရွေးပါ။
            ၂။ ပွဲတစ်ပွဲချင်းစီအတွက် အကြံပြုချက် (ဥပမာ- W1, Over 1.5, Away Win) ပေးပါ။
            ၃။ ခန့်မှန်းခြေ Odds (ဥပမာ- 1.25, 1.50) ကို ထည့်ပေးပါ။
            ၄။ မြန်မာလိုပဲ ရှင်းပြပါ။ ဇယား (Table) ပုံစံနဲ့ ပြပေးပါ။

            Matches:
            {matches_text}
            """
            
            try:
                completion = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": prompt}]
                )
                st.success("တွက်ချက်မှု ပြီးပါပြီ!")
                st.markdown(completion.choices[0].message.content)
            except Exception as e:
                st.error(f"Error: {e}")
        else:
            st.warning("ဒေတာ မရှိသေးပါ။")

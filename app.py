import streamlit as st
import requests
from groq import Groq

# ၁။ API KEYS (မင်းရဲ့ Key တွေ ဒီမှာ အမှန်ပြန်ထည့်ပါ)
GROQ_API_KEY = "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"
FOOTBALL_KEY = "5da489c665e54c44a227d7826b02134a"

st.set_page_config(page_title="AI Football Betting Expert", page_icon="⚽", layout="wide")
st.title("⚽ AI ဘောလုံးပွဲ ခန့်မှန်းချက် နှင့် Betting Tips")
st.markdown("---")

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

if st.button('ယနေ့အတွက် အကောင်းဆုံး Tips ၅ ပွဲ ထုတ်ရန်'):
    with st.spinner('AI က နိုင်ခြေရှိသော Odds များနှင့် Tips များကို တွက်ချက်နေသည်...'):
        matches = get_cleaned_data()
        if matches:
            matches_text = "\n".join([f"{m['home']} vs {m['away']} ({m['league']})" for m in matches])
            
            # AI ကို အသေးစိတ် ခိုင်းစေသည့် Prompt
            prompt = f"""
            မင်းက ကမ္ဘာကျော် ဘောလုံးလောင်းကစား ကျွမ်းကျင်သူပါ။
            အောက်ပါ ပွဲစဉ်စာရင်းထဲကနေ နိုင်ခြေအရှိဆုံး ၅ ပွဲကို ရွေးပေးပါ။
            
            ရလဒ်ကို အောက်ပါ Markdown Table ပုံစံအတိုင်းပဲ ထုတ်ပေးပါ-
            | စဉ် | ပွဲစဉ် | အကြံပြုချက် (Tips) | ခန့်မှန်းခြေ Odds | သုံးသပ်ချက် |
            |----|------|-----------------|----------------|----------|
            
            ဥပမာ Tips နေရာမှာ (W1, W2, Over 1.5, GG) စသဖြင့် ထည့်ပါ။ 
            Odds နေရာမှာ (1.25, 1.85) စသဖြင့် ခန့်မှန်းပေးပါ။
            မြန်မာလိုပဲ ရေးပေးပါ။

            ယနေ့ပွဲစဉ်များ:
            {matches_text}
            """
            
            try:
                completion = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": prompt}]
                )
                st.success("✅ ခန့်မှန်းချက်များ ထွက်လာပါပြီ!")
                st.markdown(completion.choices[0].message.content)
            except Exception as e:
                st.error(f"AI Error: {e}")
        else:
            st.warning("⚠️ ယနေ့အတွက် ပွဲစဉ်ဒေတာ မရှိသေးပါ။")

st.markdown("---")
st.caption("Developed by AI Assistant | Data from Football-Data API")
